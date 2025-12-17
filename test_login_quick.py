"""
QUICK LOGIN TEST - Show me the correct credentials
Run: python test_login_quick.py
"""

from core.database import get_db
from core.models import User, UserRole
from core.auth_manager import auth_manager

print("="*60)
print("  QUICK LOGIN TEST")
print("="*60)
print()

try:
    with get_db() as db:
        # Get all doctor users
        doctors = db.query(User).filter(User.role == UserRole.doctor).all()
        
        if not doctors:
            print("❌ NO DOCTORS FOUND IN DATABASE!")
            print()
            print("The database is empty. Run this to create test data:")
            print("   python database\\db_manager.py setup")
            print()
            exit(1)
        
        print(f"✅ Found {len(doctors)} doctors in database")
        print()
        
        # Test login with first doctor
        first_doctor = doctors[0]
        username = first_doctor.username
        password = "password123"
        
        print("🧪 Testing authentication...")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        print()
        
        result = auth_manager.authenticate(username, password)
        
        if result['success']:
            print("✅ AUTHENTICATION SUCCESSFUL!")
            print()
            print("🔑 USE THESE CREDENTIALS:")
            print(f"   Username: {username}")
            print(f"   Password: password123")
            print()
            print("📋 All available doctors:")
            for i, doc in enumerate(doctors[:5], 1):
                print(f"   {i}. {doc.username} / password123")
        else:
            print("❌ AUTHENTICATION FAILED!")
            print(f"   Error: {result.get('message', 'Unknown')}")
            print()
            print("This means password hashing is broken.")
            print("Run: python database\\db_manager.py setup")
        
        print()

except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("Run: python database\\db_manager.py setup")
