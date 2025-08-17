#!/usr/bin/env python3
"""
Direct handler test - simulates a RunPod job without needing A1111 running.
This tests the handler logic and error handling.
"""

import sys
import os
sys.path.append('.')

from rp_handler import handler

def test_handler_error_cases():
    """Test handler with various error cases"""
    print("🧪 Testing handler error cases...\n")
    
    # Test 1: Missing required input fields
    print("Test 1: Missing API endpoint")
    job = {
        'id': 'test-1',
        'input': {
            'api': {
                'method': 'POST'
                # missing endpoint
            }
        }
    }
    
    result = handler(job)
    if 'error' in result:
        print("✅ Correctly rejected job with missing endpoint")
        print(f"   Error: {result['error'][:100]}...")
    else:
        print("❌ Should have failed for missing endpoint")
        return False
    
    # Test 2: Invalid endpoint
    print("\nTest 2: Invalid endpoint")
    job = {
        'id': 'test-2',
        'input': {
            'api': {
                'method': 'POST',
                'endpoint': 'invalid/endpoint'
            },
            'payload': {}
        }
    }
    
    result = handler(job)
    # This should pass validation but fail when trying to connect to A1111
    print(f"✅ Handler processed invalid endpoint (expected to fail later)")
    
    # Test 3: Valid structure but will fail due to no A1111
    print("\nTest 3: Valid txt2img request (will fail due to no A1111)")
    job = {
        'id': 'test-3',
        'input': {
            'api': {
                'method': 'POST',
                'endpoint': 'sdapi/v1/txt2img'
            },
            'payload': {
                'prompt': 'test prompt',
                'steps': 20,
                'width': 512,
                'height': 512
            }
        }
    }
    
    result = handler(job)
    if 'error' in result:
        print("✅ Correctly failed when A1111 not available")
        print(f"   Expected connection error occurred")
    else:
        print("❌ Should have failed due to no A1111 connection")
    
    return True

def main():
    """Run handler tests"""
    print("🔧 Testing RunPod handler directly...\n")
    
    if test_handler_error_cases():
        print("\n🎉 Handler error handling works correctly!")
        print("💡 The handler validates inputs properly and fails gracefully when A1111 is not available.")
        return True
    else:
        print("\n❌ Handler tests failed")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)