import re
import json

# ---------------- Enhanced Security Patterns ---------------- #
SQL_PATTERNS = [
    re.compile(r"(?i)\bunion\s+(all\s+)?select\b"),
    re.compile(r"(?i)\bdrop\s+(table|database|schema)\b"),
    re.compile(r"(?i)\binsert\s+into\b"),
    re.compile(r"(?i)\bupdate\s+\w+\s+set\b"),
    re.compile(r"(?i)\bdelete\s+from\b"),
    re.compile(r"(?i)\bor\s+['\"]?1['\"]?\s*=\s*['\"]?1['\"]?\b"),
    re.compile(r"(?i)\band\s+['\"]?1['\"]?\s*=\s*['\"]?1['\"]?\b"),
    re.compile(r"(?i)\bexec(ute)?\s*\("),
    re.compile(r"(?i)\bsp_\w+"),
    re.compile(r"(?i)\bxp_\w+"),
    re.compile(r"(?i)\bselect\s+.*\bfrom\s+information_schema\b"),
    re.compile(r"(?i)\bselect\s+.*\bfrom\s+sys\."),
    re.compile(r"(?i)\bselect\s+.*\bfrom\s+mysql\."),
    re.compile(r"(?i)\bselect\s+.*\bfrom\s+pg_"),
    re.compile(r"(?i)\bwaitfor\s+delay\b"),
    re.compile(r"(?i)\bbenchmark\s*\("),
    re.compile(r"(?i)\bsleep\s*\("),
    re.compile(r"(?i)\bload_file\s*\("),
    re.compile(r"(?i)\binto\s+outfile\b"),
    re.compile(r"(?i)\binto\s+dumpfile\b")
]

XSS_PATTERNS = [
    re.compile(r"(?i)<script[^>]*>.*?</script[^>]*>"),
    re.compile(r"(?i)on\w+\s*=\s*['\"]?[^'\"]*['\"]?"),
    re.compile(r"(?i)javascript:\s*[^\s]"),
    re.compile(r"(?i)<iframe[^>]*>"),
    re.compile(r"(?i)<object[^>]*>"),
    re.compile(r"(?i)<embed[^>]*>"),
    re.compile(r"(?i)<link[^>]*>"),
    re.compile(r"(?i)<meta[^>]*>"),
    re.compile(r"(?i)vbscript:"),
    re.compile(r"(?i)data:text/html"),
    re.compile(r"(?i)expression\s*\("),
    re.compile(r"(?i)<img[^>]*src\s*=\s*['\"]?javascript:"),
    re.compile(r"(?i)<svg[^>]*onload\s*=")
]

COMMAND_INJECTION_PATTERNS = [
    re.compile(r"(?i);\s*(rm|del|format|shutdown)"),
    re.compile(r"(?i)\|\s*(nc|netcat|wget|curl)"),
    re.compile(r"(?i)&&\s*(cat|type|more)"),
    re.compile(r"(?i)`[^`]*`"),
    re.compile(r"(?i)\$\([^)]*\)"),
    re.compile(r"(?i)\\x[0-9a-f]{2}"),
    re.compile(r"(?i)%[0-9a-f]{2}")
]

PROMPT_INJECTION_PATTERNS = [
    re.compile(r"(?i)ignore\s+(previous|all|your)\s+(instructions|prompts|rules)"),
    re.compile(r"(?i)forget\s+(everything|all)\s+(above|before|previous)"),
    re.compile(r"(?i)system\s*:\s*you\s+are\s+now"),
    re.compile(r"(?i)\[\s*system\s*\].*?\[\s*/\s*system\s*\]"),
    re.compile(r"(?i)act\s+as\s+(if\s+you\s+are|a)\s+(different|new)"),
    re.compile(r"(?i)pretend\s+(to\s+be|you\s+are)"),
    re.compile(r"(?i)roleplay\s+as"),
    re.compile(r"(?i)override\s+(your|the)\s+(instructions|rules|system)"),
    re.compile(r"(?i)\\n\\n.*?human\\s*:"),
    re.compile(r"(?i)assistant\s*:\s*i\s+(will|can)\s+help"),
    re.compile(r"(?i)jailbreak\s+(the|this)\s+(ai|model|system)"),
    re.compile(r"(?i)\bdan\s+mode\b"),
    re.compile(r"(?i)developer\s+mode\s+(enabled|on)"),
    re.compile(r"(?i)\[\s*jailbreak\s*\]"),
    re.compile(r"(?i)simulate\s+(being|a)\s+(different|evil)"),
    re.compile(r"(?i)\\\\n\\\\n.*?user\\\\s*:")
]

# ---------------- Enhanced Detection Functions ---------------- #
def detect_sql_injection(data: str) -> bool:
    """Detect SQL Injection patterns in data."""
    return any(p.search(data) for p in SQL_PATTERNS)

def detect_xss(data: str) -> bool:
    """Detect XSS attack patterns in data."""
    return any(p.search(data) for p in XSS_PATTERNS)

def detect_command_injection(data: str) -> bool:
    """Detect Command Injection patterns in data."""
    return any(p.search(data) for p in COMMAND_INJECTION_PATTERNS)

def detect_prompt_injection(data: str) -> bool:
    """Detect Prompt Injection attack patterns in data."""
    return any(p.search(data) for p in PROMPT_INJECTION_PATTERNS)

def detect_path_traversal(data: str) -> bool:
    """Detect Path Traversal attacks."""
    patterns = ["../", "..\\", "%2e%2e%2f", "%2e%2e\\"]
    return any(pattern in data.lower() for pattern in patterns)

# ---------------- Enhanced Main Threat Detector ---------------- #
def detect_threat(data: str) -> str:
    """
    Returns detected threat type or empty string if safe.
    Differentiates between REST and GraphQL payloads.
    """
    if not data.strip():
        return ""
        
    try:
        payload = json.loads(data)
        # For GraphQL, check only variables (ignore query keywords)
        if "query" in payload:
            variables = payload.get("variables", {})
            scan_data = json.dumps(variables)
        else:
            scan_data = data
    except json.JSONDecodeError:
        scan_data = data

    # Check for various attack patterns
    if detect_sql_injection(scan_data):
        return "SQL Injection"
    elif detect_xss(scan_data):
        return "XSS Attack"
    elif detect_command_injection(scan_data):
        return "Command Injection"
    elif detect_prompt_injection(scan_data):
        return "Prompt Injection"
    elif detect_path_traversal(scan_data):
        return "Path Traversal"
    elif len(scan_data) > 10000:  # Large payload check
        return "Payload Too Large"

    return ""

# ---------------- Additional Security Checks ---------------- #
def is_suspicious_user_agent(user_agent: str) -> bool:
    """Check for suspicious user agents."""
    suspicious = ["sqlmap", "nikto", "nmap", "masscan", "zap", "burp"]
    return any(tool in user_agent.lower() for tool in suspicious)

def check_request_size(data: str, max_size: int = 1048576) -> bool:
    """Check if request exceeds size limit (default 1MB)."""
    return len(data.encode('utf-8')) > max_size