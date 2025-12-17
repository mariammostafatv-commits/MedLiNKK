"""
COMPLETE LOGIN DIAGNOSTIC - Find EXACTLY what's wrong
Run: python diagnose_login.py
"""

from core.database import get_db, text
from core.models import User, Doctor, DoctorCard, UserRole
from utils.security import hash_password, verify_password
import traceback

print("="*70)
print("  COMPLETE LOGIN DIAGNOSTIC")
print("="*70)
print()

# Test 1: Check database connection
print("1️⃣ Testing database connection...")
try:
    with get_db() as db:
        result = db.execute(text("SELECT 1")).scalar()
        print("   ✅ Database connection works")
except Exception as e:
    print(f"   ❌ Database connection failed: {e}")
    exit(1)

print()

# Test 2: Check if users table exists and has data
print("2️⃣ Checking users table...")
try:
    with get_db() as db:
        count = db.query(DoctorCard).count()
        print(f"   Total users in database: {count}")
        
        if count == 0:
            print("   ❌ NO USERS FOUND!")
            print("   The database is empty.")
            print()
            print("   🔧 FIX: Run this command:")
            print("      python database\\db_manager.py setup")
            print()
            exit(1)
        else:
            print("   ✅ Users exist")
except Exception as e:
    print(f"   ❌ Error checking users: {e}")
    exit(1)

print()

# Test 3: Check password hashing
print("3️⃣ Testing password hashing...")
try:
    test_password = "password123"
    hashed = hash_password(test_password)
    print(f"   Created hash: {hashed[:60]}...")
    
    # Test verification
    can_verify = verify_password(test_password, hashed)
    print(f"   Can verify: {can_verify}")
    
    if not can_verify:
        print("   ❌ Password hashing is BROKEN!")
        print("   utils/security.py has issues")
        exit(1)
    else:
        print("   ✅ Password hashing works")
except Exception as e:
    print(f"   ❌ Password hashing error: {e}")
    traceback.print_exc()
    exit(1)

print()

# Test 4: Check first user details
print("4️⃣ Checking first user in database...")
try:
    with get_db() as db:
        first_user = db.query(User).filter(User.role == UserRole.doctor).first()
        
        if not first_user:
            print("   ❌ No doctor users found!")
            exit(1)
        
        print(f"   Username: {first_user.username}")
        print(f"   Full Name: {first_user.full_name}")
        print(f"   Role: {first_user.role.value}")
        print(f"   Active: {first_user.is_active}")
        print(f"   Password Hash: {first_user.password_hash[:60]}...")
        print()
        
        # Test password verification with database hash
        print("   Testing password verification with database hash...")
        test_result = verify_password("password123", first_user.password_hash)
        print(f"   verify_password('password123', database_hash): {test_result}")
        
        if not test_result:
            print()
            print("   ❌ PROBLEM FOUND!")
            print("   The password hash in the database doesn't match!")
            print()
            print("   This means:")
            print("   1. Database was created with different hashing method")
            print("   2. Or hash_password() changed")
            print()
            print("   🔧 FIX: Recreate database")
            print("      python database\\db_manager.py setup")
        else:
            print("   ✅ Password verification works!")
            
except Exception as e:
    print(f"   ❌ Error: {e}")
    traceback.print_exc()
    exit(1)

print()

# Test 5: Test auth_manager.authenticate()
print("5️⃣ Testing auth_manager.authenticate()...")
try:
    from core.auth_manager import auth_manager
    
    username = first_user.username
    password = "password123"
    
    print(f"   Testing: {username} / {password}")
    result = auth_manager.authenticate(username, password)
    
    print(f"   Success: {result.get('success', False)}")
    print(f"   Message: {result.get('message', 'N/A')}")
    
    if result['success']:
        print("   ✅ auth_manager.authenticate() works!")
    else:
        print("   ❌ auth_manager.authenticate() FAILED!")
        print()
        print("   Debugging authenticate() method...")
        
        # Manual step-by-step test
        with get_db() as db:
            user = db.query(User).filter(User.username == username).first()
            if user:
                print(f"   - User found: {user.username}")
                print(f"   - User active: {user.is_active}")
                print(f"   - Password hash matches: {verify_password(password, user.password_hash)}")
            else:
                print("   - User NOT found in database!")
                
except Exception as e:
    print(f"   ❌ Error: {e}")
    traceback.print_exc()

print()

# Test 6: Test auth_manager.login()
print("6️⃣ Testing auth_manager.login()...")
try:
    from core.auth_manager import auth_manager
    
    username = first_user.username
    password = "password123"
    
    print(f"   Testing: {username} / {password}")
    success, message, user_data = auth_manager.login(username, password)
    
    print(f"   Success: {success}")
    print(f"   Message: {message}")
    
    if success:
        print("   ✅ auth_manager.login() works!")
    else:
        print("   ❌ auth_manager.login() FAILED!")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    traceback.print_exc()

print()

# Summary
print("="*70)
print("  SUMMARY")
print("="*70)
print()

if count > 0 and test_result and result.get('success'):
    print("✅ EVERYTHING WORKS!")
    print()
    print("🔑 Login Credentials:")
    print(f"   Username: {first_user.username}")
    print(f"   Password: password123")
    print()
    print("💡 If login STILL fails in GUI:")
    print("   1. Make sure you copied auth_manager.py to core/")
    print("   2. Clear cache: rmdir /s /q core\\__pycache__")
    print("   3. Restart application")
    print("   4. Type username EXACTLY as shown above")
    print("   5. Type password EXACTLY: password123")
else:
    print("❌ ISSUES FOUND!")
    print()
    print("🔧 RECOMMENDED FIX:")
    print()
    print("1. Make sure all files are in place:")
    print("   - utils/security.py has hash_password() and verify_password()")
    print("   - core/auth_manager.py has authenticate() and login() methods")
    print("   - database/setup_database_with_data.py is fixed")
    print()
    print("2. Recreate database:")
    print("   python database\\db_manager.py setup")
    print()
    print("3. Run this diagnostic again:")
    print("   python diagnose_login.py")

print()
