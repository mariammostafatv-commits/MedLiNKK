"""
FIXED Database Setup with Test Data
Works with the NEW models.py structure

Location: database/setup_database_with_data.py
"""

from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from core.database import engine, get_db
from core.models import *
from utils.security import hash_password
import random


class DataSeeder:
    """Generate realistic test data for MedLink"""
    
    def __init__(self):
        self.doctors_created = 0
        self.patients_created = 0
        self.cards_created = 0
    
    # ==================== DOCTOR DATA ====================
    
    def create_doctors(self, count=10):
        """Create doctor accounts with NFC cards"""
        
        # Egyptian doctor names
        doctor_names = [
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
            for i, (first, last, spec, hospital) in enumerate(doctor_names[:count], 1):
                try:
                    # Generate national ID (14 digits)
                    national_id = f"280{str(i).zfill(2)}01012{str(i).zfill(4)}"
                    username = f"dr.{first.lower()}.{last.lower()}"
                    
                    # Step 1: Create User account
                    user = User(
                        username=username,
                        password_hash=hash_password('password123'),
                        role=UserRole.doctor,
                        full_name=f"Dr. {first} {last}",
                        email=f"{username}@medlink.com",
                        phone=f"010{random.randint(10000000, 99999999)}",
                        is_active=True,
                        account_status=AccountStatus.active
                    )
                    db.add(user)
                    db.flush()  # Get user_id
                    
                    # Step 2: Create Doctor profile
                    doctor = Doctor(
                        user_id=user.user_id,
                        national_id=national_id,
                        specialization=spec,
                        license_number=f"EG-MED-{random.randint(100000, 999999)}",
                        hospital=hospital,
                        department=spec,
                        years_of_experience=random.randint(5, 25),
                        consultation_fee=random.choice([300, 400, 500, 600]),
                        bio=f"Experienced {spec} specialist with over 10 years of practice."
                    )
                    db.add(doctor)
                    db.flush()
                    
                    # Step 3: Create NFC card
                    card_uid = f"072418{str(i).zfill(4)}"
                    
                    doctor_card = DoctorCard(
                        card_uid=card_uid,
                        user_id=user.user_id,
                        full_name=f"Dr. {first} {last}",
                        specialization=spec,
                        card_type='doctor',
                        status=CardStatus.active,
                        issue_date=date.today(),
                        expiry_date=date.today() + timedelta(days=1825)  # 5 years
                    )
                    db.add(doctor_card)
                    
                    self.doctors_created += 1
                    self.cards_created += 1
                    
                    print(f"   ✅ Created: {username} (Card: {card_uid})")
                    
                except Exception as e:
                    print(f"   ❌ Failed to create doctor {i}: {e}")
                    db.rollback()
                    continue
            
            db.commit()
    
    # ==================== PATIENT DATA ====================
    
    def create_patients(self, count=30):
        """Create patient accounts with NFC cards"""
        
        # Egyptian names
        first_names = [
            "Ahmed", "Mohamed", "Mahmoud", "Ali", "Omar", "Karim",
            "Fatima", "Sara", "Layla", "Nour", "Heba", "Mona",
            "Hassan", "Ibrahim", "Youssef", "Khaled", "Amr",
            "Yasmin", "Dina", "Rana", "Marwa", "Salma"
        ]
        
        last_names = [
            "Hassan", "Ali", "Ibrahim", "Mahmoud", "Said",
            "Khalil", "Youssef", "Abdel", "Mansour", "Farouk"
        ]
        
        with get_db() as db:
            for i in range(1, count + 1):
                try:
                    # Generate patient data
                    first = random.choice(first_names)
                    last = random.choice(last_names)
                    gender = random.choice([Gender.Male, Gender.Female])
                    
                    # Generate national ID (14 digits)
                    year = random.randint(1960, 2005)
                    month = random.randint(1, 12)
                    day = random.randint(1, 28)
                    national_id = f"3{str(year)[2:]}{str(month).zfill(2)}{str(day).zfill(2)}0{random.randint(1000, 9999)}{i % 10}"
                    
                    # Create date of birth
                    dob = date(year, month, day)
                    age = (date.today() - dob).days // 365
                    
                    # Create patient
                    patient = Patient(
                        national_id=national_id,
                        full_name=f"{first} {last}",
                        date_of_birth=dob,
                        age=age,
                        gender=gender,
                        blood_type=random.choice(list(BloodType)),
                        phone=f"011{random.randint(10000000, 99999999)}",
                        email=f"{first.lower()}.{last.lower()}{i}@email.com",
                        address=f"{random.randint(1, 100)} {random.choice(['Tahrir', 'Nasr', 'Heliopolis', 'Maadi', 'Zamalek'])} Street",
                        city="Cairo",
                        governorate="Cairo",
                        emergency_contact={
                            'name': f"{random.choice(first_names)} {random.choice(last_names)}",
                            'relation': random.choice(['Spouse', 'Parent', 'Sibling']),
                            'phone': f"012{random.randint(10000000, 99999999)}"
                        }
                    )
                    db.add(patient)
                    db.flush()
                    
                    # Create NFC card
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
                    
                    # Add some medical history
                    if random.random() > 0.7:  # 30% have allergies
                        allergy = Allergy(
                            patient_national_id=national_id,
                            allergen_name=random.choice(['Penicillin', 'Pollen', 'Dust', 'Nuts']),
                            severity=random.choice(['Mild', 'Moderate', 'Severe']),
                            reaction='Rash, difficulty breathing'
                        )
                        db.add(allergy)
                    
                    if random.random() > 0.8:  # 20% have chronic diseases
                        disease = ChronicDisease(
                            patient_national_id=national_id,
                            disease_name=random.choice(['Diabetes', 'Hypertension', 'Asthma']),
                            date_diagnosed=date.today() - timedelta(days=random.randint(365, 3650)),
                            severity='Controlled'
                        )
                        db.add(disease)
                    
                    self.patients_created += 1
                    self.cards_created += 1
                    
                    if i % 10 == 0:
                        print(f"   ✅ Created {i} patients...")
                    
                except Exception as e:
                    print(f"   ❌ Failed to create patient {i}: {e}")
                    db.rollback()
                    continue
            
            db.commit()
            print(f"   ✅ Total patients created: {self.patients_created}")
    
    # ==================== MAIN SETUP ====================
    
    def create_all(self, doctors=10, patients=30):
        """Create all test data"""
        
        print("\n📋 Creating test data...")
        print()
        
        # Create doctors
        print(f"👨‍⚕️ Creating {doctors} doctors...")
        self.create_doctors(doctors)
        print(f"   ✅ Created {self.doctors_created} doctors")
        print()
        
        # Create patients
        print(f"🧑‍🦱 Creating {patients} patients...")
        self.create_patients(patients)
        print(f"   ✅ Created {self.patients_created} patients")
        print()
        
        print("="*70)
        print("  SUMMARY")
        print("="*70)
        print(f"✅ Doctors: {self.doctors_created}")
        print(f"✅ Patients: {self.patients_created}")
        print(f"✅ NFC Cards: {self.cards_created}")
        print()


def setup_with_data():
    """Main setup function"""
    
    print("="*70)
    print("  MEDLINK DATABASE SETUP WITH TEST DATA")
    print("="*70)
    print()
    
    try:
        # Create tables
        print("📊 Creating database tables...")
        from core.database import Base
        Base.metadata.create_all(engine)
        print("✅ Tables created")
        print()
        
        # Generate test data
        seeder = DataSeeder()
        seeder.create_all(doctors=10, patients=30)
        
        print("="*70)
        print("  ✅ DATABASE SETUP COMPLETE!")
        print("="*70)
        print()
        print("🔑 Default Login Credentials:")
        print("   Username: dr.ahmed.hassan")
        print("   Password: password123")
        print("   NFC Card: 0724184100")
        print()
        print("💡 All doctor passwords: password123")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    setup_with_data()
