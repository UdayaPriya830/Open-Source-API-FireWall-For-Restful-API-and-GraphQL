"""
Django Integration for API Firewall
Usage: Add to MIDDLEWARE in settings.py
"""

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import json
import time
from collections import defaultdict
import os
import sys

# Add firewall modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from detectors import detect_threat

class APIFirewallMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = defaultdict(list)
        self.rate_limit = int(os.getenv('RATE_LIMIT', 10))
        self.api_keys = [key.strip() for key in os.getenv('API_KEYS', '').split(',') if key.strip()]
        
    def process_request(self, request):
        client_ip = self.get_client_ip(request)
        current_time = time.time()
        
        # Rate limiting
        self.request_counts[client_ip] = [
            t for t in self.request_counts[client_ip] 
            if current_time - t < 60
        ]
        
        if len(self.request_counts[client_ip]) >= self.rate_limit:
            return JsonResponse(
                {'error': 'Rate limit exceeded'}, 
                status=429
            )
        
        self.request_counts[client_ip].append(current_time)
        
        # API key validation
        if self.api_keys and request.method == 'POST':
            api_key = request.META.get('HTTP_X_API_KEY')
            if not api_key or api_key not in self.api_keys:
                return JsonResponse(
                    {'error': 'Invalid API key'}, 
                    status=401
                )
        
        # Threat detection
        if hasattr(request, 'body') and request.body:
            body_str = request.body.decode('utf-8')
            threat = detect_threat(body_str)
            if threat:
                return JsonResponse(
                    {'error': f'Blocked: {threat}'}, 
                    status=400
                )
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')