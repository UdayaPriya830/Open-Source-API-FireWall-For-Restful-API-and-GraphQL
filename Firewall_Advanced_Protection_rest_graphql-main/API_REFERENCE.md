# 🔌 API Reference Guide

## 🚀 **Quick Start**

### **Installation**
```bash
# Clone and setup
git clone <repository>
cd Firewall_Advanced_Protection_rest_graphql-main

# Install dependencies
pip install -r requirements.txt

# Start services
python start.py
```

### **Access Points**
- **API Backend:** http://localhost:8000
- **Security Dashboard:** http://localhost:8501
- **API Documentation:** http://localhost:8000/docs

---

## 🛡️ **API Endpoints**

### **1. Health Check**
```http
GET /
```
**Response:**
```json
{
  "message": "API Firewall is active and monitoring traffic."
}
```

### **2. Test Endpoint**
```http
POST /test
Content-Type: application/json
x-api-key: mysecretapikey

{
  "message": "Your test message"
}
```

**Success Response:**
```json
{
  "received_message": "Your test message"
}
```

**Error Responses:**
```json
// Missing API Key
{
  "error": "Blocked: Invalid or Missing API Key"
}

// SQL Injection Detected
{
  "error": "Blocked: SQL Injection"
}

// Rate Limit Exceeded
{
  "error": "Blocked: Rate Limit Exceeded"
}
```

### **3. GraphQL Endpoint**
```http
POST /graphql
Content-Type: application/json
x-api-key: mysecretapikey

{
  "query": "query { user(id: 1) { id name email } }"
}
```

**Success Response:**
```json
{
  "data": {
    "user": {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    }
  }
}
```

---

## 🔒 **Security Headers**

### **Required Headers**
| Header | Required | Description |
|--------|----------|-------------|
| `x-api-key` | Yes* | API authentication key |
| `Content-Type` | Yes | application/json for POST requests |

*Not required for GET requests to `/`, `/docs`, `/openapi.json`

### **Optional Headers**
| Header | Description |
|--------|-------------|
| `User-Agent` | Client identification (monitored for suspicious tools) |
| `X-Forwarded-For` | Real client IP (if behind proxy) |

---

## ⚙️ **Configuration Reference**

### **Environment Variables (.env)**
```bash
# Rate limiting
RATE_LIMIT=10                    # Requests per minute per IP

# Access control
ALLOWED_IPS=127.0.0.1,192.168.1.5  # Comma-separated IPs (empty = allow all)
API_KEYS=key1,key2,key3          # Comma-separated API keys (empty = no auth)

# GraphQL security
MAX_GRAPHQL_DEPTH=5              # Maximum query depth allowed

# Request limits
MAX_REQUEST_SIZE=1048576         # Maximum request body size (bytes)

# ML features
ENABLE_ML_DETECTION=true         # Enable anomaly detection
```

---

## 🚨 **HTTP Status Codes**

| Code | Meaning | Trigger |
|------|---------|---------|
| **200** | OK | Request allowed and processed |
| **400** | Bad Request | Threat detected (SQL, XSS, etc.) |
| **401** | Unauthorized | Invalid or missing API key |
| **403** | Forbidden | IP not in allowlist |
| **429** | Too Many Requests | Rate limit exceeded |
| **500** | Internal Server Error | Server-side error |

---

## 🔍 **Threat Detection Patterns**

### **SQL Injection Patterns**
```regex
# Union-based attacks
(?i)\bunion\s+(all\s+)?select\b

# Database manipulation
(?i)\bdrop\s+(table|database|schema)\b
(?i)\binsert\s+into\b
(?i)\bupdate\s+\w+\s+set\b
(?i)\bdelete\s+from\b

# Boolean-based attacks
(?i)\bor\s+['\"]?1['\"]?\s*=\s*['\"]?1['\"]?\b
(?i)\band\s+['\"]?1['\"]?\s*=\s*['\"]?1['\"]?\b

# Time-based attacks
(?i)\bwaitfor\s+delay\b
(?i)\bbenchmark\s*\(
(?i)\bsleep\s*\(

# Information gathering
(?i)\bselect\s+.*\bfrom\s+information_schema\b
(?i)\bselect\s+.*\bfrom\s+sys\.
```

### **XSS Attack Patterns**
```regex
# Script injection
(?i)<script[^>]*>.*?</script[^>]*>

# Event handlers
(?i)on\w+\s*=\s*['\"]?[^'\"]*['\"]?

# JavaScript execution
(?i)javascript:\s*[^\s]

# Dangerous tags
(?i)<iframe[^>]*>
(?i)<object[^>]*>
(?i)<embed[^>]*>
```

