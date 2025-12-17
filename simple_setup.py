"""
SIMPLE DATABASE SETUP - No complex imports
Just run: python simple_setup.py
"""

import sys
from pathlib import Path

# Make sure we're in project root
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("="*70)
print("  SIMPLE DATABASE SETUP")
print("="*70)
print()

try:
    # Import after fixing path
    from core.database import engine, Base, get_db
    from core.models import *
    from utils.security import hash_password
    from datetime import datetime, date, timedelta
    import random
    
    print("✅ Imports successful")
    print()
    
    # Step 1: Drop all tables
    print("🗑️  Dropping existing tables...")
    Base.metadata.drop_all(engine)
    print("   ✅ Tables dropped")
    print()
    
    # Step 2: Create all tables
    print("🔨 Creating tables...")
    Base.metadata.create_all(engine)
    print("   ✅ Tables created")
    print()
    
    # Step 3: Create doctors
    print("👨‍⚕️ Creating 10 doctors...")
    
    doctors_data = [
        ("Ahmed", "Hassan", "Cardiology", "Cairo University Hospital"),
        ("Mohamed", "Ali", "Pediatrics", "Ain Shams Hospital"),
        ("Mahmoud", "Ibrahim", "Orthopedics", "Kasr Al Ainy Hospital"),
        ("Fatima", "Said", "Gynecology", "Al-Azhar Hospital"),
        ("Sara", "Khalil", "Dermatology", "Nasser Institute"),
        ("Omar", "Youssef", "Neurology", "October 6 Hospital"),
        ("Layla", "Abdel", "Ophthalmology", "Maadi Hospital"),
        ("Karim", "Mansour", "Internal Medicine", "Sheikh Zayed Hospital"),
        ("Nour", "Farouk", "Emergency Medicine", "Heliopolis Hospital"),
        ("Heba", "Mahmoud", "Radiology", "Cairo Scan Center")
    ]
    
    with get_db() as db:
        for i, (first, last, spec, hospital) in enumerate(doctors_data, 1):
            # Create User
            user = User(
                username=f"dr.{first.lower()}.{last.lower()}",
                password_hash=hash_password('password123'),
                role=UserRole.doctor,
                full_name=f"Dr. {first} {last}",
                email=f"dr.{first.lower()}.{last.lower()}@medlink.com",
                phone=f"010{random.randint(10000000, 99999999)}",
                is_active=True,
                account_status=AccountStatus.active
            )
            db.add(user)
            db.flush()
            
            # Create Doctor profile
            national_id = f"280{str(i).zfill(2)}01012{str(i).zfill(4)}"
            doctor = Doctor(
                user_id=user.user_id,
                national_id=national_id,
                specialization=spec,
                license_number=f"EG-MED-{random.randint(100000, 999999)}",
                hospital=hospital,
                department=spec,
                years_of_experience=random.randint(5, 25),
                consultation_fee=random.choice([300, 400, 500, 600])
            )
            db.add(doctor)
            db.flush()
            
            # Create NFC Card
            card_uid = f"072418{str(i).zfill(4)}"
            doctor_card = DoctorCard(
                card_uid=card_uid,
                user_id=user.user_id,
                full_name=f"Dr. {first} {last}",
                specialization=spec,
                card_type='doctor',
                status=CardStatus.active,
                issue_date=date.today(),
                expiry_date=date.today() + timedelta(days=1825)
            )
            db.add(doctor_card)
            
            print(f"   ✅ Created: dr.{first.lower()}.{last.lower()} (Card: {card_uid})")
        
        db.commit()
    
    print()
    print("🧑‍🦱 Creating 30 patients...")
    
    first_names = ["Ahmed", "Mohamed", "Mahmoud", "Ali", "Omar", "Karim",
                   "Fatima", "Sara", "Layla", "Nour", "Heba", "Mona"]
    last_names = ["Hassan", "Ali", "Ibrahim", "Mahmoud", "Said", "Khalil"]
    
    with get_db() as db:
        for i in range(1, 31):
            first = random.choice(first_names)
            last = random.choice(last_names)
            gender = random.choice([Gender.Male, Gender.Female])
            
            year = random.randint(1960, 2005)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            national_id = f"3{str(year)[2:]}{str(month).zfill(2)}{str(day).zfill(2)}0{random.randint(1000, 9999)}{i % 10}"
            
            dob = date(year, month, day)
            age = (date.today() - dob).days // 365
            
            patient = Patient(
                national_id=national_id,
                full_name=f"{first} {last}",
                date_of_birth=dob,
                age=age,
                gender=gender,
                blood_type=random.choice(list(BloodType)),
                phone=f"011{random.randint(10000000, 99999999)}",
                email=f"{first.lower()}.{last.lower()}{i}@email.com",
                address=f"{random.randint(1, 100)} Tahrir Street",
                city="Cairo",
                governorate="Cairo",
                emergency_contact={
                    'name': f"{random.choice(first_names)} {random.choice(last_names)}",
                    'relation': 'Family',
                    'phone': f"012{random.randint(10000000, 99999999)}"
                }
            )
            db.add(patient)
            db.flush()
            
            # Create NFC Card
            card_uid = f"072575{str(i).zfill(4)}"
            patient_card = PatientCard(
                card_uid=card_uid,
                patient_national_id=national_id,
                full_name=f"{first} {last}",
                blood_type=patient.blood_type.value,
                card_type='patient',
                status=CardStatus.active,
                issue_date=date.today(),
                expiry_date=date.today() + timedelta(days=1825)
            )
            db.add(patient_card)
            
            if i % 10 == 0:
                print(f"   ✅ Created {i} patients...")
        
        db.commit()
    
    print(f"   ✅ Total: 30 patients created")
    print()
    
    print("="*70)
    print("  ✅ SETUP COMPLETE!")
    print("="*70)
    print()
    print("🔑 Default Login Credentials:")
    print("   Username: dr.ahmed.hassan")
    print("   Password: password123")
    print("   NFC Card: 0724184100")
    print()
    print("💡 All doctor passwords: password123")
    print()
    print("📊 Summary:")
    print("   ✅ 10 Doctors created")
    print("   ✅ 30 Patients created")
    print("   ✅ 40 NFC Cards created")
    print()
    print("🚀 Next steps:")
    print("   1. Test login: python test_login_quick.py")
    print("   2. Run app: python main.py")
    print()
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print()
    print("Make sure you're running from project root:")
    print("   cd D:\\My-Projects\\Python\\Projects\\webscraping\\MedLink")
    print("   python simple_setup.py")
    print()
    print("And make sure these files exist:")
    print("   - core/models.py")
    print("   - core/database.py")
    print("   - utils/security.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
