"""
Database Layer Test Script
Tests database connection and basic operations
Location: database/test_database.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import get_db_context, test_connection
from database.models import User, Patient, Visit
from datetime import date, datetime


def test_phase_1():
    """
    Test Phase 1: Database Foundation
    Tests connection, models, and basic CRUD operations
    """
    print("=" * 60)
    print("🧪 Testing MedLink Database - Phase 1")
    print("=" * 60)
    
    # Test 1: Connection
    print("\n✅ Test 1: Database Connection")
    if not test_connection():
        print("❌ Connection test failed!")
        return False
    
    # Test 2: Create User
    print("\n✅ Test 2: Create User")
    try:
        with get_db_context() as db:
            user = User(
                user_id="TEST001",
                username="test_doctor",
                password_hash="hashed_password",
                role="doctor",
                full_name="Dr. Test Doctor",
                specialization="Cardiology",
                hospital="Test Hospital",
                email="test@hospital.eg"
            )
            db.add(user)
        print("   ✓ User created successfully")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 3: Create Patient
    print("\n✅ Test 3: Create Patient")
    try:
        with get_db_context() as db:
            patient = Patient(
                national_id="30001011111111",
                full_name="Test Patient",
                date_of_birth=date(2000, 1, 1),
                age=24,
                gender="Male",
                blood_type="A+",
                phone="01012345678",
                chronic_diseases=["Asthma"],
                allergies=["Penicillin"],
                current_medications=[
                    {
                        "name": "Ventolin",
                        "dosage": "2 puffs",
                        "frequency": "As needed"
                    }
                ]
            )
            db.add(patient)
        print("   ✓ Patient created successfully")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 4: Query Patient
    print("\n✅ Test 4: Query Patient")
    try:
        with get_db_context() as db:
            patient = db.query(Patient).filter_by(national_id="30001011111111").first()
            if patient:
                print(f"   ✓ Found patient: {patient.full_name}")
                print(f"   ✓ Blood Type: {patient.blood_type}")
                print(f"   ✓ Allergies: {patient.allergies}")
                print(f"   ✓ Medications: {len(patient.current_medications)} items")
            else:
                print("   ✗ Patient not found")
                return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 5: Update Patient
    print("\n✅ Test 5: Update Patient")
    try:
        with get_db_context() as db:
            patient = db.query(Patient).filter_by(national_id="30001011111111").first()
            patient.phone = "01098765432"
            patient.email = "updated@email.com"
        print("   ✓ Patient updated successfully")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 6: Create Visit with Relationship
    print("\n✅ Test 6: Create Visit")
    try:
        with get_db_context() as db:
            visit = Visit(
                visit_id="TEST_VISIT_001",
                patient_national_id="30001011111111",
                date=date.today(),
                time="10:30",
                doctor_id="TEST001",
                doctor_name="Dr. Test Doctor",
                hospital="Test Hospital",
                department="Cardiology",
                visit_type="Consultation",
                chief_complaint="Test complaint",
                diagnosis="Test diagnosis"
            )
            db.add(visit)
        print("   ✓ Visit created successfully")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 7: Query Patient with Visits (Relationship)
    print("\n✅ Test 7: Test Relationships")
    try:
        with get_db_context() as db:
            patient = db.query(Patient).filter_by(national_id="30001011111111").first()
            print(f"   ✓ Patient: {patient.full_name}")
            print(f"   ✓ Total Visits: {len(patient.visits)}")
            if patient.visits:
                visit = patient.visits[0]
                print(f"   ✓ Visit Date: {visit.date}")
                print(f"   ✓ Doctor: {visit.doctor_name}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 8: JSON Column Storage
    print("\n✅ Test 8: JSON Column Storage")
    try:
        with get_db_context() as db:
            patient = db.query(Patient).filter_by(national_id="30001011111111").first()
            
            # Add surgery record
            patient.surgeries = [
                {
                    "surgery_id": "SRG_TEST_001",
                    "date": "2023-05-20",
                    "procedure": "Test Appendectomy",
                    "hospital": "Test Hospital",
                    "surgeon": "Dr. Test Surgeon"
                }
            ]
            
            # Add family history
            patient.family_history = {
                "father": {
                    "alive": True,
                    "age": 60,
                    "medical_conditions": ["Hypertension"]
                },
                "mother": {
                    "alive": True,
                    "age": 58,
                    "medical_conditions": []
                }
            }
        print("   ✓ JSON data stored successfully")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 9: Verify JSON Data
    print("\n✅ Test 9: Verify JSON Data")
    try:
        with get_db_context() as db:
            patient = db.query(Patient).filter_by(national_id="30001011111111").first()
            print(f"   ✓ Surgeries: {len(patient.surgeries)} records")
            print(f"   ✓ Surgery: {patient.surgeries[0]['procedure']}")
            print(f"   ✓ Father's conditions: {patient.family_history['father']['medical_conditions']}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 10: Cleanup
    print("\n✅ Test 10: Cleanup Test Data")
    try:
        with get_db_context() as db:
            # Delete test records
            db.query(Visit).filter_by(visit_id="TEST_VISIT_001").delete()
            db.query(Patient).filter_by(national_id="30001011111111").delete()
            db.query(User).filter_by(user_id="TEST001").delete()
        print("   ✓ Test data cleaned up successfully")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED! Phase 1 is working perfectly!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    # Run tests
    success = test_phase_1()
    
    if success:
        print("\n✅ Ready for Phase 2: Data Migration")
    else:
        print("\n❌ Tests failed. Please check the errors above.")
    
    sys.exit(0 if success else 1)