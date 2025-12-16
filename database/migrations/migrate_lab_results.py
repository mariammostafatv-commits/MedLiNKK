"""
Migrate lab results from JSON to database
Location: database/migrations/migrate_lab_results.py
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_db_context
from database.models import LabResult


def migrate_lab_results(json_file_path: str = 'data/lab_results.json'):
    """
    Migrate lab results from JSON file to database
    
    Args:
        json_file_path: Path to lab_results.json file
    
    Returns:
        (success: bool, message: str, count: int)
    """
    print("\n" + "="*60)
    print("🔬 MIGRATING LAB RESULTS")
    print("="*60)
    
    try:
        # Load JSON data
        print(f"📖 Reading from: {json_file_path}")
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both formats: {"lab_results": [...]} or {"result_id": ..., "lab_results": [...]}
        lab_results_data = data.get('lab_results', [])
        
        print(f"✅ Found {len(lab_results_data)} lab results in JSON")
        
        if not lab_results_data:
            return True, "No lab results to migrate", 0
        
        # Migrate to database
        migrated_count = 0
        skipped_count = 0
        
        with get_db_context() as db:
            for result_data in lab_results_data:
                result_id = result_data.get('result_id')
                
                # Skip if no result_id
                if not result_id:
                    print(f"  ⚠️  Skipping record without result_id")
                    skipped_count += 1
                    continue
                
                # Check if result already exists
                existing = db.query(LabResult).filter_by(result_id=result_id).first()
                if existing:
                    print(f"  ⏭️  Skipping {result_id} (already exists)")
                    skipped_count += 1
                    continue
                
                # Parse date
                result_date = None
                if result_data.get('date'):
                    try:
                        result_date = datetime.strptime(result_data['date'], "%Y-%m-%d").date()
                    except:
                        pass
                
                # Create lab result object
                lab_result = LabResult(
                    result_id=result_id,
                    patient_national_id=result_data.get('patient_national_id'),
                    date=result_date,
                    lab_name=result_data.get('lab_name'),
                    test_type=result_data.get('test_type'),
                    status=result_data.get('status', 'completed'),
                    
                    # JSON fields
                    results=result_data.get('results', {}),
                    
                    # Additional fields
                    notes=result_data.get('notes'),
                    external_link=result_data.get('external_link'),
                    attachment=result_data.get('attachment'),
                    ordered_by=result_data.get('ordered_by'),
                    
                    # Timestamps
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                
                # Parse created_at if exists
                if result_data.get('created_at'):
                    try:
                        lab_result.created_at = datetime.strptime(
                            result_data['created_at'], "%Y-%m-%d %H:%M:%S"
                        )
                    except:
                        pass
                
                db.add(lab_result)
                print(f"  ✅ {result_id}: {lab_result.test_type} - {lab_result.patient_national_id}")
                migrated_count += 1
        
        print(f"\n✅ Migration complete!")
        print(f"   Migrated: {migrated_count}")
        print(f"   Skipped: {skipped_count}")
        
        return True, f"Successfully migrated {migrated_count} lab results", migrated_count
        
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
    success, message, count = migrate_lab_results()
    sys.exit(0 if success else 1)