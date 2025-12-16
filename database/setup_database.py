"""
Complete MedLink Database Setup Script
Run this to setup everything automatically
"""

from colorama import Fore, Style, init
from database.database_manager import DatabaseManager
from database.seeder import DataSeeder
from config.database_config import DB_SETTINGS, SEEDER_CONFIG

init(autoreset=True)


def complete_setup():
    """Complete automated database setup"""
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🏥 MedLink Complete Database Setup{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    # Step 1: Database Manager
    print(f"{Fore.YELLOW}Step 1: Database Setup{Style.RESET_ALL}")
    manager = DatabaseManager()
    
    if not manager.setup_database(drop_if_exists=DB_SETTINGS.get('drop_if_exists', False)):
        print(f"{Fore.RED}❌ Database setup failed!{Style.RESET_ALL}")
        return False
    
    # Step 2: Data Seeding
    print(f"\n{Fore.YELLOW}Step 2: Data Seeding{Style.RESET_ALL}")
    
    choice = input(f"\n{Fore.CYAN}Seed test data? (Y/n): {Style.RESET_ALL}").strip().lower()
    
    if choice in ['', 'y', 'yes']:
        seeder = DataSeeder()
        seeder.seed_all()
    
    # Step 3: Final Summary
    print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ MedLink Database Ready!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}📌 Next Steps:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}1. Update your application to use the database{Style.RESET_ALL}")
    print(f"{Fore.WHITE}2. Test database connection{Style.RESET_ALL}")
    print(f"{Fore.WHITE}3. Start MedLink application{Style.RESET_ALL}\n")
    
    return True


if __name__ == "__main__":
    complete_setup()