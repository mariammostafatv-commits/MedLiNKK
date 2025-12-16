"""
Master migration script - Runs all migrations in correct order
Location: database/migrations/run_migration.py
"""
import sys
from pathlib import Path
from datetime import datetime
import shutil

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import test_connection
from database.migrations.migrate_users import migrate_users
from database.migrations.migrate_patients import migrate_patients
from database.migrations.migrate_visits import migrate_visits
from database.migrations.migrate_lab_results import migrate_lab_results
from database.migrations.migrate_imaging import migrate_imaging
from database.migrations.migrate_cards import migrate_cards


def create_backup():
    """Create backup of JSON files before migration"""
    print("\n" + "="*60)
    print("💾 CREATING BACKUP")
    print("="*60)
    
    try:
        # Create backup directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = Path(f"data/backup_{timestamp}")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Files to backup
        json_files = [
            'data/users.json',
            'data/patients.json',
            'data/visits.json',
            'data/lab_results.json',
            'data/imaging_results.json',
            'data/cards.json'
        ]
        
        backed_up = 0
        for file_path in json_files:
            if Path(file_path).exists():
                shutil.copy2(file_path, backup_dir)
                print(f"  ✅ Backed up: {file_path}")
                backed_up += 1
            else:
                print(f"  ⏭️  Not found: {file_path}")
        
        print(f"\n✅ Backup complete! {backed_up} files backed up to: {backup_dir}")
        return True, str(backup_dir)
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False, None


def run_all_migrations():
    """
    Run all migrations in the correct order
    
    Order is important:
    1. Users (no dependencies)
    2. Patients (no dependencies)
    3. Visits (depends on patients)
    4. Lab Results (depends on patients)
    5. Imaging Results (depends on patients)
    6. NFC Cards (no dependencies)
    """
    print("\n" + "="*70)
    print(" "*15 + "🚀 MEDLINK DATA MIGRATION")
    print("="*70)
    print("\n📊 This will migrate all JSON data to the database")
    print("   Make sure database is initialized first!")
    print("\n" + "="*70)
    
    # Test database connection
    print("\n📡 Testing database connection...")
    if not test_connection():
        print("\n❌ Migration aborted - database connection failed!")
        return False
    
    # Create backup
    print("\n" + "="*70)
    user_input = input("\n💾 Do you want to create a backup first? (yes/no): ").lower()
    if user_input in ['yes', 'y']:
        backup_success, backup_path = create_backup()
        if not backup_success:
            print("\n⚠️  Backup failed. Continue anyway? (yes/no): ", end='')
            if input().lower() not in ['yes', 'y']:
                print("❌ Migration cancelled")
                return False
    
    # Confirm migration
    print("\n" + "="*70)
    print("⚠️  READY TO MIGRATE")
    print("="*70)
    print("\nThis will:")
    print("  1. Migrate users")
    print("  2. Migrate patients (with full medical history)")
    print("  3. Migrate visits")
    print("  4. Migrate lab results")
    print("  5. Migrate imaging results")
    print("  6. Migrate NFC cards")
    print("\n" + "="*70)
    
    user_input = input("\nProceed with migration? (yes/no): ").lower()
    if user_input not in ['yes', 'y']:
        print("❌ Migration cancelled")
        return False
    
    # Start migration
    start_time = datetime.now()
    print("\n" + "="*70)
    print(f"⏱️  Migration started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    results = []
    total_records = 0
    
    # 1. Migrate Users
    success, message, count = migrate_users()
    results.append(("Users", success, count))
    total_records += count
    if not success:
        print(f"\n⚠️  Warning: {message}")
    
    # 2. Migrate Patients
    success, message, count = migrate_patients()
    results.append(("Patients", success, count))
    total_records += count
    if not success:
        print(f"\n⚠️  Warning: {message}")
    
    # 3. Migrate Visits
    success, message, count = migrate_visits()
    results.append(("Visits", success, count))
    total_records += count
    if not success:
        print(f"\n⚠️  Warning: {message}")
    
    # 4. Migrate Lab Results
    success, message, count = migrate_lab_results()
    results.append(("Lab Results", success, count))
    total_records += count
    if not success:
        print(f"\n⚠️  Warning: {message}")
    
    # 5. Migrate Imaging Results
    success, message, count = migrate_imaging()
    results.append(("Imaging Results", success, count))
    total_records += count
    if not success:
        print(f"\n⚠️  Warning: {message}")
    
    # 6. Migrate NFC Cards
    success, message, count = migrate_cards()
    results.append(("NFC Cards", success, count))
    total_records += count
    if not success:
        print(f"\n⚠️  Warning: {message}")
    
    # End migration
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Summary
    print("\n" + "="*70)
    print(" "*20 + "🎉 MIGRATION SUMMARY")
    print("="*70)
    
    for name, success, count in results:
        status = "✅" if success else "❌"
        print(f"  {status} {name:.<25} {count:>5} records")
    
    print("="*70)
    print(f"  📊 Total Records Migrated: {total_records}")
    print(f"  ⏱️  Duration: {duration:.2f} seconds")
    print(f"  🏁 Completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Check if all successful
    all_success = all(success for _, success, _ in results)
    
    if all_success:
        print("\n✅ ALL MIGRATIONS COMPLETED SUCCESSFULLY!")
        print("\n🎯 Next Steps:")
        print("   1. Verify data in database")
        print("   2. Test desktop GUI (should work without changes)")
        print("   3. Move to Phase 3: Update Core Managers")
        print("\n" + "="*70)
        return True
    else:
        print("\n⚠️  SOME MIGRATIONS HAD ISSUES")
        print("   Check the errors above and retry if needed")
        print("\n" + "="*70)
        return False


if __name__ == "__main__":
    success = run_all_migrations()
    sys.exit(0 if success else 1)