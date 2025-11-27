"""Test patient data loading"""
# from core.patient_manager import patient_manager


# Test loading patient data
national_id = "29501012345678"
patient = patient_manager.get_patient_by_id(national_id)

print(f"Testing patient data for: {national_id}")
print(f"Patient found: {patient is not None}")

if patient:
    print(f"Name: {patient.get('full_name')}")
    print(f"Age: {patient.get('age')}")
    print(f"Blood Type: {patient.get('blood_type')}")
    print(f"Allergies: {patient.get('allergies')}")
    print("✅ Patient data loaded successfully!")
else:
    print("❌ ERROR: Patient data not found!")
    print("Please run: python tests/generate_test_data.py")