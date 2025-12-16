"""
Database Configuration for MedLink
"""

# MySQL Connection Settings
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Set your MySQL root password
    'database': 'medlink_db',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

# Database Settings
DB_SETTINGS = {
    'auto_create': True,      # Automatically create database if not exists
    'auto_migrate': True,     # Automatically run migrations
    'drop_if_exists': False,  # WARNING: Drop database if exists (USE CAREFULLY)
}

# Seeder Settings
SEEDER_CONFIG = {
    'generate_patients': 50,      # Number of fake patients to generate
    'generate_visits': 200,       # Number of fake visits
    'generate_lab_results': 100,  # Number of fake lab results
    'generate_imaging': 80,       # Number of fake imaging results
    'import_json': True,          # Import existing JSON data
}