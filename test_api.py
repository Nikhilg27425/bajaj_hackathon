#!/usr/bin/env python3
"""
Test script for the Document Q&A API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8001"

# Bearer token for authentication
BEARER_TOKEN = "3eda6f3ac8aeaebd1954058607902b3759d6cbbf848dec41d470a19263cd7180"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def test_qa_endpoint():
    """Test the main Q&A endpoint"""
    print("\n🔍 Testing Q&A endpoint...")
    
    # Sample request data
    data = {
        "documents": "https://example.com/sample-policy.pdf",
        "questions": [
            "What is the grace period for premium payment?",
            "What is the waiting period for pre-existing diseases?",
            "Does this policy cover maternity expenses?",
            "What is the waiting period for cataract surgery?",
            "Are the medical expenses for an organ donor covered under this policy?"
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/hackrx/run", json=data, headers=headers)
        if response.status_code == 200:
            print("✅ Q&A endpoint passed")
            result = response.json()
            print(f"Number of answers: {len(result.get('answers', []))}")
            for i, answer in enumerate(result.get('answers', []), 1):
                print(f"Q{i}: {answer[:100]}...")
        else:
            print(f"❌ Q&A endpoint failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Q&A endpoint error: {e}")

def test_api_documentation():
    """Test if API documentation is accessible"""
    print("\n🔍 Testing API documentation...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ API documentation accessible")
        else:
            print(f"❌ API documentation not accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ API documentation error: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting API tests...")
    print("=" * 50)
    
    # Wait a moment for the server to be ready
    time.sleep(2)
    
    # Run tests
    test_health_check()
    test_qa_endpoint()
    test_api_documentation()
    
    print("\n" + "=" * 50)
    print("🏁 Tests completed!")

if __name__ == "__main__":
    main() 