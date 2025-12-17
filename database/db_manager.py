"""
MedLink Database Manager - FIXED VERSION
Works from any directory, handles import issues
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
END = '\033[0m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'='*60}{END}")
    print(f"{BOLD}{BLUE}{text.center(60)}{END}")
    print(f"{BOLD}{BLUE}{'='*60}{END}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{END}")

def print_error(text):
    print(f"{RED}❌ {text}{END}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{END}")

def print_info(text):
    print(f"{BLUE}ℹ️  {text}{END}")

def check_mysql():
    """Check if MySQL is running"""
    import subprocess
    try:
        result = subprocess.run(
            ['mysql', '--version'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except:
        return False

def get_database_config():
    """Get database configuration"""
    # Try to import from config
    try:
        from config.database_config import DATABASE_CONFIG
        return DATABASE_CONFIG
    except ImportError:
        # Ask user for configuration
        print_warning("Config file not found. Let's set it up!")
        
        password = input(f"{BLUE}Enter MySQL root password: {END}")
        
        return {
            'host': 'localhost',
            'user': 'root',
            'password': password,
            'database': 'medlink_db',
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'autocommit': False
        }

def save_database_config(config):
    """Save database configuration to file"""
    config_dir = project_root / 'config'
    config_dir.mkdir(exist_ok=True)
    
    # Create __init__.py
    init_file = config_dir / '__init__.py'
    if not init_file.exists():
        init_file.write_text('"""Config Package"""\n')
    
    # Create database_config.py
    config_file = config_dir / 'database_config.py'
    content = f'''"""
