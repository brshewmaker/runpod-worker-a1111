#!/usr/bin/env python3
"""
Local test script for RunPod worker validation.
Tests the core handler logic without requiring A1111 to be running.
"""

import sys
import os
sys.path.append('.')

from rp_handler import validate_input, validate_api, validate_payload, extract_scheduler

def test_input_validation():
    """Test input schema validation"""
    print("Testing input validation...")
    
    # Valid input
    valid_job = {
        'input': {
            'api': {
                'method': 'POST',
                'endpoint': 'sdapi/v1/txt2img'
            },
            'payload': {
                'prompt': 'test prompt',
                'steps': 20
            }
        }
    }
    
    result = validate_input(valid_job)
    if 'errors' in result:
        print(f"❌ Valid input failed: {result['errors']}")
        return False
    else:
        print("✅ Valid input passed")
    
    # Invalid input (missing required fields)
    invalid_job = {
        'input': {
            'api': {
                'method': 'POST'
                # missing endpoint
            }
        }
    }
    
    result = validate_input(invalid_job)
    if 'errors' not in result:
        print("❌ Invalid input should have failed")
        return False
    else:
        print("✅ Invalid input correctly rejected")
    
    return True

def test_api_validation():
    """Test API schema validation"""
    print("\nTesting API validation...")
    
    valid_job = {
        'input': {
            'api': {
                'method': 'POST',
                'endpoint': '/sdapi/v1/txt2img'  # Leading slash should be stripped
            }
        }
    }
    
    result = validate_api(valid_job)
    if 'errors' in result:
        print(f"❌ Valid API failed: {result['errors']}")
        return False
    else:
        print("✅ Valid API passed")
        # Check that leading slash was stripped
        if valid_job['input']['api']['endpoint'] == 'sdapi/v1/txt2img':
            print("✅ Leading slash correctly stripped")
        else:
            print("❌ Leading slash not stripped properly")
            return False
    
    return True

def test_scheduler_extraction():
    """Test scheduler extraction from sampler names"""
    print("\nTesting scheduler extraction...")
    
    test_cases = [
        ("DPM++ 2M Karras", "karras", "DPM++ 2M"),
        ("Euler a", None, "Euler a"),
        ("DPM++ SDE Exponential", "exponential", "DPM++ SDE"),
        ("LMS", None, "LMS"),
        ("DPM2 a uniform", "uniform", "DPM2 a")
    ]
    
    for input_val, expected_scheduler, expected_cleaned in test_cases:
        scheduler, cleaned = extract_scheduler(input_val)
        if scheduler == expected_scheduler and cleaned == expected_cleaned:
            print(f"✅ '{input_val}' -> scheduler: {scheduler}, cleaned: '{cleaned}'")
        else:
            print(f"❌ '{input_val}' -> expected scheduler: {expected_scheduler}, cleaned: '{expected_cleaned}', got scheduler: {scheduler}, cleaned: '{cleaned}'")
            return False
    
    return True

def test_payload_validation():
    """Test payload validation for different endpoints"""
    print("\nTesting payload validation...")
    
    # Test txt2img payload
    txt2img_job = {
        'id': 'test-job',
        'input': {
            'api': {
                'method': 'POST',
                'endpoint': 'sdapi/v1/txt2img'
            },
            'payload': {
                'prompt': 'a beautiful landscape',
                'steps': 20,
                'width': 512,
                'height': 512,
                'sampler_name': 'DPM++ 2M Karras'
            }
        }
    }
    
    endpoint, method, validated_payload = validate_payload(txt2img_job)
    
    if 'errors' in validated_payload:
        print(f"❌ txt2img validation failed: {validated_payload['errors']}")
        return False
    else:
        print("✅ txt2img payload validation passed")
        # Check if scheduler was extracted
        payload = validated_payload.get('validated_input', validated_payload)
        if 'scheduler' in payload and payload['scheduler'] == 'karras':
            print("✅ Scheduler correctly extracted from sampler_name")
        else:
            print("❌ Scheduler not extracted properly")
            return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Running local validation tests...\n")
    
    tests = [
        test_input_validation,
        test_api_validation, 
        test_scheduler_extraction,
        test_payload_validation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print("Test failed!")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All validation tests passed! Your worker logic is working correctly.")
        print("\n💡 To test with actual A1111:")
        print("   1. Ensure A1111 is running on port 3000")
        print("   2. Run: python3 tests/txt2img.py")
        return True
    else:
        print("❌ Some tests failed. Check the validation logic.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)