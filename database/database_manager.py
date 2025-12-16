"""
Complete Database Manager for MedLink
Handles database creation, migrations, and operations
"""

import mysql.connector
from mysql.connector import Error
from colorama import Fore, Style, init
from pathlib import Path
import sys

# Import from our modules
from database.schema import DatabaseSchema
from config.database_config import *

init(autoreset=True)


class DatabaseManager:
    """Complete database management for MedLink"""
    
    def __init__(self, config=None):
        """
        Initialize Database Manager
        
        Args:
            config (dict): Database configuration (optional)
        """
        self.config = config or DATABASE_CONFIG
        self.db_name = self.config['database']
        self.connection = None
        self.cursor = None
        
    def connect(self, use_database=True):
        """
        Connect to MySQL server
        
        Args:
            use_database (bool): Whether to connect to specific database
            
        Returns:
            bool: True if successful
        """
        try:
            config = self.config.copy()
            if not use_database:
                config.pop('database', None)
            
            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor(dictionary=True)
            return True
        except Error as e:
            print(f"{Fore.RED}❌ Connection Error: {e}{Style.RESET_ALL}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def database_exists(self):
        """Check if database exists"""
        try:
            if not self.connect(use_database=False):
                return False
            
            self.cursor.execute("SHOW DATABASES LIKE %s", (self.db_name,))
            result = self.cursor.fetchone()
            self.disconnect()
            
            return result is not None
        except Error as e:
            print(f"{Fore.RED}❌ Error checking database: {e}{Style.RESET_ALL}")
            return False
    
    def create_database(self, drop_if_exists=False):
        """
        Create database
        
        Args:
            drop_if_exists (bool): Drop database if it exists
            
        Returns:
            bool: True if successful
        """
        try:
            print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}📊 Database Creation{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
            
            if not self.connect(use_database=False):
                return False
            
            # Check if exists
            if self.database_exists() and drop_if_exists:
                print(f"{Fore.YELLOW}⚠️  Database '{self.db_name}' exists - Dropping...{Style.RESET_ALL}")
                self.cursor.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
                print(f"{Fore.GREEN}✅ Database dropped{Style.RESET_ALL}\n")
            elif self.database_exists():
                print(f"{Fore.GREEN}✅ Database '{self.db_name}' already exists{Style.RESET_ALL}")
                self.disconnect()
                return True
            
            # Create database
            print(f"{Fore.YELLOW}🔄 Creating database '{self.db_name}'...{Style.RESET_ALL}")
            
            charset = self.config.get('charset', 'utf8mb4')
            collation = self.config.get('collation', 'utf8mb4_unicode_ci')
            
            create_query = f"""
            CREATE DATABASE {self.db_name}
            CHARACTER SET {charset}
            COLLATE {collation}
            """
            
            self.cursor.execute(create_query)
            print(f"{Fore.GREEN}✅ Database '{self.db_name}' created successfully{Style.RESET_ALL}\n")
            
            self.disconnect()
            return True
            
        except Error as e:
            print(f"{Fore.RED}❌ Error creating database: {e}{Style.RESET_ALL}")
            return False
    
    def create_tables(self):
        """
        Create all tables from schema
        
        Returns:
            bool: True if successful
        """
        try:
            print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}🏗️  Table Creation{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
            
            if not self.connect():
                return False
            
            # Get all table schemas in correct order
            tables = DatabaseSchema.get_all_tables()
            
            created_count = 0
            for table_name, create_query in tables.items():
                try:
                    print(f"{Fore.YELLOW}🔄 Creating table '{table_name}'...{Style.RESET_ALL}")
                    self.cursor.execute(create_query)
                    print(f"{Fore.GREEN}✅ Table '{table_name}' created{Style.RESET_ALL}\n")
                    created_count += 1
                except Error as e:
                    print(f"{Fore.RED}❌ Error creating table '{table_name}': {e}{Style.RESET_ALL}\n")
            
            self.connection.commit()
            self.disconnect()
            
            print(f"{Fore.GREEN}✅ Created {created_count}/{len(tables)} tables successfully{Style.RESET_ALL}\n")
            return created_count > 0
            
        except Error as e:
            print(f"{Fore.RED}❌ Error creating tables: {e}{Style.RESET_ALL}")
            return False
    
    def get_table_info(self, table_name):
        """
        Get information about a table
        
        Args:
            table_name (str): Name of the table
            
        Returns:
            dict: Table information
        """
        try:
            if not self.connect():
                return None
            
            # Get column information
            self.cursor.execute(f"DESCRIBE {table_name}")
            columns = self.cursor.fetchall()
            
            # Get row count
            self.cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = self.cursor.fetchone()['count']
            
            self.disconnect()
            
            return {
                'name': table_name,
                'columns': columns,
                'row_count': count
            }
        except Error as e:
            print(f"{Fore.RED}❌ Error getting table info: {e}{Style.RESET_ALL}")
            return None
    
    def print_database_status(self):
        """Print complete database status"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 Database Status{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        # Check if database exists
        if not self.database_exists():
            print(f"{Fore.RED}❌ Database '{self.db_name}' does not exist{Style.RESET_ALL}\n")
            return
        
        print(f"{Fore.GREEN}✅ Database: {self.db_name}{Style.RESET_ALL}\n")
        
        # Get all tables
        try:
            if not self.connect():
                return
            
            self.cursor.execute("SHOW TABLES")
            tables = [list(row.values())[0] for row in self.cursor.fetchall()]
            
            if not tables:
                print(f"{Fore.YELLOW}⚠️  No tables found{Style.RESET_ALL}\n")
                self.disconnect()
                return
            
            print(f"{Fore.CYAN}Tables:{Style.RESET_ALL}\n")
            
            total_rows = 0
            for table in tables:
                info = self.get_table_info(table)
                if info:
                    column_count = len(info['columns'])
                    row_count = info['row_count']
                    total_rows += row_count
                    print(f"{Fore.WHITE}  • {table:.<30} {column_count} cols, {row_count:>8,} rows{Style.RESET_ALL}")
            
            print(f"\n{Fore.GREEN}  Total Tables: {len(tables)}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}  Total Records: {total_rows:,}{Style.RESET_ALL}\n")
            
            self.disconnect()
            
        except Error as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
    
    def setup_database(self, drop_if_exists=False):
        """
        Complete database setup (create database + tables)
        
        Args:
            drop_if_exists (bool): Drop database if exists
            
        Returns:
            bool: True if successful
        """
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🚀 MedLink Database Setup{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        # Step 1: Create database
        if not self.create_database(drop_if_exists):
            print(f"{Fore.RED}❌ Database setup failed{Style.RESET_ALL}\n")
            return False
        
        # Step 2: Create tables
        if not self.create_tables():
            print(f"{Fore.RED}❌ Table creation failed{Style.RESET_ALL}\n")
            return False
        
        # Step 3: Show status
        self.print_database_status()
        
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Database Setup Completed Successfully!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
        
        return True
    
    def execute_query(self, query, params=None, fetch=False):
        """
        Execute a SQL query
        
        Args:
            query (str): SQL query
            params (tuple): Query parameters
            fetch (bool): Whether to fetch results
            
        Returns:
            list/bool: Query results or success status
        """
        try:
            if not self.connect():
                return False if not fetch else []
            
            self.cursor.execute(query, params or ())
            
            if fetch:
                result = self.cursor.fetchall()
                self.disconnect()
                return result
            else:
                self.connection.commit()
                self.disconnect()
                return True
                
        except Error as e:
            print(f"{Fore.RED}❌ Query Error: {e}{Style.RESET_ALL}")
            return False if not fetch else []


def main():
    """CLI interface for database management"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}MedLink Database Manager{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    manager = DatabaseManager()
    
    print(f"{Fore.WHITE}Options:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}1. Setup Database (Create DB + Tables){Style.RESET_ALL}")
    print(f"{Fore.WHITE}2. Create Database Only{Style.RESET_ALL}")
    print(f"{Fore.WHITE}3. Create Tables Only{Style.RESET_ALL}")
    print(f"{Fore.WHITE}4. Show Database Status{Style.RESET_ALL}")
    print(f"{Fore.WHITE}5. Drop and Recreate Database{Style.RESET_ALL}")
    print(f"{Fore.WHITE}6. Exit{Style.RESET_ALL}\n")
    
    choice = input(f"{Fore.CYAN}Choose option (1-6): {Style.RESET_ALL}").strip()
    
    if choice == "1":
        manager.setup_database()
    elif choice == "2":
        manager.create_database()
    elif choice == "3":
        manager.create_tables()
    elif choice == "4":
        manager.print_database_status()
    elif choice == "5":
        confirm = input(f"{Fore.RED}⚠️  This will delete all data! Continue? (yes/no): {Style.RESET_ALL}").strip().lower()
        if confirm == "yes":
            manager.setup_database(drop_if_exists=True)
    else:
        print(f"{Fore.GREEN}Exiting...{Style.RESET_ALL}")


if __name__ == "__main__":
    main()