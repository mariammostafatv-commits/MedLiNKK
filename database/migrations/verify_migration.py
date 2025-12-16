"""
Verify migrated data integrity
Location: database/migrations/verify_migration.py
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_db_context
from database.models import User, Patient, Visit, LabResult, ImagingResult, NFCCard


def verify_migration():
    """Verify that migration was successful"""
    print("\n" + "="*60)
    print("🔍 VERIFYING MIGRATION")
    print("="*60)
    
    try:
        with get_db_context() as db:
            # Count records
            user_count = db.query(User).count()
            patient_count = db.query(Patient).count()
            visit_count = db.query(Visit).count()
            lab_count = db.query(LabResult).count()
            imaging_count = db.query(ImagingResult).count()
            card_count = db.query(NFCCard).count()
            
            print(f"\n📊 Database Record Counts:")
            print(f"  👥 Users: {user_count}")
            print(f"  🏥 Patients: {patient_count}")
            print(f"  🩺 Visits: {visit_count}")
            print(f"  🔬 Lab Results: {lab_count}")
            print(f"  📷 Imaging Results: {imaging_count}")
            print(f"  💳 NFC Cards: {card_count}")
            
            total = user_count + patient_count + visit_count + lab_count + imaging_count + card_count
            print(f"\n  📈 Total Records: {total}")
            
            # Verify relationships
            print(f"\n🔗 Verifying Relationships:")
            
            # Get a patient with visits
            patient_with_visits = db.query(Patient).join(Visit).first()
            if patient_with_visits:
                visits = patient_with_visits.visits
                print(f"  ✅ Patient-Visit relationship: OK ({len(visits)} visits found)")
            else:
                print(f"  ⚠️  No patients with visits found")
            
            # Get a patient with lab results
            patient_with_labs = db.query(Patient).join(LabResult).first()
            if patient_with_labs:
                labs = patient_with_labs.lab_results
                print(f"  ✅ Patient-LabResult relationship: OK ({len(labs)} results found)")
            else:
                print(f"  ⚠️  No patients with lab results found")
            
            # Get a patient with imaging
            patient_with_imaging = db.query(Patient).join(ImagingResult).first()
            if patient_with_imaging:
                imaging = patient_with_imaging.imaging_results
                print(f"  ✅ Patient-Imaging relationship: OK ({len(imaging)} results found)")
            else:
                print(f"  ⚠️  No patients with imaging results found")
            
            # Verify JSON data
            print(f"\n📋 Verifying JSON Data:")
            
            # Check patient with surgeries
            patient_with_surgeries = db.query(Patient).filter(Patient.surgeries.isnot(None)).first()
            if patient_with_surgeries and patient_with_surgeries.surgeries:
                surgery_count = len(patient_with_surgeries.surgeries)
                print(f"  ✅ Surgery data: OK ({surgery_count} surgeries in JSON)")
            else:
                print(f"  ⚠️  No surgery data found")
            
            # Check patient with medications
            patient_with_meds = db.query(Patient).filter(Patient.current_medications.isnot(None)).first()
            if patient_with_meds and patient_with_meds.current_medications:
                med_count = len(patient_with_meds.current_medications)
                print(f"  ✅ Medication data: OK ({med_count} medications in JSON)")
            else:
                print(f"  ⚠️  No medication data found")
            
            # Check patient with family history
            patient_with_family = db.query(Patient).filter(Patient.family_history.isnot(None)).first()
            if patient_with_family and patient_with_family.family_history:
                print(f"  ✅ Family history data: OK")
            else:
                print(f"  ⚠️  No family history data found")
            
            # Sample data verification
            print(f"\n🔍 Sample Data Verification:")
            
            # Show first patient
            first_patient = db.query(Patient).first()
            if first_patient:
                print(f"  Patient: {first_patient.full_name}")
                print(f"  National ID: {first_patient.national_id}")
                print(f"  Blood Type: {first_patient.blood_type}")
                print(f"  Allergies: {first_patient.allergies}")
            
            # Show first visit
            first_visit = db.query(Visit).first()
            if first_visit:
                print(f"\n  Visit: {first_visit.visit_id}")
                print(f"  Patient: {first_visit.patient_national_id}")
                print(f"  Doctor: {first_visit.doctor_name}")
                print(f"  Date: {first_visit.date}")
            
            print(f"\n" + "="*60)
            print("✅ VERIFICATION COMPLETE!")
            print("="*60)
            
            if total > 0:
                print("\n🎉 Migration successful! Database contains data.")
                return True
            else:
                print("\n⚠️  Warning: No data found in database!")
                return False
            
    except Exception as e:
        print(f"\n❌ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = verify_migration()
    sys.exit(0 if success else 1)