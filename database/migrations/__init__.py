"""
Database migrations package
Handles migration from JSON files to database
Location: database/migrations/__init__.py
"""
from database.migrations.migrate_users import migrate_users
from database.migrations.migrate_patients import migrate_patients
from database.migrations.migrate_visits import migrate_visits
from database.migrations.migrate_lab_results import migrate_lab_results
from database.migrations.migrate_imaging import migrate_imaging
from database.migrations.migrate_cards import migrate_cards

__all__ = [
    'migrate_users',
    'migrate_patients', 
    'migrate_visits',
    'migrate_lab_results',
    'migrate_imaging',
    'migrate_cards'
]