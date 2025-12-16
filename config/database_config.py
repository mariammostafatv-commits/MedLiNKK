"""
Database Configuration for MedLink
Update these settings for your MySQL environment
"""

# MySQL Connection Settings
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # ⚠️ SET YOUR MYSQL ROOT PASSWORD HERE
    'database': 'medlink_db',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': False
}

# Database Settings
DB_SETTINGS = {
    'auto_create': True,           # Automatically create database if not exists
    'auto_migrate': True,          # Automatically run migrations
    'drop_if_exists': False,       # ⚠️ WARNING: Drop database if exists (USE CAREFULLY)
    'import_json_data': True,      # Import existing JSON data files
    'generate_test_data': False,   # Generate fake test data
}

# Data Import Settings
IMPORT_CONFIG = {
    'data_folder': 'data',         # Folder containing JSON files
    'import_users': True,
    'import_patients': True,
    'import_visits': True,
    'import_lab_results': True,
    'import_imaging': True,
    'import_cards': True,
    'import_hardware_log': True,
}

# Test Data Generation Settings (if generate_test_data = True)
SEEDER_CONFIG = {
    'generate_users': 20,          # Number of fake doctors
    'generate_patients': 100,      # Number of fake patients
    'generate_visits': 500,        # Number of fake visits
    'generate_lab_results': 300,   # Number of fake lab results
    'generate_imaging': 200,       # Number of fake imaging results
}

# Backup Settings
BACKUP_CONFIG = {
    'auto_backup': True,           # Backup before destructive operations
    'backup_folder': 'backups',
    'keep_backups': 7,             # Keep last N backups
}