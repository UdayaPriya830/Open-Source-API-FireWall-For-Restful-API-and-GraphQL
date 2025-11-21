#!/usr/bin/env python3
"""
Quick test script for API Firewall functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_normal_request():
    """Test normal API request."""
    print("✅ Testing normal request...")
    response = requests.post(
        f"{BASE_URL}/test",
        json={"message": "Hello, this is a normal request"},
        headers={"x-api-key": "mysecretapikey"}
    )
    print(f"Status: {response.status_code}, Response: {response.json()}")

def test_sql_injection():
    """Test SQL injection detection."""
    print("🚨 Testing SQL injection...")
    response = requests.post(
        f"{BASE_URL}/test",
        json={"message": "'; DROP TABLE users; --"},
        headers={"x-api-key": "mysecretapikey"}
    )
    print(f"Status: {response.status_code}, Response: {response.json()}")

def test_xss_attack():
    """Test XSS attack detection."""
    print("🚨 Testing XSS attack...")
    response = requests.post(
        f"{BASE_URL}/test",
        json={"message": "<script>alert('XSS')</script>"},
        headers={"x-api-key": "mysecretapikey"}
    )
    print(f"Status: {response.status_code}, Response: {response.json()}")

def test_graphql_query():
    """Test GraphQL query."""
    print("📊 Testing GraphQL query...")
    query = {
        "query": "query { user(id: 1) { id name email } }"
    }
    response = requests.post(
        f"{BASE_URL}/graphql",
        json=query,
        headers={"x-api-key": "mysecretapikey"}
    )
    print(f"Status: {response.status_code}")

def test_deep_graphql_query():
    """Test deep GraphQL query (should be blocked)."""
    print("🚨 Testing deep GraphQL query...")
    query = {
        "query": """
        query {
            user(id: 1) {
                posts {
                    comments {
                        replies {
                            author {
                                posts {
                                    comments {
                                        text
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        """
    }
    response = requests.post(
        f"{BASE_URL}/graphql",
        json=query,
        headers={"x-api-key": "mysecretapikey"}
    )
    print(f"Status: {response.status_code}, Response: {response.json()}")

def test_rate_limiting():
    """Test rate limiting."""
    print("⏱️  Testing rate limiting...")
    for i in range(12):  # Exceed rate limit of 10
        response = requests.get(
            f"{BASE_URL}/",
            headers={"x-api-key": "mysecretapikey"}
        )
        print(f"Request {i+1}: Status {response.status_code}")
        if response.status_code == 429:
            print("Rate limit triggered!")
            break
        time.sleep(0.1)

def test_invalid_api_key():
    """Test invalid API key."""
    print("🔑 Testing invalid API key...")
    response = requests.post(
        f"{BASE_URL}/test",
        json={"message": "Hello"},
        headers={"x-api-key": "invalid_key"}
    )
    print(f"Status: {response.status_code}, Response: {response.json()}")

def main():
    print("🛡️  API Firewall Test Suite")
    print("=" * 40)
    
    tests = [
        test_normal_request,
        test_sql_injection,
        test_xss_attack,
        test_graphql_query,
        test_deep_graphql_query,
        test_invalid_api_key,
        test_rate_limiting
    ]
    
    for test in tests:
        try:
            test()
            print("-" * 40)
            time.sleep(1)
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to API. Make sure the server is running on localhost:8000")
            break
        except Exception as e:
            print(f"❌ Test failed: {e}")
            print("-" * 40)

if __name__ == "__main__":
    main()