"""
VERIFY TEST ACCOUNTS - Check all doctors and NFC cards
Run: python verify_test_accounts.py
"""

from core.database import get_db
from core.models import User, Doctor, DoctorCard, PatientCard
from core.auth_manager import auth_manager

print("="*70)
print("  VERIFYING TEST ACCOUNTS")
print("="*70)
print()

try:
    with get_db() as db:
        # Check doctors
        doctors = db.query(Doctor).join(User).all()
        
        print(f"📋 Total Doctors: {len(doctors)}")
        print()
        
        if doctors:
            print("="*70)
            print("  DOCTOR ACCOUNTS")
            print("="*70)
            print()
            
            for i, doctor in enumerate(doctors, 1):
                print(f"👨‍⚕️ Doctor #{i}")
                print(f"   Username: {doctor.user.username}")
                print(f"   Full Name: {doctor.user.full_name}")
                print(f"   Specialization: {doctor.specialization}")
                print(f"   Hospital: {doctor.hospital}")
                print(f"   Password: password123")
                print()
                
                # Check for NFC cards
                cards = db.query(DoctorCard).filter(
                    DoctorCard.user_id == doctor.user.user_id
                ).all()
                
                if cards:
                    for card in cards:
                        print(f"   💳 NFC Card: {card.card_uid}")
                else:
                    print(f"   ⚠️  No NFC card assigned")
                
                print()
        else:
            print("❌ No doctors found in database!")
            print("   Run: python database\\db_manager.py setup")
        
        # Check NFC cards
        print("="*70)
        print("  NFC CARDS")
        print("="*70)
        print()
        
        doctor_cards = db.query(DoctorCard).all()
        print(f"👨‍⚕️ Doctor Cards: {len(doctor_cards)}")
        for card in doctor_cards[:5]:  # Show first 5
            print(f"   Card UID: {card.card_uid} → {card.full_name}")
        
        print()
        
        patient_cards = db.query(PatientCard).all()
        print(f"🧑‍🦱 Patient Cards: {len(patient_cards)}")
        for card in patient_cards[:5]:  # Show first 5
            print(f"   Card UID: {card.card_uid} → {card.full_name}")
        
        print()
        
        # Test login for first doctor
        if doctors:
            print("="*70)
            print("  TESTING LOGIN")
            print("="*70)
            print()
            
            first_doctor = doctors[0]
            username = first_doctor.user.username
            password = "password123"
            
            print(f"Testing login for: {username}")
            print(f"Password: {password}")
            print()
            
            # Test authentication
            result = auth_manager.authenticate(username, password)
            
            if result['success']:
                print("✅ Login SUCCESSFUL!")
                print(f"   User: {result['user'].full_name}")
                print(f"   Role: {result['user'].role.value}")
            else:
                print("❌ Login FAILED!")
                print(f"   Error: {result['message']}")
            
            print()
        
        print("="*70)
        print("  QUICK REFERENCE")
        print("="*70)
        print()
        print("📝 Default Password: password123")
        print()
        print("🔑 First Doctor Login:")
        if doctors:
            print(f"   Username: {doctors[0].user.username}")
            print(f"   Password: password123")
            
            # Get NFC card
            card = db.query(DoctorCard).filter(
                DoctorCard.user_id == doctors[0].user.user_id
            ).first()
            if card:
                print(f"   NFC Card: {card.card_uid}")
        
        print()
        print("💡 To login:")
        print("   1. Username/Password: Use any username above + 'password123'")
        print("   2. NFC Card: Scan any doctor card UID shown above")
        print()

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
