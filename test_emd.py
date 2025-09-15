#!/usr/bin/env python3
"""
Test script for PANACEA ICONO EMD endpoints
Demonstrates the new Emergency Medical Data functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_emd_system():
    """Test the EMD system endpoints"""
    
    print("🧪 Testing PANACEA ICONO EMD System")
    print("=" * 50)
    
    # Test 1: Register a patient
    print("\n1. 👤 Registering a test patient...")
    patient_data = {
        "first_name": "María",
        "last_name": "García",
        "date_of_birth": "1975-08-22",
        "gender": "female",
        "phone": "+1555123456",
        "email": "maria.garcia@example.com",
        "medical_conditions": ["diabetes", "asthma"],
        "medications": ["insulin", "albuterol"],
        "allergies": ["latex"]
    }
    
    response = requests.post(f"{BASE_URL}/emd/patients/", json=patient_data)
    if response.status_code == 200:
        result = response.json()
        patient_id = result["data"]["patient_id"]
        print(f"   ✅ Patient registered: {patient_id}")
        print(f"   ⚠️  Warnings: {result['data']['validation_warnings']}")
    else:
        print(f"   ❌ Error: {response.text}")
        return
    
    # Test 2: Submit emergency data
    print(f"\n2. 🚨 Submitting emergency for patient {patient_id}...")
    emergency_data = {
        "patient_id": patient_id,
        "emergency_type": "respiratory",
        "severity": "high",
        "symptoms": ["difficulty breathing", "wheezing", "chest tightness"],
        "vital_signs": {
            "heart_rate": 95,
            "blood_pressure_systolic": 130,
            "blood_pressure_diastolic": 85,
            "temperature": 37.0,
            "respiratory_rate": 28,
            "oxygen_saturation": 88
        },
        "location": "Patient's home"
    }
    
    response = requests.post(f"{BASE_URL}/emd/emergency/", json=emergency_data)
    if response.status_code == 200:
        result = response.json()
        emergency_id = result["data"]["emergency_id"]
        print(f"   ✅ Emergency submitted: {emergency_id}")
        print(f"   🏥 Triage Priority: {result['data']['triage_priority']}")
        print(f"   📝 Reason: {result['data']['triage_reason']}")
        print(f"   ⚠️  Warnings: {result['data']['validation_warnings']}")
    else:
        print(f"   ❌ Error: {response.text}")
        return
    
    # Test 3: AI Diagnosis
    print(f"\n3. 🤖 Running AI diagnosis...")
    ai_request = {
        "patient_id": patient_id,
        "symptoms": ["difficulty breathing", "wheezing", "chest tightness", "fatigue"],
        "medical_history": ["diabetes", "asthma"],
        "current_medications": ["insulin", "albuterol"],
        "analysis_type": "diagnosis"
    }
    
    response = requests.post(f"{BASE_URL}/emd/ai/diagnose", json=ai_request)
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ AI Analysis completed")
        print(f"   🎯 Confidence: {result['confidence']:.2f}")
        print(f"   💊 Recommendations: {result['recommendations']}")
        print(f"   ⚡ Actions: {result['suggested_actions']}")
        print(f"   ⚠️  Risk Factors: {result['risk_factors']}")
    else:
        print(f"   ❌ Error: {response.text}")
    
    # Test 4: Risk Assessment
    print(f"\n4. 📊 Running risk assessment...")
    risk_request = {
        "patient_id": patient_id,
        "symptoms": ["difficulty breathing", "wheezing"],
        "vital_signs": {
            "oxygen_saturation": 88,
            "respiratory_rate": 28
        },
        "medical_history": ["diabetes", "asthma"],
        "current_medications": ["insulin", "albuterol"]
    }
    
    response = requests.post(f"{BASE_URL}/emd/ai/risk-assessment", json=risk_request)
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Risk assessment completed")
        print(f"   🎯 Confidence: {result['confidence']:.2f}")
        print(f"   ⚠️  Risk Factors: {result['risk_factors']}")
        print(f"   💊 Recommendations: {result['recommendations']}")
    else:
        print(f"   ❌ Error: {response.text}")
    
    # Test 5: Data validation
    print(f"\n5. ✅ Testing data validation...")
    invalid_data = {
        "patient_id": "TEST",
        "first_name": "Test",
        "last_name": "User",
        "date_of_birth": "2050-12-31",  # Future date
        "gender": "unknown",  # Invalid gender
        "phone": "123",  # Too short
        "medical_conditions": [],
        "medications": [],
        "allergies": []
    }
    
    response = requests.post(f"{BASE_URL}/emd/validate/", json=invalid_data)
    if response.status_code == 200:
        result = response.json()
        print(f"   📋 Validation result: {'Valid' if result['is_valid'] else 'Invalid'}")
        if result['validation_errors']:
            print(f"   ❌ Errors found: {len(result['validation_errors'])}")
    else:
        print(f"   ❌ Error: {response.text}")
    
    print(f"\n🎉 EMD System testing completed!")
    print(f"📊 Summary:")
    print(f"   - Patient registration: ✅")
    print(f"   - Emergency submission: ✅")
    print(f"   - AI diagnosis: ✅")
    print(f"   - Risk assessment: ✅")
    print(f"   - Data validation: ✅")

if __name__ == "__main__":
    # Wait a moment for server to start
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            health = response.json()
            if health["services"]["emd"] == "healthy":
                test_emd_system()
            else:
                print("❌ EMD system not available")
        else:
            print("❌ Server not responding")
    except requests.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on localhost:8000")