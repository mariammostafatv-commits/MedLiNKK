"""
Migrate visits from JSON to database
Location: database/migrations/migrate_visits.py
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_db_context
from database.models import Visit


def migrate_visits(json_file_path: str = 'data/visits.json'):
    """
    Migrate visits from JSON file to database
    
    Args:
        json_file_path: Path to visits.json file
    
    Returns:
        (success: bool, message: str, count: int)
    """
    print("\n" + "="*60)
    print("🩺 MIGRATING VISITS")
    print("="*60)
    
    try:
        # Load JSON data
        print(f"📖 Reading from: {json_file_path}")
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        visits_data = data.get('visits', [])
        print(f"✅ Found {len(visits_data)} visits in JSON")
        
        if not visits_data:
            return True, "No visits to migrate", 0
        
        # Migrate to database
        migrated_count = 0
        skipped_count = 0
        
        with get_db_context() as db:
            for visit_data in visits_data:
                visit_id = visit_data.get('visit_id')
                
                # Check if visit already exists
                existing = db.query(Visit).filter_by(visit_id=visit_id).first()
                if existing:
                    print(f"  ⏭️  Skipping {visit_id} (already exists)")
                    skipped_count += 1
                    continue
                
                # Parse date
                visit_date = None
                if visit_data.get('date'):
                    try:
                        visit_date = datetime.strptime(visit_data['date'], "%Y-%m-%d").date()
                    except:
                        pass
                
                # Create visit object
                visit = Visit(
                    visit_id=visit_id,
                    patient_national_id=visit_data.get('patient_national_id'),
                    date=visit_date,
                    time=visit_data.get('time'),
                    
                    # Doctor information
                    doctor_id=visit_data.get('doctor_id'),
                    doctor_name=visit_data.get('doctor_name'),
                    hospital=visit_data.get('hospital'),
                    department=visit_data.get('department'),
                    
                    # Visit details
                    visit_type=visit_data.get('visit_type'),
                    chief_complaint=visit_data.get('chief_complaint'),
                    diagnosis=visit_data.get('diagnosis'),
                    treatment_plan=visit_data.get('treatment_plan'),
                    notes=visit_data.get('notes'),
                    
                    # JSON fields
                    vital_signs=visit_data.get('vital_signs', {}),
                    prescriptions=visit_data.get('prescriptions', []),
                    attachments=visit_data.get('attachments', []),
                    
                    # Timestamps
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                
                # Parse created_at if exists in JSON
                if visit_data.get('created_at'):
                    try:
                        visit.created_at = datetime.strptime(
                            visit_data['created_at'], "%Y-%m-%d %H:%M:%S"
                        )
                    except:
                        pass
                
                db.add(visit)
                print(f"  ✅ {visit_id}: {visit.patient_national_id} - {visit.date} ({visit.visit_type})")
                migrated_count += 1
        
        print(f"\n✅ Migration complete!")
        print(f"   Migrated: {migrated_count}")
        print(f"   Skipped: {skipped_count}")
        
        return True, f"Successfully migrated {migrated_count} visits", migrated_count
        
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
    success, message, count = migrate_visits()
    sys.exit(0 if success else 1)