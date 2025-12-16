"""
Migrate patients from JSON to database
Location: database/migrations/migrate_patients.py
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_db_context
from database.models import Patient


def migrate_patients(json_file_path: str = 'data/patients.json'):
    """
    Migrate patients from JSON file to database
    
    Args:
        json_file_path: Path to patients.json file
    
    Returns:
        (success: bool, message: str, count: int)
    """
    print("\n" + "="*60)
    print("🏥 MIGRATING PATIENTS")
    print("="*60)
    
    try:
        # Load JSON data
        print(f"📖 Reading from: {json_file_path}")
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        patients_data = data.get('patients', [])
        print(f"✅ Found {len(patients_data)} patients in JSON")
        
        if not patients_data:
            return True, "No patients to migrate", 0
        
        # Migrate to database
        migrated_count = 0
        skipped_count = 0
        
        with get_db_context() as db:
            for patient_data in patients_data:
                national_id = patient_data.get('national_id')
                
                # Check if patient already exists
                existing = db.query(Patient).filter_by(national_id=national_id).first()
                if existing:
                    print(f"  ⏭️  Skipping {national_id} (already exists)")
                    skipped_count += 1
                    continue
                
                # Parse date of birth
                dob = None
                if patient_data.get('date_of_birth'):
                    try:
                        dob = datetime.strptime(patient_data['date_of_birth'], "%Y-%m-%d").date()
                    except:
                        pass
                
                # Create patient object
                patient = Patient(
                    national_id=national_id,
                    full_name=patient_data.get('full_name'),
                    date_of_birth=dob,
                    age=patient_data.get('age'),
                    gender=patient_data.get('gender'),
                    blood_type=patient_data.get('blood_type'),
                    
                    # Contact information
                    phone=patient_data.get('phone'),
                    email=patient_data.get('email'),
                    address=patient_data.get('address'),
                    
                    # Emergency contact (already JSON)
                    emergency_contact=patient_data.get('emergency_contact'),
                    
                    # Medical information (already JSON arrays)
                    chronic_diseases=patient_data.get('chronic_diseases', []),
                    allergies=patient_data.get('allergies', []),
                    current_medications=patient_data.get('current_medications', []),
                    
                    # Insurance (already JSON)
                    insurance=patient_data.get('insurance'),
                    
                    # External links (already JSON)
                    external_links=patient_data.get('external_links', {}),
                    
                    # NFC Card information
                    nfc_card_uid=patient_data.get('nfc_card_uid'),
                    nfc_card_assigned=patient_data.get('nfc_card_assigned', False),
                    nfc_card_type=patient_data.get('nfc_card_type'),
                    nfc_card_status=patient_data.get('nfc_card_status'),
                    nfc_scan_count=patient_data.get('nfc_scan_count', 0),
                    
                    # Complex nested medical records (stored as JSON)
                    surgeries=patient_data.get('surgeries', []),
                    hospitalizations=patient_data.get('hospitalizations', []),
                    vaccinations=patient_data.get('vaccinations', []),
                    family_history=patient_data.get('family_history', {}),
                    disabilities_special_needs=patient_data.get('disabilities_special_needs', {}),
                    emergency_directives=patient_data.get('emergency_directives', {}),
                    lifestyle=patient_data.get('lifestyle', {}),
                    
                    # Timestamps
                    created_at=datetime.now(),
                    last_updated=datetime.now()
                )
                
                # Parse NFC assignment date
                if patient_data.get('nfc_card_assignment_date'):
                    try:
                        patient.nfc_card_assignment_date = datetime.strptime(
                            patient_data['nfc_card_assignment_date'], "%Y-%m-%d"
                        ).date()
                    except:
                        pass
                
                # Parse last NFC scan
                if patient_data.get('nfc_card_last_scan'):
                    try:
                        patient.nfc_card_last_scan = datetime.strptime(
                            patient_data['nfc_card_last_scan'], "%Y-%m-%d %H:%M:%S"
                        )
                    except:
                        pass
                
                db.add(patient)
                
                # Show progress with medical data counts
                surgeries_count = len(patient.surgeries) if patient.surgeries else 0
                hospitalizations_count = len(patient.hospitalizations) if patient.hospitalizations else 0
                vaccinations_count = len(patient.vaccinations) if patient.vaccinations else 0
                
                print(f"  ✅ {patient.full_name}")
                print(f"     ID: {national_id}")
                print(f"     Medical: {surgeries_count} surgeries, {hospitalizations_count} hospitalizations, {vaccinations_count} vaccines")
                
                migrated_count += 1
        
        print(f"\n✅ Migration complete!")
        print(f"   Migrated: {migrated_count}")
        print(f"   Skipped: {skipped_count}")
        
        return True, f"Successfully migrated {migrated_count} patients", migrated_count
        
    except FileNotFoundError:
        error_msg = f"❌ File not found: {json_file_path}"
        print(error_msg)
        return False, error_msg, 0
    
    except Exception as e:
        error_msg = f"❌ Error during migration: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return False, error_msg, 0


if __name__ == "__main__":
    # Run standalone
    success, message, count = migrate_patients()
    sys.exit(0 if success else 1)