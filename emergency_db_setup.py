"""
EMERGENCY DATABASE RECREATION
Force recreate database with correct schema

Run: python emergency_db_setup.py
"""

import sys
from pathlib import Path

print("="*70)
print("  EMERGENCY DATABASE RECREATION")
print("="*70)
print()

try:
    # Import database components
    from core.database import engine, Base
    from core.models import *
    from sqlalchemy import text, inspect
    
    print("✅ Imports successful")
    print()
    
    # Step 1: Drop all tables
    print("🗑️  Dropping all existing tables...")
    try:
        Base.metadata.drop_all(engine)
        print("   ✅ All tables dropped")
    except Exception as e:
        print(f"   ⚠️  Error dropping tables: {e}")
        print("   (This is OK if tables don't exist)")
    
    print()
    
    # Step 2: Create all tables
    print("🔨 Creating tables with new schema...")
    try:
        Base.metadata.create_all(engine)
        print("   ✅ All tables created")
    except Exception as e:
        print(f"   ❌ Error creating tables: {e}")
        sys.exit(1)
    
    print()
    
    # Step 3: Verify tables
    print("🔍 Verifying tables...")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    expected_tables = [
        'users', 'doctors', 'patients',
        'allergies', 'chronic_diseases', 'current_medications',
        'surgeries', 'hospitalizations', 'vaccinations',
        'family_history', 'disabilities', 'emergency_directives',
        'lifestyle', 'insurance', 'visits', 'prescriptions',
        'vital_signs', 'lab_results', 'imaging_results',
        'nfc_cards', 'doctor_cards', 'patient_cards',
        'hardware_audit_logs'
    ]
    
    for table in expected_tables:
        if table in tables:
            print(f"   ✅ {table}")
        else:
            print(f"   ❌ {table} - MISSING!")
    
    print()
    print(f"Total tables created: {len(tables)}")
    
    # Step 4: Verify user_id column in users table
    print()
    print("🔍 Checking users table schema...")
    columns = inspector.get_columns('users')
    column_names = [col['name'] for col in columns]
    
    if 'user_id' in column_names:
        print("   ✅ users.user_id exists")
    else:
        print("   ❌ users.user_id MISSING!")
        print(f"   Available columns: {column_names}")
    
    print()
    print("="*70)
    print("  DATABASE RECREATION COMPLETE")
    print("="*70)
    print()
    print("Next steps:")
    print("1. Clear cache:")
    print("   rmdir /s /q core\\__pycache__")
    print("   rmdir /s /q database\\__pycache__")
    print()
    print("2. Populate with sample data:")
    print("   python database\\db_manager.py setup")
    print()
    print("3. Test app:")
    print("   python main.py")
    print()
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print()
    print("Make sure:")
    print("1. models.py is in core/ directory")
    print("2. database.py is in core/ directory")
    print("3. All imports are correct")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
