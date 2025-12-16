"""
Migrate imaging results from JSON to database
Location: database/migrations/migrate_imaging.py
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_db_context
from database.models import ImagingResult


def migrate_imaging(json_file_path: str = 'data/imaging_results.json'):
    """
    Migrate imaging results from JSON file to database
    
    Args:
        json_file_path: Path to imaging_results.json file
    
    Returns:
        (success: bool, message: str, count: int)
    """
    print("\n" + "="*60)
    print("📷 MIGRATING IMAGING RESULTS")
    print("="*60)
    
    try:
        # Load JSON data
        print(f"📖 Reading from: {json_file_path}")
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both formats
        imaging_results_data = data.get('imaging_results', [])
        
        print(f"✅ Found {len(imaging_results_data)} imaging results in JSON")
        
        if not imaging_results_data:
            return True, "No imaging results to migrate", 0
        
        # Migrate to database
        migrated_count = 0
        skipped_count = 0
        
        with get_db_context() as db:
            for result_data in imaging_results_data:
                imaging_id = result_data.get('imaging_id')
                
                # Skip if no imaging_id
                if not imaging_id:
                    print(f"  ⚠️  Skipping record without imaging_id")
                    skipped_count += 1
                    continue
                
                # Check if result already exists
                existing = db.query(ImagingResult).filter_by(imaging_id=imaging_id).first()
                if existing:
                    print(f"  ⏭️  Skipping {imaging_id} (already exists)")
                    skipped_count += 1
                    continue
                
                # Parse date
                result_date = None
                if result_data.get('date'):
                    try:
                        result_date = datetime.strptime(result_data['date'], "%Y-%m-%d").date()
                    except:
                        pass
                
                # Create imaging result object
                imaging_result = ImagingResult(
                    imaging_id=imaging_id,
                    patient_national_id=result_data.get('patient_national_id'),
                    date=result_date,
                    imaging_center=result_data.get('imaging_center'),
                    imaging_type=result_data.get('imaging_type'),
                    body_part=result_data.get('body_part'),
                    
                    # Results
                    findings=result_data.get('findings'),
                    radiologist=result_data.get('radiologist'),
                    
                    # Additional fields
                    external_link=result_data.get('external_link'),
                    images=result_data.get('images', []),
                    ordered_by=result_data.get('ordered_by'),
                    
                    # Timestamps
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                
                # Parse created_at if exists
                if result_data.get('created_at'):
                    try:
                        imaging_result.created_at = datetime.strptime(
                            result_data['created_at'], "%Y-%m-%d %H:%M:%S"
                        )
                    except:
                        pass
                
                db.add(imaging_result)
                print(f"  ✅ {imaging_id}: {imaging_result.imaging_type} - {imaging_result.patient_national_id}")
                migrated_count += 1
        
        print(f"\n✅ Migration complete!")
        print(f"   Migrated: {migrated_count}")
        print(f"   Skipped: {skipped_count}")
        
        return True, f"Successfully migrated {migrated_count} imaging results", migrated_count
        
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
    success, message, count = migrate_imaging()
    sys.exit(0 if success else 1)