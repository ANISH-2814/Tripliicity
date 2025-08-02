#!/usr/bin/env python
"""
Performance test for login and signup functionality
Tests the time taken for user registration and login operations
"""

import os
import sys
import django
import time
from pathlib import Path

# Add project to path
project_root = Path(__file__).resolve().parent / 'Triplicity'
sys.path.append(str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Triplicity.settings')

try:
    django.setup()
    
    from django.test import TestCase, Client
    from django.contrib.auth import get_user_model
    from accounts.forms import SimpleRegistrationForm, SimpleLoginForm
    import uuid
    
    User = get_user_model()
    
    def test_registration_performance():
        """Test registration performance"""
        print("🔄 Testing user registration performance...")
        
        # Create test data
        test_email = f"test_{uuid.uuid4()}@example.com"
        form_data = {
            'email': test_email,
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
        }
        
        # Time the form processing
        start_time = time.time()
        
        form = SimpleRegistrationForm(data=form_data)
        if form.is_valid():
            user = form.save()
            print(f"✅ User created: {user.email}")
        else:
            print(f"❌ Form errors: {form.errors}")
            return False
            
        end_time = time.time()
        registration_time = end_time - start_time
        
        print(f"⏱️  Registration time: {registration_time:.2f} seconds")
        
        # Check if it's under acceptable threshold (should be < 1 second now)
        if registration_time < 1.0:
            print("✅ Registration performance: GOOD (< 1 second)")
            return True
        elif registration_time < 5.0:
            print("⚠️  Registration performance: ACCEPTABLE (< 5 seconds)")
            return True
        else:
            print("❌ Registration performance: POOR (> 5 seconds)")
            return False
    
    def test_login_performance():
        """Test login performance"""
        print("\n🔄 Testing user login performance...")
        
        # Create a test user first
        test_email = f"login_test_{uuid.uuid4()}@example.com"
        user = User.objects.create_user(
            username=test_email,
            email=test_email,
            password='TestPassword123!',
            first_name='Login',
            last_name='Test'
        )
        
        # Test login form processing
        form_data = {
            'username': test_email,
            'password': 'TestPassword123!',
        }
        
        start_time = time.time()
        
        # Create a dummy request object for the form
        class DummyRequest:
            def __init__(self):
                self.session = {}
        
        form = SimpleLoginForm(DummyRequest(), data=form_data)
        if form.is_valid():
            authenticated_user = form.get_user()
            print(f"✅ User authenticated: {authenticated_user.email}")
        else:
            print(f"❌ Login form errors: {form.errors}")
            return False
            
        end_time = time.time()
        login_time = end_time - start_time
        
        print(f"⏱️  Login time: {login_time:.2f} seconds")
        
        # Check if it's under acceptable threshold
        if login_time < 0.5:
            print("✅ Login performance: EXCELLENT (< 0.5 seconds)")
            return True
        elif login_time < 2.0:
            print("✅ Login performance: GOOD (< 2 seconds)")
            return True
        else:
            print("❌ Login performance: POOR (> 2 seconds)")
            return False
    
    def test_email_async_behavior():
        """Test that email sending doesn't block registration"""
        print("\n🔄 Testing asynchronous email behavior...")
        
        # This test verifies that registration completes quickly
        # even if email sending would be slow (in async thread)
        
        test_email = f"async_test_{uuid.uuid4()}@example.com"
        form_data = {
            'email': test_email,
            'first_name': 'Async',
            'last_name': 'Test',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
        }
        
        start_time = time.time()
        
        form = SimpleRegistrationForm(data=form_data)
        if form.is_valid():
            user = form.save()
            # This should complete quickly because email is async
            end_time = time.time()
            async_test_time = end_time - start_time
            
            print(f"⏱️  Registration with async email: {async_test_time:.2f} seconds")
            
            if async_test_time < 1.0:
                print("✅ Async email implementation: WORKING (registration fast)")
                return True
            else:
                print("❌ Async email implementation: NOT WORKING (registration slow)")
                return False
        else:
            print(f"❌ Form errors: {form.errors}")
            return False
    
    # Run all performance tests
    print("🚀 Starting Tripliicity Performance Tests\n")
    
    results = []
    results.append(test_registration_performance())
    results.append(test_login_performance())
    results.append(test_email_async_behavior())
    
    print(f"\n📊 Test Results Summary:")
    print(f"   - Tests passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 All performance tests PASSED! Login/signup performance is optimized.")
    else:
        print("⚠️  Some performance tests FAILED. Further optimization may be needed.")
        
except Exception as e:
    print(f"❌ Error running performance tests: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)