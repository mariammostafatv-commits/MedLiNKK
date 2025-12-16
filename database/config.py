"""
Database configuration and connection management
Supports SQLite (development) and MySQL (production)
Location: database/config.py
"""
import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Database configuration
DB_TYPE = os.getenv('DB_TYPE', 'sqlite')  # 'sqlite' or 'mysql'

# SQLite configuration (default for development)
SQLITE_DB_PATH = PROJECT_ROOT / 'data' / 'medlink.db'

# MySQL configuration (for production)
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER', 'medlink'),
    'password': os.getenv('MYSQL_PASSWORD', 'medlink123'),
    'database': os.getenv('MYSQL_DATABASE', 'medlink_db'),
}


def get_database_url():
    """
    Get database connection URL based on DB_TYPE
    
    Returns:
        str: SQLAlchemy database URL
    """
    if DB_TYPE == 'mysql':
        # MySQL connection string
        return (
            f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}"
            f"@{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}"
            f"?charset=utf8mb4"
        )
    else:
        # SQLite connection string (default)
        # Ensure data directory exists
        SQLITE_DB_PATH.parent.mkdir(exist_ok=True)
        return f"sqlite:///{SQLITE_DB_PATH}"


# Database URL
DATABASE_URL = get_database_url()

# SQLAlchemy engine configuration
ENGINE_CONFIG = {
    'echo': False,  # Set to True for SQL query logging
    'pool_pre_ping': True,  # Verify connections before using
    'pool_recycle': 3600,  # Recycle connections after 1 hour
}

# SQLite specific settings
if DB_TYPE == 'sqlite':
    ENGINE_CONFIG['connect_args'] = {'check_same_thread': False}

# Session configuration
SESSION_CONFIG = {
    'autocommit': False,
    'autoflush': False,
}