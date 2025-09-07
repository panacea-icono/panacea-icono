#!/usr/bin/env python3
"""
🧪 Test Deployment Features
Test the new deployment workflow endpoints and features
"""

import requests
import json
from typing import Dict, Any
import asyncio
import uvicorn
from main import app
import subprocess
import time
import signal
import os

def test_deployment_endpoints():
    """Test all deployment endpoints"""
    print("🧪 Testing PANACEA ICONO Deployment Features")
    print("=" * 50)
    
    # Start FastAPI server in background
    print("🚀 Starting test server...")
    proc = subprocess.Popen([
        'python3', '-c', 
        'import uvicorn; from main import app; uvicorn.run(app, host="0.0.0.0", port=8002, log_level="error")'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Wait for server to start
    time.sleep(3)
    
    base_url = "http://localhost:8002"
    
    # Test endpoints
    endpoints = {
        "Root": "/",
        "Health Check": "/health", 
        "App Info": "/info",
        "Environments": "/deploy/environments",
        "Production Status": "/deploy/status/production",
        "Development Status": "/deploy/status/development",
        "Deployment Links": "/deploy/links",
        "Projections": "/deploy/projections",
        "Production Objectives": "/deploy/objectives/production",
        "Releases": "/deploy/releases",
        "Tags": "/deploy/tags",
        "Packages": "/deploy/packages"
    }
    
    results = {}
    success_count = 0
    
    for name, endpoint in endpoints.items():
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: {endpoint}")
                results[name] = {"status": "success", "data": response.json()}
                success_count += 1
            else:
                print(f"❌ {name}: {endpoint} (HTTP {response.status_code})")
                results[name] = {"status": "error", "code": response.status_code}
        except Exception as e:
            print(f"❌ {name}: {endpoint} (Error: {str(e)[:50]})")
            results[name] = {"status": "error", "error": str(e)}
    
    print("\n📊 Test Results Summary:")
    print(f"✅ Successful: {success_count}/{len(endpoints)}")
    print(f"❌ Failed: {len(endpoints) - success_count}/{len(endpoints)}")
    
    # Test POST endpoint (Gist creation)
    print("\n🧪 Testing POST endpoints...")
    try:
        gist_data = {
            "description": "Test deployment gist",
            "files": {
                "deployment.md": "# Test deployment info\nThis is a test gist."
            },
            "public": True
        }
        response = requests.post(f"{base_url}/deploy/gist", json=gist_data, timeout=5)
        if response.status_code == 200:
            print("✅ Gist Creation: /deploy/gist")
            success_count += 1
        else:
            print(f"❌ Gist Creation: /deploy/gist (HTTP {response.status_code})")
    except Exception as e:
        print(f"❌ Gist Creation: /deploy/gist (Error: {str(e)[:50]})")
    
    # Cleanup
    proc.terminate()
    proc.wait()
    
    print(f"\n🎯 Final Score: {success_count}/{len(endpoints) + 1} endpoints working")
    
    # Show sample data from successful endpoints
    print("\n📝 Sample Response Data:")
    for name, result in results.items():
        if result["status"] == "success" and name in ["Environments", "Deployment Links"]:
            print(f"\n{name}:")
            print(json.dumps(result["data"], indent=2)[:300] + "...")
    
    return success_count >= len(endpoints) * 0.8  # 80% success rate

def test_deployment_models():
    """Test Pydantic models"""
    print("\n🔍 Testing Pydantic Models...")
    
    from main import (
        EnvironmentInfo, DeploymentInfo, GistRequest, 
        LinkInfo, ProjectionData
    )
    from datetime import datetime
    
    try:
        # Test EnvironmentInfo
        env = EnvironmentInfo(
            name="test",
            status="active",
            url="https://test.com",
            objectives=["Testing", "Validation"]
        )
        print("✅ EnvironmentInfo model")
        
        # Test DeploymentInfo
        deploy = DeploymentInfo(
            environment="test",
            status="healthy",
            timestamp=datetime.utcnow(),
            version="1.0.0"
        )
        print("✅ DeploymentInfo model")
        
        # Test GistRequest
        gist = GistRequest(
            description="Test gist",
            files={"test.md": "content"},
            public=True
        )
        print("✅ GistRequest model")
        
        # Test LinkInfo
        link = LinkInfo(
            name="Test Link",
            url="https://example.com",
            category="test",
            description="Test description"
        )
        print("✅ LinkInfo model")
        
        # Test ProjectionData
        projection = ProjectionData(
            metric="test_metric",
            current_value=10.0,
            projected_value=15.0,
            timeframe="next_month"
        )
        print("✅ ProjectionData model")
        
        return True
        
    except Exception as e:
        print(f"❌ Model validation error: {e}")
        return False

def main():
    """Run all tests"""
    print("🏥 PANACEA ICONO Deployment Features Test Suite")
    print("=" * 60)
    
    # Test models
    models_ok = test_deployment_models()
    
    # Test endpoints
    endpoints_ok = test_deployment_endpoints()
    
    print("\n" + "=" * 60)
    print("🎯 Test Summary:")
    print(f"📋 Models: {'✅ PASS' if models_ok else '❌ FAIL'}")
    print(f"🌐 Endpoints: {'✅ PASS' if endpoints_ok else '❌ FAIL'}")
    
    if models_ok and endpoints_ok:
        print("\n🎉 All deployment features working correctly!")
        return True
    else:
        print("\n⚠️  Some features need attention.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)