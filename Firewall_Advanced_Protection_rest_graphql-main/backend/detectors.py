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

# OWASP Top 10 - Additional Patterns
BROKEN_ACCESS_CONTROL_PATTERNS = [
    re.compile(r"(?i)\.\./(.*/)*(etc|passwd|shadow)"),
    re.compile(r"(?i)/admin|/administrator|/root"),
    re.compile(r"(?i)user_id=\d+.*user_id=\d+"),  # Parameter pollution
    re.compile(r"(?i)role=admin|role=root|role=superuser")
]

CRYPTO_FAILURE_PATTERNS = [
    re.compile(r"(?i)(password|pwd|pass)\s*=\s*['\"][^'\"]{1,8}['\"]")
]

INSECURE_DESIGN_PATTERNS = [
    re.compile(r"(?i)debug=true|debug=1"),
    re.compile(r"(?i)test=true|test=1"),
    re.compile(r"(?i)admin=true|admin=1")
]

SECURITY_MISCONFIG_PATTERNS = [
    re.compile(r"(?i)\bdefault\b.*\b(password|pwd|pass)\b"),
    re.compile(r"(?i)\b(admin|root|test):(admin|root|test|password|123456)\b")
]

VULNERABLE_COMPONENTS_PATTERNS = [
    re.compile(r"(?i)version\s*[=:]\s*['\"]?\d+\.\d+\.\d+['\"]?"),
    re.compile(r"(?i)jquery.*1\.[0-7]\."),  # Old jQuery versions
    re.compile(r"(?i)apache.*2\.[0-2]\.")   # Old Apache versions
]

AUTH_FAILURE_PATTERNS = [
    re.compile(r"(?i)session_id=.*session_id="),  # Session fixation
    re.compile(r"(?i)remember_me=true.*password="),
    re.compile(r"(?i)auto_login=true|auto_login=1")
]

INTEGRITY_FAILURE_PATTERNS = [
    re.compile(r"(?i)eval\s*\("),
    re.compile(r"(?i)exec\s*\("),
    re.compile(r"(?i)system\s*\("),
    re.compile(r"(?i)shell_exec\s*\(")
]

LOGGING_FAILURE_PATTERNS = [
    re.compile(r"(?i)log_level\s*=\s*(debug|trace)"),
    re.compile(r"(?i)disable.*log"),
    re.compile(r"(?i)no.*audit")
]

SSRF_PATTERNS = [
    re.compile(r"(?i)url\s*=\s*['\"]?https?://localhost"),
    re.compile(r"(?i)url\s*=\s*['\"]?https?://127\.0\.0\.1"),
    re.compile(r"(?i)url\s*=\s*['\"]?https?://192\.168\."),
    re.compile(r"(?i)url\s*=\s*['\"]?https?://10\."),
    re.compile(r"(?i)url\s*=\s*['\"]?file://")
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

# OWASP Top 10 Detection Functions
def detect_broken_access_control(data: str) -> bool:
    """OWASP #1 - Broken Access Control"""
    return any(p.search(data) for p in BROKEN_ACCESS_CONTROL_PATTERNS)

def detect_crypto_failure(data: str) -> bool:
    """OWASP #2 - Cryptographic Failures"""
    return any(p.search(data) for p in CRYPTO_FAILURE_PATTERNS)

def detect_insecure_design(data: str) -> bool:
    """OWASP #4 - Insecure Design"""
    return any(p.search(data) for p in INSECURE_DESIGN_PATTERNS)

def detect_security_misconfiguration(data: str) -> bool:
    """OWASP #5 - Security Misconfiguration"""
    return any(p.search(data) for p in SECURITY_MISCONFIG_PATTERNS)

def detect_vulnerable_components(data: str) -> bool:
    """OWASP #6 - Vulnerable and Outdated Components"""
    return any(p.search(data) for p in VULNERABLE_COMPONENTS_PATTERNS)

def detect_auth_failure(data: str) -> bool:
    """OWASP #7 - Identification and Authentication Failures"""
    return any(p.search(data) for p in AUTH_FAILURE_PATTERNS)

def detect_integrity_failure(data: str) -> bool:
    """OWASP #8 - Software and Data Integrity Failures"""
    return any(p.search(data) for p in INTEGRITY_FAILURE_PATTERNS)

def detect_logging_failure(data: str) -> bool:
    """OWASP #9 - Security Logging and Monitoring Failures"""
    return any(p.search(data) for p in LOGGING_FAILURE_PATTERNS)

def detect_ssrf(data: str) -> bool:
    """OWASP #10 - Server-Side Request Forgery"""
    return any(p.search(data) for p in SSRF_PATTERNS)

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

    # Check for various attack patterns (OWASP Top 10 Coverage)
    if detect_sql_injection(scan_data):
        return "SQL Injection (OWASP #3)"
    elif detect_xss(scan_data):
        return "XSS Attack (OWASP #3)"
    elif detect_broken_access_control(scan_data):
        return "Broken Access Control (OWASP #1)"
    elif detect_crypto_failure(scan_data):
        return "Cryptographic Failure (OWASP #2)"
    elif detect_insecure_design(scan_data):
        return "Insecure Design (OWASP #4)"
    elif detect_security_misconfiguration(scan_data):
        return "Security Misconfiguration (OWASP #5)"
    elif detect_vulnerable_components(scan_data):
        return "Vulnerable Components (OWASP #6)"
    elif detect_auth_failure(scan_data):
        return "Authentication Failure (OWASP #7)"
    elif detect_integrity_failure(scan_data):
        return "Integrity Failure (OWASP #8)"
    elif detect_logging_failure(scan_data):
        return "Logging Failure (OWASP #9)"
    elif detect_ssrf(scan_data):
        return "SSRF Attack (OWASP #10)"
    elif detect_command_injection(scan_data):
        return "Command Injection"
    elif detect_prompt_injection(scan_data):
        return "Prompt Injection (AI/LLM)"
    elif detect_path_traversal(scan_data):
        return "Path Traversal"
    elif len(scan_data) > 10000:
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