from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from detectors import detect_threat
from dotenv import load_dotenv
import os, time, json
from graphql import parse
from collections import defaultdict

load_dotenv()

RATE_LIMIT = int(os.getenv("RATE_LIMIT", 10))
ALLOWED_IPS = [ip.strip() for ip in os.getenv("ALLOWED_IPS", "").split(",") if ip.strip()]
API_KEYS = [key.strip() for key in os.getenv("API_KEYS", "").split(",") if key.strip()]
MAX_DEPTH = int(os.getenv("MAX_GRAPHQL_DEPTH", 5))

request_counts = defaultdict(list)
LOG_FILE = "firewall_logs.json"

def log_request(data: dict):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"Logging error: {e}")

# ---------------- GraphQL Threat Detection ---------------- #
def get_depth(node, current_depth=0):
    """Recursively calculates the depth of a GraphQL query."""
    if hasattr(node, "selection_set") and node.selection_set:
        return max(get_depth(sel, current_depth + 1) for sel in node.selection_set.selections)
    return current_depth

def detect_graphql_threat(data: str) -> str:
    """Detects GraphQL-specific threats."""
    if not data.strip():
        return ""
    
    try:
        payload = json.loads(data)
        query = payload.get("query", "")
        
        # Check for introspection queries
        if "__schema" in query or "__type" in query:
            return "GraphQL Introspection Blocked"
        
        # Parse and check depth
        tree = parse(query)
        depth = max(get_depth(sel) for sel in tree.definitions if hasattr(sel, 'selection_set'))
        if depth > MAX_DEPTH:
            return f"Query depth {depth} exceeds limit {MAX_DEPTH}"
            
    except json.JSONDecodeError:
        return "Invalid JSON in GraphQL request"
    except Exception as e:
        return f"GraphQL parsing error: {str(e)[:50]}"
    return ""

# ---------------- API Firewall Middleware ---------------- #
class APIFirewallMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        threat_type = ""
        status_code = 200
        
        # Read and preserve request body
        body = await request.body()
        data_str = body.decode("utf-8") if body else ""
        
        # Create new request with preserved body
        async def receive():
            return {"type": "http.request", "body": body}
        request._receive = receive

        # IP allowlist check (highest priority)
        if ALLOWED_IPS and client_ip not in ALLOWED_IPS:
            threat_type, status_code = "IP Not Allowed", 403
        
        # API key check (skip for GET requests to public endpoints)
        elif API_KEYS and not (request.method == "GET" and request.url.path in ["/", "/docs", "/openapi.json"]):
            api_key = request.headers.get("x-api-key")
            if not api_key or api_key not in API_KEYS:
                threat_type, status_code = "Invalid or Missing API Key", 401
        
        # Rate limiting
        if not threat_type:
            request_counts[client_ip] = [t for t in request_counts[client_ip] if current_time - t < 60]
            if len(request_counts[client_ip]) >= RATE_LIMIT:
                threat_type, status_code = "Rate Limit Exceeded", 429
            else:
                request_counts[client_ip].append(current_time)

        # Threat detection
        if not threat_type and data_str:
            if "/graphql" in request.url.path:
                threat_type = detect_graphql_threat(data_str)
            else:
                threat_type = detect_threat(data_str)
            if threat_type:
                status_code = 400

        # Log request
        log_data = {
            "timestamp": time.ctime(),
            "client_ip": client_ip,
            "method": request.method,
            "url": str(request.url),
            "threat_type": threat_type or "None",
            "status_code": status_code,
            "body_size": len(data_str)
        }
        log_request(log_data)

        # Block if threat detected
        if threat_type:
            return JSONResponse({"error": f"Blocked: {threat_type}"}, status_code=status_code)

        return await call_next(request)
