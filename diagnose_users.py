"""
Database User Diagnostic Script
Check what users exist and their credentials
"""
import hashlib
from database.models import User
from database.connection import get_db_context
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def check_users():
    """Check all users in database"""
    print("\n" + "="*70)
    print(" "*20 + "🔍 USER DATABASE DIAGNOSTIC")
    print("="*70)

    with get_db_context() as db:
        users = db.query(User).all()

        print(f"\n📊 Total Users: {len(users)}")
        print("\n" + "="*70)

        # Group by role
        doctors = [u for u in users if u.role == 'doctor']
        patients = [u for u in users if u.role == 'patient']
        admins = [u for u in users if u.role == 'admin']
        nurses = [u for u in users if u.role == 'nurse']

        print(f"\n👨‍⚕️  Doctors: {len(doctors)}")
        print(f"👥 Patients: {len(patients)}")
        print(f"👔 Admins: {len(admins)}")
        print(f"👩‍⚕️  Nurses: {len(nurses)}")

        # Show first 5 doctors with usernames
        print("\n" + "="*70)
        print("👨‍⚕️  SAMPLE DOCTORS (First 5):")
        print("="*70)

        for i, doctor in enumerate(doctors[:5], 1):
            print(f"\n{i}. {doctor.full_name}")
            print(f"   Username: {doctor.username}")
            print(f"   Email: {doctor.email}")
            print(f"   Specialization: {doctor.specialization}")
            print(f"   Hospital: {doctor.hospital}")

        # Show first 3 patients
        print("\n" + "="*70)
        print("👥 SAMPLE PATIENTS (First 3):")
        print("="*70)

        for i, patient in enumerate(patients[:3], 1):
            print(f"\n{i}. {patient.full_name}")
            print(f"   Username: {patient.username}")
            print(f"   National ID: {patient.national_id}")

        # Check if specific user exists
        print("\n" + "="*70)
        print("🔍 CHECKING TEST USER: 'dr.ahmed.hassan'")
        print("="*70)

        test_user = db.query(User).filter_by(
            username='dr.ahmed.hassan').first()

        if test_user:
            print(f"\n✅ User found!")
            print(f"   Full Name: {test_user.full_name}")
            print(f"   Username: {test_user.username}")
            print(f"   Role: {test_user.role}")
            print(f"   Password Hash: {test_user.password_hash[:20]}...")

            # Test password
            print("\n🔑 Testing password 'password'...")
            test_hash = hash_password('password')
            print(f"   Expected Hash: {test_hash[:20]}...")
            print(f"   Stored Hash:   {test_user.password_hash[:20]}...")

            if test_user.password_hash == test_hash:
                print("   ✅ Password matches!")
            else:
                print("   ❌ Password doesn't match!")
                print("\n   Trying other common passwords...")

                common_passwords = [
                    'password',
                    'Password123',
                    'ahmed123',
                    '123456',
                    'doctor123'
                ]

                for pwd in common_passwords:
                    test_hash = hash_password(pwd)
                    if test_user.password_hash == test_hash:
                        print(f"   ✅ FOUND! Password is: '{pwd}'")
                        break
        else:
            print("\n❌ User 'dr.ahmed.hassan' NOT FOUND!")
            print("\n💡 Try one of these usernames instead:")

            for i, doctor in enumerate(doctors[:5], 1):
                print(f"   {i}. {doctor.username}")

        print("\n" + "="*70)

        # Suggest correct username/password
        print("\n💡 SUGGESTED TEST CREDENTIALS:")
        print("="*70)

        if doctors:
            first_doctor = doctors[0]
            print(f"\nUsername: {first_doctor.username}")
            print(f"Password: [testing with 'password']")

            # Test if password works for this user
            test_hash = hash_password('password')
            if first_doctor.password_hash == test_hash:
                print(
                    f"✅ Password 'password' works for {first_doctor.username}!")
            else:
                print(f"⚠️  Password 'password' doesn't work")
                print(f"    Actual hash: {first_doctor.password_hash}")


if __name__ == "__main__":
    check_users()
    print("\n" + "="*60)
    print("🔍 USER DATABASE DIAGNOSTIC COMPLETED")