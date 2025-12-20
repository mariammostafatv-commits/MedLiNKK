"""
Check what attributes exist in Patient model
"""

from core.database import get_db
from core.models import Patient
from sqlalchemy import inspect

def check_patient_model():
    """Show all attributes in Patient model"""
    try:
        # Get Patient model attributes
        mapper = inspect(Patient)
        
        print("=" * 80)
        print("PATIENT MODEL ATTRIBUTES:")
        print("=" * 80)
        
        # Get all columns
        for column in mapper.columns:
            print(f"  {column.name:<30} {column.type}")
        
        # Check for specific attributes
        print("\n" + "=" * 80)
        print("CHECKING FOR NEW ATTRIBUTES:")
        print("=" * 80)
        
        new_attrs = [
            'disabilities_special_needs',
            'surgeries',
            'hospitalizations',
            'vaccinations',
            'family_history',
            'dnr_status',
            'organ_donor',
            'power_of_attorney',
            'religious_preferences',
            'smoking_status',
            'alcohol_consumption',
            'exercise_frequency',
            'dietary_preferences'
        ]
        
        for attr in new_attrs:
            exists = hasattr(Patient, attr)
            status = "✅" if exists else "❌"
            print(f"  {status} {attr}")
        
        # Get sample patient
        print("\n" + "=" * 80)
        print("SAMPLE PATIENT DATA:")
        print("=" * 80)
        
        with get_db() as db:
            patient = db.query(Patient).first()
            if patient:
                print(f"  Name: {patient.full_name}")
                print(f"  National ID: {patient.national_id}")
                
                # Try to access each attribute
                for attr in dir(patient):
                    if not attr.startswith('_') and not callable(getattr(patient, attr)):
                        try:
                            value = getattr(patient, attr)
                            if value is not None:
                                print(f"  {attr}: {value}")
                        except:
                            pass
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_patient_model()
