"""
Migrate users from JSON to database
Location: database/migrations/migrate_users.py
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_db_context
from database.models import User


def migrate_users(json_file_path: str = 'data/users.json'):
    """
    Migrate users from JSON file to database
    
    Args:
        json_file_path: Path to users.json file
    
    Returns:
        (success: bool, message: str, count: int)
    """
    print("\n" + "="*60)
    print("👥 MIGRATING USERS")
    print("="*60)
    
    try:
        # Load JSON data
        print(f"📖 Reading from: {json_file_path}")
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        users_data = data.get('users', [])
        print(f"✅ Found {len(users_data)} users in JSON")
        
        if not users_data:
            return True, "No users to migrate", 0
        
        # Migrate to database
        migrated_count = 0
        skipped_count = 0
        
        with get_db_context() as db:
            for user_data in users_data:
                user_id = user_data.get('user_id')
                
                # Check if user already exists
                existing = db.query(User).filter_by(user_id=user_id).first()
                if existing:
                    print(f"  ⏭️  Skipping {user_id} (already exists)")
                    skipped_count += 1
                    continue
                
                # Create user object
                user = User(
                    user_id=user_data.get('user_id'),
                    username=user_data.get('username'),
                    password_hash=user_data.get('password_hash'),
                    role=user_data.get('role'),
                    full_name=user_data.get('full_name'),
                    email=user_data.get('email'),
                    phone=user_data.get('phone'),
                    
                    # Doctor-specific fields
                    specialization=user_data.get('specialization'),
                    hospital=user_data.get('hospital'),
                    license_number=user_data.get('license_number'),
                    
                    # Patient-specific fields
                    national_id=user_data.get('national_id'),
                    
                    # Fingerprint fields
                    fingerprint_id=user_data.get('fingerprint_id'),
                    fingerprint_enrolled=user_data.get('fingerprint_enrolled', False),
                    
                    # Parse date if exists
                    fingerprint_enrollment_date=None,
                    last_fingerprint_login=None,
                    created_at=datetime.now(),
                    last_login=None
                )
                
                # Parse dates if they exist
                if user_data.get('fingerprint_enrollment_date'):
                    try:
                        user.fingerprint_enrollment_date = datetime.strptime(
                            user_data['fingerprint_enrollment_date'], "%Y-%m-%d"
                        ).date()
                    except:
                        pass
                
                if user_data.get('last_fingerprint_login'):
                    try:
                        user.last_fingerprint_login = datetime.strptime(
                            user_data['last_fingerprint_login'], "%Y-%m-%d %H:%M:%S"
                        )
                    except:
                        pass
                
                db.add(user)
                print(f"  ✅ Migrated: {user.username} ({user.role})")
                migrated_count += 1
        
        print(f"\n✅ Migration complete!")
        print(f"   Migrated: {migrated_count}")
        print(f"   Skipped: {skipped_count}")
        
        return True, f"Successfully migrated {migrated_count} users", migrated_count
        
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
    success, message, count = migrate_users()
    sys.exit(0 if success else 1)