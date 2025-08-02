#!/usr/bin/env python
"""
Code analysis verification for performance optimizations
Checks that the key performance improvements are present in the code
"""

import re
import sys
from pathlib import Path

def check_file_exists(filepath):
    """Check if file exists"""
    return Path(filepath).exists()

def check_async_email_implementation():
    """Verify asynchronous email implementation"""
    views_file = "Triplicity/accounts/views.py"
    
    if not check_file_exists(views_file):
        return False, "views.py file not found"
    
    with open(views_file, 'r') as f:
        content = f.read()
    
    checks = [
        ("import threading", "Threading import for async email"),
        ("send_welcome_email_async", "Async email method"),
        ("threading.Thread", "Thread creation for email"),
        ("daemon = True", "Daemon thread configuration"),
        ("fail_silently=False", "Proper email error handling"),
        ("logger.error", "Error logging"),
    ]
    
    results = []
    for check, description in checks:
        if check in content:
            results.append(f"✅ {description}: FOUND")
        else:
            results.append(f"❌ {description}: MISSING")
    
    all_found = all(check in content for check, _ in checks)
    return all_found, results

def check_email_configuration():
    """Verify email configuration optimizations"""
    settings_file = "Triplicity/Triplicity/settings.py"
    
    if not check_file_exists(settings_file):
        return False, "settings.py file not found"
    
    with open(settings_file, 'r') as f:
        content = f.read()
    
    checks = [
        ("EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'", "Console email backend for dev"),
        ("EMAIL_TIMEOUT", "Email timeout setting"),
        ("if DEBUG:", "Debug-based email configuration"),
        ("LOGGING", "Logging configuration"),
    ]
    
    results = []
    for check, description in checks:
        if check in content:
            results.append(f"✅ {description}: FOUND")
        else:
            results.append(f"❌ {description}: MISSING")
    
    all_found = all(check in content for check, _ in checks)
    return all_found, results

def check_database_optimizations():
    """Verify database query optimizations"""
    forms_file = "Triplicity/accounts/forms.py"
    
    if not check_file_exists(forms_file):
        return False, "forms.py file not found"
    
    with open(forms_file, 'r') as f:
        content = f.read()
    
    checks = [
        (".only('email')", "Email field optimization"),
        (".only('username', 'email')", "Username field optimization"),
    ]
    
    results = []
    for check, description in checks:
        if check in content:
            results.append(f"✅ {description}: FOUND")
        else:
            results.append(f"❌ {description}: MISSING")
    
    all_found = all(check in content for check, _ in checks)
    return all_found, results

def check_password_optimizations():
    """Verify password hashing optimizations"""
    settings_file = "Triplicity/Triplicity/settings.py"
    
    if not check_file_exists(settings_file):
        return False, "settings.py file not found"
    
    with open(settings_file, 'r') as f:
        content = f.read()
    
    checks = [
        ("PASSWORD_HASHERS", "Password hasher configuration"),
        ("Argon2PasswordHasher", "Optimized password hasher"),
    ]
    
    results = []
    for check, description in checks:
        if check in content:
            results.append(f"✅ {description}: FOUND")
        else:
            results.append(f"❌ {description}: MISSING")
    
    # Check that excessive validators are removed
    if "UserAttributeSimilarityValidator" not in content and "NumericPasswordValidator" not in content:
        results.append("✅ Excessive password validators: REMOVED")
        validators_optimized = True
    else:
        results.append("❌ Excessive password validators: STILL PRESENT")
        validators_optimized = False
    
    hashers_found = all(check in content for check, _ in checks)
    return hashers_found and validators_optimized, results

def main():
    """Run all verification checks"""
    print("🔍 Verifying Performance Optimizations for Tripliicity\n")
    
    tests = [
        ("Asynchronous Email Implementation", check_async_email_implementation),
        ("Email Configuration", check_email_configuration),
        ("Database Query Optimizations", check_database_optimizations),
        ("Password Hashing Optimizations", check_password_optimizations),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"🔄 Checking {test_name}...")
        try:
            success, details = test_func()
            results.append(success)
            
            if isinstance(details, list):
                for detail in details:
                    print(f"   {detail}")
            else:
                print(f"   {details}")
                
            if success:
                print(f"✅ {test_name}: PASSED\n")
            else:
                print(f"❌ {test_name}: FAILED\n")
                
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}\n")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("📊 Verification Summary:")
    print(f"   Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All optimization verifications PASSED!")
        print("   The following performance improvements are implemented:")
        print("   • Asynchronous email sending to prevent blocking")
        print("   • Console email backend for development")
        print("   • Database query optimizations")
        print("   • Optimized password hashing")
        print("   • Proper error handling and logging")
        print("\n💡 Expected performance improvement:")
        print("   • Registration: 3-4 minutes → < 1 second")
        print("   • Login: Should remain fast (< 0.5 seconds)")
        return True
    else:
        print(f"\n⚠️  {total - passed} optimization verification(s) FAILED")
        print("   Some performance improvements may not be properly implemented.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)