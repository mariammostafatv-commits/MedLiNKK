"""
Complete MedLink Database Setup Script
Automated setup for MedLink database system

Usage:
    python setup_database_complete.py

This script will:
1. Check MySQL connection
2. Create database
3. Create all tables
4. Import JSON data (optional)
5. Generate test data (optional)
"""

from colorama import Fore, Style, init
from pathlib import Path
import sys

# Import our modules
from database_manager import DatabaseManager
from json_data_importer import JSONDataImporter
from config.database_config import DATABASE_CONFIG, DB_SETTINGS, IMPORT_CONFIG

init(autoreset=True)


class MedLinkDatabaseSetup:
    """Complete automated database setup"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.json_importer = JSONDataImporter(IMPORT_CONFIG.get('data_folder', 'data'))
        
    def print_header(self):
        """Print setup header"""
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'🏥 MedLink Complete Database Setup':^70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    def check_mysql_connection(self):
        """Check if MySQL is accessible"""
        print(f"{Fore.CYAN}Step 1: Checking MySQL Connection{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*70}{Style.RESET_ALL}\n")
        
        try:
            config = DATABASE_CONFIG.copy()
            config.pop('database', None)  # Don't specify database yet
            
            import mysql.connector
            connection = mysql.connector.connect(**config)
            
            if connection.is_connected():
                db_info = connection.get_server_info()
                print(f"{Fore.GREEN}✅ MySQL Server Connected{Style.RESET_ALL}")
                print(f"{Fore.WHITE}   Version: {db_info}{Style.RESET_ALL}")
                print(f"{Fore.WHITE}   Host: {DATABASE_CONFIG['host']}{Style.RESET_ALL}")
                print(f"{Fore.WHITE}   User: {DATABASE_CONFIG['user']}{Style.RESET_ALL}\n")
                connection.close()
                return True
        except Exception as e:
            print(f"{Fore.RED}❌ MySQL Connection Failed!{Style.RESET_ALL}")
            print(f"{Fore.RED}   Error: {e}{Style.RESET_ALL}\n")
            print(f"{Fore.YELLOW}💡 Troubleshooting:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}   1. Make sure MySQL is running{Style.RESET_ALL}")
            print(f"{Fore.WHITE}   2. Check your credentials in database_config.py{Style.RESET_ALL}")
            print(f"{Fore.WHITE}   3. Verify MySQL root password is set correctly{Style.RESET_ALL}\n")
            return False
    
    def setup_database_structure(self):
        """Setup database and tables"""
        print(f"\n{Fore.CYAN}Step 2: Setting Up Database Structure{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*70}{Style.RESET_ALL}\n")
        
        drop_if_exists = DB_SETTINGS.get('drop_if_exists', False)
        
        if drop_if_exists:
            confirm = input(f"{Fore.RED}⚠️  WARNING: This will DELETE existing database! Continue? (yes/no): {Style.RESET_ALL}").strip().lower()
            if confirm != "yes":
                print(f"{Fore.YELLOW}Setup cancelled by user{Style.RESET_ALL}")
                return False
        
        return self.db_manager.setup_database(drop_if_exists=drop_if_exists)
    
    def import_json_data(self):
        """Import data from JSON files"""
        print(f"\n{Fore.CYAN}Step 3: Importing JSON Data{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*70}{Style.RESET_ALL}\n")
        
        if not DB_SETTINGS.get('import_json_data', False):
            print(f"{Fore.YELLOW}⏭️  JSON import disabled in config{Style.RESET_ALL}\n")
            return True
        
        # Check if data folder exists
        data_folder = Path(IMPORT_CONFIG.get('data_folder', 'data'))
        if not data_folder.exists():
            print(f"{Fore.YELLOW}⚠️  Data folder not found: {data_folder}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   Skipping JSON import{Style.RESET_ALL}\n")
            return True
        
        choice = input(f"{Fore.CYAN}Import JSON data? (Y/n): {Style.RESET_ALL}").strip().lower()
        if choice in ['', 'y', 'yes']:
            return self.json_importer.import_all()
        else:
            print(f"{Fore.YELLOW}Skipping JSON import{Style.RESET_ALL}\n")
            return True
    
    def generate_test_data(self):
        """Generate test data"""
        print(f"\n{Fore.CYAN}Step 4: Generating Test Data{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*70}{Style.RESET_ALL}\n")
        
        if not DB_SETTINGS.get('generate_test_data', False):
            print(f"{Fore.YELLOW}⏭️  Test data generation disabled in config{Style.RESET_ALL}\n")
            return True
        
        print(f"{Fore.YELLOW}⚠️  Test data generation not yet implemented{Style.RESET_ALL}")
        print(f"{Fore.WHITE}   You can add this feature later using Faker library{Style.RESET_ALL}\n")
        return True
    
    def print_summary(self):
        """Print final summary"""
        print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'✅ Setup Complete!':^70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}\n")
        
        # Show database status
        self.db_manager.print_database_status()
        
        print(f"{Fore.CYAN}📌 Next Steps:{Style.RESET_ALL}\n")
        print(f"{Fore.WHITE}1. Verify data in your MySQL client{Style.RESET_ALL}")
        print(f"{Fore.WHITE}2. Update your MedLink app to use the database{Style.RESET_ALL}")
        print(f"{Fore.WHITE}3. Test database connections{Style.RESET_ALL}")
        print(f"{Fore.WHITE}4. Start your MedLink application{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}🔧 Useful Commands:{Style.RESET_ALL}\n")
        print(f"{Fore.WHITE}• Check status: python database_manager.py{Style.RESET_ALL}")
        print(f"{Fore.WHITE}• Import data: python json_data_importer.py{Style.RESET_ALL}")
        print(f"{Fore.WHITE}• MySQL shell: mysql -u root -p medlink_db{Style.RESET_ALL}\n")
    
    def run(self):
        """Run complete setup"""
        self.print_header()
        
        # Step 1: Check MySQL connection
        if not self.check_mysql_connection():
            print(f"{Fore.RED}{'='*70}{Style.RESET_ALL}")
            print(f"{Fore.RED}❌ Setup Failed: Cannot connect to MySQL{Style.RESET_ALL}")
            print(f"{Fore.RED}{'='*70}{Style.RESET_ALL}\n")
            return False
        
        # Step 2: Setup database structure
        if not self.setup_database_structure():
            print(f"{Fore.RED}{'='*70}{Style.RESET_ALL}")
            print(f"{Fore.RED}❌ Setup Failed: Database creation error{Style.RESET_ALL}")
            print(f"{Fore.RED}{'='*70}{Style.RESET_ALL}\n")
            return False
        
        # Step 3: Import JSON data
        if not self.import_json_data():
            print(f"{Fore.YELLOW}⚠️  JSON import had errors but continuing...{Style.RESET_ALL}\n")
        
        # Step 4: Generate test data
        self.generate_test_data()
        
        # Final summary
        self.print_summary()
        
        return True


def main():
    """Main entry point"""
    setup = MedLinkDatabaseSetup()
    success = setup.run()
    
    if success:
        print(f"{Fore.GREEN}🎉 Database setup completed successfully!{Style.RESET_ALL}\n")
        sys.exit(0)
    else:
        print(f"{Fore.RED}❌ Database setup failed. Please check errors above.{Style.RESET_ALL}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()