### **Command Injection Patterns**
```regex
# Command chaining
(?i);\s*(rm|del|format|shutdown)
(?i)\|\s*(nc|netcat|wget|curl)
(?i)&&\s*(cat|type|more)

# Code execution
(?i)`[^`]*`
(?i)\$\([^)]*\)
```

---

## 📊 **Dashboard API**

### **Log Data Structure**
```json
{
  "timestamp": "Wed Nov  6 00:42:10 2025",
  "client_ip": "127.0.0.1",
  "method": "POST",
  "url": "http://localhost:8000/test",
  "threat_type": "SQL Injection",
  "status_code": 400,
  "body_size": 156
}
```

### **Dashboard Metrics**
- **Total Requests:** Count of all requests
- **Blocked Requests:** Count of threats detected
- **Allowed Requests:** Count of clean requests
- **Block Rate:** Percentage of blocked requests
- **Top IPs:** Most active client addresses
- **Threat Distribution:** Pie chart of threat types
- **Timeline:** Requests over time graph

---

## 🧪 **Testing Examples**

### **Normal Request Test**
```bash
curl -X POST http://localhost:8000/test \
  -H "Content-Type: application/json" \
  -H "x-api-key: mysecretapikey" \
  -d '{"message": "Hello World"}'
```

### **SQL Injection Test**
```bash
curl -X POST http://localhost:8000/test \
  -H "Content-Type: application/json" \
  -H "x-api-key: mysecretapikey" \
  -d '{"message": "'; DROP TABLE users; --"}'
```

### **XSS Attack Test**
```bash
curl -X POST http://localhost:8000/test \
  -H "Content-Type: application/json" \
  -H "x-api-key: mysecretapikey" \
  -d '{"message": "<script>alert(\"XSS\")</script>"}'
```

### **GraphQL Depth Test**
```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -H "x-api-key: mysecretapikey" \
  -d '{
    "query": "query { user(id: 1) { posts { comments { replies { author { posts { comments { text } } } } } } } }"
  }'
```

### **Rate Limiting Test**
```bash
# Run this multiple times quickly
for i in {1..15}; do
  curl http://localhost:8000/ -H "x-api-key: mysecretapikey"
done
```

---

## 🔧 **Integration Examples**

### **Python Requests**
```python
import requests

# Normal request
response = requests.post(
    'http://localhost:8000/test',
    json={'message': 'Hello API'},
    headers={'x-api-key': 'mysecretapikey'}
)
print(response.json())
```

### **JavaScript Fetch**
```javascript
fetch('http://localhost:8000/test', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-api-key': 'mysecretapikey'
  },
  body: JSON.stringify({message: 'Hello API'})
})
.then(response => response.json())
.then(data => console.log(data));
```

### **cURL Examples**
```bash
# GET request (no API key needed)
curl http://localhost:8000/

# POST with API key
curl -X POST http://localhost:8000/test \
  -H "Content-Type: application/json" \
  -H "x-api-key: mysecretapikey" \
  -d '{"message": "test"}'

# GraphQL query
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -H "x-api-key: mysecretapikey" \
  -d '{"query": "{ user(id: 1) { name } }"}'
```

---

## 🚨 **Error Handling**

### **Client Errors (4xx)**
```json
// 400 - Threat Detected
{
  "error": "Blocked: SQL Injection"
}

// 401 - Authentication Failed
{
  "error": "Blocked: Invalid or Missing API Key"
}

// 403 - Access Denied
{
  "error": "Blocked: IP Not Allowed"
}

// 429 - Rate Limited
{
  "error": "Blocked: Rate Limit Exceeded"
}
```

### **Server Errors (5xx)**
```json
// 500 - Internal Server Error
{
  "detail": "Internal server error"
}
```

---

## 📈 **Performance Guidelines**

### **Best Practices**
- Use connection pooling for high-volume requests
- Implement client-side rate limiting
- Cache API responses when possible
- Use compression for large payloads

### **Rate Limiting Strategy**
- Default: 10 requests/minute per IP
- Adjust based on your use case
- Consider different limits for different endpoints
- Implement exponential backoff on 429 responses

### **Security Recommendations**
- Rotate API keys regularly
- Use HTTPS in production
- Implement request signing for sensitive operations
- Monitor logs for attack patterns

---

## 🔍 **Monitoring & Debugging**

### **Log Analysis**
```bash
# View recent logs
tail -f backend/firewall_logs.json

# Count threats by type
grep "SQL Injection" backend/firewall_logs.json | wc -l

# Find top attacking IPs
grep "threat_type" backend/firewall_logs.json | \
  jq -r '.client_ip' | sort | uniq -c | sort -nr
```

### **Health Monitoring**
```bash
# Check API health
curl http://localhost:8000/

# Check dashboard health
curl http://localhost:8501/

# Monitor response times
time curl http://localhost:8000/
```

---

## 🛠️ **Troubleshooting**

### **Common Issues**

**Connection Refused**
```bash
# Check if services are running
netstat -an | grep :8000
netstat -an | grep :8501
```

**Rate Limit Hit**
```bash
# Wait 60 seconds or restart service
# Or increase RATE_LIMIT in .env
```

**API Key Rejected**
```bash
# Verify key in .env file
# Check header spelling: x-api-key
```

**Threat False Positive**
```bash
# Check detectors.py patterns
# Adjust patterns if needed
# Whitelist specific patterns
```

---

**📚 This API reference provides everything needed to integrate with and operate the API Firewall system.**