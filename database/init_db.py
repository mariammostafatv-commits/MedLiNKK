"""
Database initialization script
Creates all tables and tests connection
Location: database/init_db.py
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import init_database, test_connection, reset_database
from config.database_config import DATABASE_URL, DB_TYPE


def main():
    """
    Main initialization function
    """
    print("=" * 60)
    print("🚀 MedLink Database Initialization")
    print("=" * 60)
    print(f"Database Type: {DB_TYPE}")
    print(f"Database URL: {DATABASE_URL}")
    print("=" * 60)
    
    # Test connection first
    print("\n📡 Testing database connection...")
    if not test_connection():
        print("❌ Connection test failed. Please check your database configuration.")
        return False
    
    # Ask user confirmation
    print("\n⚠️  This will create all database tables.")
    choice = input("Do you want to proceed? (yes/no): ").lower()
    
    if choice not in ['yes', 'y']:
        print("❌ Initialization cancelled.")
        return False
    
    # Initialize database
    print("\n🔨 Creating database tables...")
    try:
        init_database()
        print("\n✅ Database initialization completed successfully!")
        print("\n📊 Tables created:")
        print("   - users")
        print("   - patients")
        print("   - visits")
        print("   - lab_results")
        print("   - imaging_results")
        print("   - nfc_cards")
        print("   - hardware_audit_logs")
        print("\n🎉 Ready to migrate data from JSON files!")
        return True
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        return False


def reset():
    """
    Reset database (drop and recreate all tables)
    ⚠️ WARNING: This will delete all data!
    """
    print("=" * 60)
    print("⚠️  DATABASE RESET - ALL DATA WILL BE DELETED!")
    print("=" * 60)
    
    choice = input("Are you ABSOLUTELY sure? Type 'RESET' to confirm: ")
    
    if choice != 'RESET':
        print("❌ Reset cancelled.")
        return False
    
    try:
        reset_database()
        print("\n✅ Database reset completed!")
        return True
    except Exception as e:
        print(f"\n❌ Error during reset: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='MedLink Database Initialization')
    parser.add_argument('--reset', action='store_true', help='Reset database (delete all data)')
    
    args = parser.parse_args()
    
    if args.reset:
        reset()
    else:
        main()