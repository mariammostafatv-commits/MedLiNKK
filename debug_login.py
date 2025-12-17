"""
LOGIN DEBUG SCRIPT - Find out why login is failing
Run: python debug_login.py
"""

from core.database import get_db
from core.models import User, Doctor, DoctorCard
from core.auth_manager import auth_manager
from utils.security import hash_password, verify_password

print("="*70)
print("  LOGIN DEBUG - Finding the Issue")
print("="*70)
print()

try:
    with get_db() as db:
        # Step 1: Check if any users exist
        print("1️⃣ Checking database...")
        users = db.query(User).all()
        doctors = db.query(Doctor).all()
        cards = db.query(DoctorCard).all()
        
        print(f"   Users: {len(users)}")
        print(f"   Doctors: {len(doctors)}")
        print(f"   NFC Cards: {len(cards)}")
        print()
        
        if len(users) == 0:
            print("❌ NO USERS FOUND!")
            print("   The database is empty - no test data was created.")
            print()
            print("🔧 FIX: Run this command:")
            print("   python database\\db_manager.py setup")
            print()
            exit(1)
        
        # Step 2: Show first user details
        print("2️⃣ First user in database:")
        first_user = users[0]
        print(f"   Username: {first_user.username}")
        print(f"   Full Name: {first_user.full_name}")
        print(f"   Role: {first_user.role.value}")
        print(f"   Active: {first_user.is_active}")
        print(f"   Password Hash: {first_user.password_hash[:50]}...")
        print()
        
        # Step 3: Test password hashing
        print("3️⃣ Testing password hashing...")
        test_password = "password123"
        test_hash = hash_password(test_password)
        print(f"   Test hash created: {test_hash[:50]}...")
        
        # Check if hashes match format
        db_hash_format = "bcrypt" if first_user.password_hash.startswith("$2") else "sha256"
        test_hash_format = "bcrypt" if test_hash.startswith("$2") else "sha256"
        
        print(f"   Database hash format: {db_hash_format}")
        print(f"   Test hash format: {test_hash_format}")
        
        if db_hash_format != test_hash_format:
            print("   ⚠️  Hash format mismatch!")
            print("   Database was created with different hashing method.")
        print()
        
        # Step 4: Test password verification
        print("4️⃣ Testing password verification...")
        can_verify = verify_password(test_password, first_user.password_hash)
        print(f"   Can verify 'password123': {can_verify}")
        
        if not can_verify:
            print("   ❌ Password verification FAILED!")
            print("   This means the stored hash doesn't match the password.")
            print()
            print("🔧 FIX: Recreate database with matching hash method")
            print("   python database\\db_manager.py setup")
        else:
            print("   ✅ Password verification works!")
        print()
        
        # Step 5: Test authentication with auth_manager
        print("5️⃣ Testing authentication...")
        username = first_user.username
        password = "password123"
        
        print(f"   Testing: {username} / {password}")
        result = auth_manager.authenticate(username, password)
        
        if result['success']:
            print("   ✅ Authentication SUCCESSFUL!")
            print(f"   User: {result['user'].full_name}")
            print(f"   Role: {result['user'].role.value}")
        else:
            print("   ❌ Authentication FAILED!")
            print(f"   Error: {result.get('message', 'Unknown error')}")
            print()
            print("   Possible causes:")
            print("   1. Password hash format mismatch")
            print("   2. auth_manager using wrong verification method")
            print("   3. User account is inactive")
        print()
        
        # Step 6: List all doctor accounts
        print("6️⃣ Available doctor accounts:")
        print()
        for i, user in enumerate(users[:5], 1):
            if user.role == UserRole.doctor:
                print(f"   {i}. Username: {user.username}")
                print(f"      Name: {user.full_name}")
                print(f"      Password: password123")
                
                # Check for NFC card
                doctor = db.query(Doctor).filter(Doctor.user_id == user.user_id).first()
                if doctor:
                    card = db.query(DoctorCard).filter(DoctorCard.user_id == user.user_id).first()
                    if card:
                        print(f"      NFC Card: {card.card_uid}")
                print()
        
        # Step 7: Summary and recommendations
        print("="*70)
        print("  SUMMARY")
        print("="*70)
        print()
        
        if len(users) > 0 and can_verify and result['success']:
            print("✅ EVERYTHING LOOKS GOOD!")
            print()
            print("🔑 Login Credentials:")
            print(f"   Username: {first_user.username}")
            print(f"   Password: password123")
            print()
            print("💡 If login still fails in GUI:")
            print("   1. Check if you're typing username correctly (case-sensitive)")
            print("   2. Make sure password is exactly: password123")
            print("   3. Clear browser cache if using web interface")
            print("   4. Restart the application")
        else:
            print("❌ ISSUES FOUND!")
            print()
            print("🔧 RECOMMENDED FIX:")
            print("   1. Delete database and recreate:")
            print("      python database\\db_manager.py setup")
            print()
            print("   2. Make sure utils/security.py has correct hash_password")
            print()
            print("   3. Run this debug script again:")
            print("      python debug_login.py")
        
        print()

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    print()
    print("🔧 This error usually means:")
    print("   1. Database not created: Run 'python database\\db_manager.py setup'")
    print("   2. Models not matching database schema")
    print("   3. Import errors in core modules")
