"""
Flask Integration for API Firewall
Usage: app.wsgi_app = APIFirewallMiddleware(app.wsgi_app)
"""

from flask import Flask, request, jsonify
from functools import wraps
import time
from collections import defaultdict
import os
import sys

# Add firewall modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from detectors import detect_threat

class APIFirewallMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app
        self.request_counts = defaultdict(list)
        self.rate_limit = int(os.getenv('RATE_LIMIT', 10))
        self.api_keys = [key.strip() for key in os.getenv('API_KEYS', '').split(',') if key.strip()]

    def __call__(self, environ, start_response):
        def new_start_response(status, response_headers, exc_info=None):
            return start_response(status, response_headers, exc_info)
        
        # Get client IP
        client_ip = environ.get('HTTP_X_FORWARDED_FOR', environ.get('REMOTE_ADDR', ''))
        if ',' in client_ip:
            client_ip = client_ip.split(',')[0].strip()
        
        current_time = time.time()
        
        # Rate limiting
        self.request_counts[client_ip] = [
            t for t in self.request_counts[client_ip] 
            if current_time - t < 60
        ]
        
        if len(self.request_counts[client_ip]) >= self.rate_limit:
            response = b'{"error": "Rate limit exceeded"}'
            start_response('429 Too Many Requests', [
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(response)))
            ])
            return [response]
        
        self.request_counts[client_ip].append(current_time)
        
        # API key validation for POST requests
        if environ.get('REQUEST_METHOD') == 'POST' and self.api_keys:
            api_key = environ.get('HTTP_X_API_KEY')
            if not api_key or api_key not in self.api_keys:
                response = b'{"error": "Invalid API key"}'
                start_response('401 Unauthorized', [
                    ('Content-Type', 'application/json'),
                    ('Content-Length', str(len(response)))
                ])
                return [response]
        
        return self.wsgi_app(environ, new_start_response)

def firewall_decorator(f):
    """Decorator for individual Flask routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Threat detection
        if request.data:
            body_str = request.data.decode('utf-8')
            threat = detect_threat(body_str)
            if threat:
                return jsonify({'error': f'Blocked: {threat}'}), 400
        return f(*args, **kwargs)
    return decorated_function

# Usage example:
"""
from flask import Flask
from integrations.flask_integration import APIFirewallMiddleware, firewall_decorator

app = Flask(__name__)
app.wsgi_app = APIFirewallMiddleware(app.wsgi_app)

@app.route('/api/test', methods=['POST'])
@firewall_decorator
def test_endpoint():
    return {'message': 'Success'}
"""