Database Configuration
"""

DATABASE_CONFIG = {{
    'host': '{config['host']}',
    'user': '{config['user']}',
    'password': '{config['password']}',
    'database': '{config['database']}',
    'charset': '{config['charset']}',
    'collation': '{config['collation']}',
    'autocommit': False
}}

# Database Settings
DB_SETTINGS = {{
    'auto_create': True,
    'auto_migrate': True,
    'drop_if_exists': False,
    'import_json_data': True,
    'generate_test_data': False
}}
'''
    config_file.write_text(content)
    print_success(f"Configuration saved to {config_file}")

def test_connection():
    """Test database connection"""
    try:
        from core.database import test_connection as test_conn
        return test_conn()
    except Exception as e:
        print_error(f"Connection test failed: {e}")
        return False

def create_database():
    """Create the database"""
    print_info("Creating database...")
    import subprocess
    
    # Get configuration
    config = get_database_config()
    password = config['password']
    
    if password == 'password':
        print_error("Please set your MySQL password!")
        password = input(f"{BLUE}Enter MySQL root password: {END}")
        config['password'] = password
        save_database_config(config)
    
    # Create database command
    create_db_sql = f"CREATE DATABASE IF NOT EXISTS {config['database']} CHARACTER SET {config['charset']} COLLATE {config['collation']};"
    
    try:
        # Try using mysql command
        cmd = ['mysql', '-u', config['user'], f'-p{password}', '-e', create_db_sql]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success("Database created successfully")
            return True
        else:
            # Try using python mysql connector
            try:
                import mysql.connector
                conn = mysql.connector.connect(
                    host=config['host'],
                    user=config['user'],
                    password=password
                )
                cursor = conn.cursor()
                cursor.execute(create_db_sql)
                cursor.close()
                conn.close()
                print_success("Database created successfully")
                return True
            except Exception as e:
                print_error(f"Failed to create database: {e}")
                return False
    except Exception as e:
        print_error(f"Error creating database: {e}")
        return False

def create_tables():
    """Create all tables"""
    print_info("Creating tables...")
    try:
        from core.database import init_db
        init_db()
        print_success("Tables created successfully")
        return True
    except Exception as e:
        print_error(f"Failed to create tables: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_test_data(doctors=10, patients=30):
    """Generate test data"""
    print_info(f"Generating test data ({doctors} doctors, {patients} patients)...")
    try:
        # Check if setup script exists
        setup_script = project_root / 'database' / 'setup_database_with_data.py'
        if not setup_script.exists():
            setup_script = project_root / 'setup_database_with_data.py'
        
        if setup_script.exists():
            # Import and run
            import importlib.util
            spec = importlib.util.spec_from_file_location("seeder", setup_script)
            seeder_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(seeder_module)
            
            seeder = seeder_module.DatabaseSeeder()
            seeder.create_all(doctors=doctors, patients=patients)
            return True
        else:
            print_warning("Setup script not found. Creating basic test data...")
            
            # Create basic test data manually
            from core.database import get_db_context
            from core.models import User, Patient, DoctorCard, PatientCard
            import hashlib
            from datetime import date
            
            def hash_password(password):
                return hashlib.sha256(password.encode()).hexdigest()
            
            with get_db_context() as db:
                # Create 1 doctor
                user = User(
                    user_id='DOC001',
                    username='dr.ahmed.hassan',
                    password_hash=hash_password('password123'),
                    role='doctor',
                    full_name='Dr. Ahmed Hassan',
                    email='dr.ahmed@medlink.com',
                    phone='01012345678',
                    national_id='29501011234567',
                    specialization='Cardiology',
                    hospital='Cairo University Hospital',
                    license_number='LIC123456',
                    account_status='active'
                )
                db.add(user)
                
                # Create NFC card for doctor
                doctor_card = DoctorCard(
                    card_uid='0724184100',
                    user_id='DOC001',
                    username='dr.ahmed.hassan',
                    full_name='Dr. Ahmed Hassan',
                    is_active=True
                )
                db.add(doctor_card)
                
                # Create 1 patient
                patient = Patient(
                    national_id='30003150134340',
                    full_name='Ahmed Mohamed',
                    date_of_birth=date(2000, 3, 15),
                    age=24,
                    gender='Male',
                    blood_type='A+',
                    phone='01098765432',
                    email='ahmed@email.com',
                    address='123 Tahrir Street',
                    city='Cairo',
                    governorate='Cairo',
                    emergency_contact={
                        'name': 'Mohamed Ahmed',
                        'phone': '01012345678',
                        'relationship': 'Father'
                    },
                    nfc_card_assigned=True,
                    nfc_card_uid='0725755100',
                    nfc_card_status='active'
                )
                db.add(patient)
                
                # Create NFC card for patient
                patient_card = PatientCard(
                    card_uid='0725755100',
                    national_id='30003150134340',
                    full_name='Ahmed Mohamed',
                    is_active=True
                )
                db.add(patient_card)
                
                db.flush()
            
            print_success("Basic test data created")
            print_info("   Created: 1 doctor, 1 patient")
            print_info("   Doctor: dr.ahmed.hassan / password123")
            print_info("   Doctor Card: 0724184100")
            print_info("   Patient Card: 0725755100")
            
            return True
            
    except Exception as e:
        print_error(f"Failed to generate test data: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_status():
    """Show database status"""
    print_info("Checking database status...")
    
    try:
        from core.database import get_db
        from core.models import User, Patient, DoctorCard, PatientCard, Visit
        
        db = get_db()
        try:
            user_count = db.query(User).count()
            patient_count = db.query(Patient).count()
            doctor_card_count = db.query(DoctorCard).count()
            patient_card_count = db.query(PatientCard).count()
            visit_count = db.query(Visit).count()
            
            print(f"\n{BOLD}Database Status:{END}")
            print(f"   Doctors: {user_count}")
            print(f"   Patients: {patient_count}")
            print(f"   Doctor Cards: {doctor_card_count}")
            print(f"   Patient Cards: {patient_card_count}")
            print(f"   Visits: {visit_count}")
            
            # Show sample credentials
            if user_count > 0:
                users = db.query(User).filter(User.role == 'doctor').limit(5).all()
                print(f"\n{BOLD}Sample Login Credentials:{END}")
                for user in users:
                    print(f"   Username: {user.username} / Password: password123")
                
                # Show NFC cards
                cards = db.query(DoctorCard).limit(3).all()
                if cards:
                    print(f"\n{BOLD}Sample NFC Cards:{END}")
                    for card in cards:
                        print(f"   Card UID: {card.card_uid} - {card.full_name}")
            
        finally:
            db.close()
        
        return True
    except Exception as e:
        print_error(f"Failed to get status: {e}")
        import traceback
        traceback.print_exc()
        return False

def reset_database():
    """Reset database (DELETE ALL DATA!)"""
    print_warning("⚠️  WARNING: This will DELETE ALL DATA!")
    confirm = input(f"{YELLOW}Type 'yes' to continue: {END}")
    
    if confirm.lower() != 'yes':
        print_info("Cancelled")
        return False
    
    print_info("Resetting database...")
    try:
        from core.database import drop_db, init_db
        drop_db()
        init_db()
        print_success("Database reset successfully")
        return True
    except Exception as e:
        print_error(f"Failed to reset database: {e}")
        return False

def full_setup():
    """Complete setup from scratch"""
    print_header("MEDLINK DATABASE FULL SETUP")
    
    # Step 1: Check MySQL
    print_info("Step 1: Checking MySQL...")
    if not check_mysql():
        print_error("MySQL not found! Please install MySQL first.")
        print_info("See: INSTALL_MYSQL.md for installation instructions")
        return False
    print_success("MySQL is installed")
    
    # Step 2: Get/Create configuration
    print_info("\nStep 2: Setting up configuration...")
    config = get_database_config()
    save_database_config(config)
    print_success("Configuration ready")
    
    # Step 3: Create database
    print_info("\nStep 3: Creating database...")
    if not create_database():
        print_error("Failed at step 3")
        return False
    
    # Step 4: Test connection
    print_info("\nStep 4: Testing connection...")
    if not test_connection():
        print_error("Failed at step 4 - Check your password")
        return False
    print_success("Connection successful")
    
    # Step 5: Create tables
    print_info("\nStep 5: Creating tables...")
    if not create_tables():
        print_error("Failed at step 5")
        return False
    
    # Step 6: Generate test data
    print_info("\nStep 6: Generating test data...")
    if not generate_test_data(doctors=10, patients=30):
        print_warning("Failed to generate full test data, but basic data created")
    
    # Step 7: Show status
    print_info("\nStep 7: Verifying setup...")
    show_status()
    
    print_success("\n🎉 SETUP COMPLETE!")
    print_info("\nYou can now run: python main.py")
    
    return True

def main_menu():
    """Main menu"""
    while True:
        print_header("MEDLINK DATABASE MANAGER")
        
        print(f"{BOLD}Choose an option:{END}\n")
        print("1. Full Setup (Create database + tables + test data)")
        print("2. Create Tables Only")
        print("3. Generate Test Data")
        print("4. Show Status")
        print("5. Reset Database (DELETE ALL!)")
        print("6. Test Connection")
        print("7. Update Configuration")
        print("0. Exit")
        
        choice = input(f"\n{BLUE}Enter choice (0-7): {END}").strip()
        
        if choice == '0':
            print_info("Goodbye!")
            break
        
        elif choice == '1':
            full_setup()
            input(f"\n{BLUE}Press Enter to continue...{END}")
        
        elif choice == '2':
            create_tables()
            input(f"\n{BLUE}Press Enter to continue...{END}")
        
        elif choice == '3':
            print("\nHow many records do you want?")
            try:
                doctors = int(input(f"{BLUE}Number of doctors (default 10): {END}") or "10")
                patients = int(input(f"{BLUE}Number of patients (default 30): {END}") or "30")
                generate_test_data(doctors=doctors, patients=patients)
            except ValueError:
                print_error("Invalid number!")
            input(f"\n{BLUE}Press Enter to continue...{END}")
        
        elif choice == '4':
            show_status()
            input(f"\n{BLUE}Press Enter to continue...{END}")
        
        elif choice == '5':
            reset_database()
            input(f"\n{BLUE}Press Enter to continue...{END}")
        
        elif choice == '6':
            if test_connection():
                print_success("Connection successful!")
            else:
                print_error("Connection failed!")
            input(f"\n{BLUE}Press Enter to continue...{END}")
        
        elif choice == '7':
            config = get_database_config()
            save_database_config(config)
            input(f"\n{BLUE}Press Enter to continue...{END}")
        
        else:
            print_error("Invalid choice!")
            input(f"\n{BLUE}Press Enter to continue...{END}")


if __name__ == "__main__":
    # Check if running with arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'setup':
            full_setup()
        elif command == 'status':
            show_status()
        elif command == 'reset':
            reset_database()
        elif command == 'test':
            if test_connection():
                print_success("Connection successful!")
                sys.exit(0)
            else:
                print_error("Connection failed!")
                sys.exit(1)
        else:
            print_error(f"Unknown command: {command}")
            print_info("Available commands: setup, status, reset, test")
            sys.exit(1)
    else:
        # Interactive mode
        main_menu()