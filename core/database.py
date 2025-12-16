"""
Database Connection and Session Management for MedLink
Provides SQLAlchemy engine and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import sys
from pathlib import Path

# Import database configuration
sys.path.append(str(Path(__file__).parent.parent))
from config.database_config import *

# Create SQLAlchemy Base
Base = declarative_base()

# Create database engine
def get_engine():
    """Create and return SQLAlchemy engine"""
    db_url = (
        f"mysql+mysqlconnector://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}"
        f"@{DATABASE_CONFIG['host']}/{DATABASE_CONFIG['database']}"
        f"?charset={DATABASE_CONFIG['charset']}"
    )
    
    engine = create_engine(
        db_url,
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=3600,   # Recycle connections after 1 hour
        echo=False,          # Set to True for SQL query logging
    )
    return engine

# Create session factory
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create thread-safe scoped session
ScopedSession = scoped_session(SessionLocal)


def get_db():
    """
    Get database session
    
    Usage:
        db = get_db()
        try:
            # Use db session
            patient = db.query(Patient).filter_by(national_id="123").first()
        finally:
            db.close()
    
    Returns:
        Session: SQLAlchemy session
    """
    return SessionLocal()


@contextmanager
def get_db_context():
    """
    Context manager for database sessions
    Automatically handles commit/rollback and close
    
    Usage:
        with get_db_context() as db:
            patient = db.query(Patient).filter_by(national_id="123").first()
            # Session automatically commits and closes
    
    Yields:
        Session: SQLAlchemy session
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """
    Initialize database - create all tables
    
    Usage:
        from core.database import init_db
        init_db()
    """
    from database.models import (
        User, Patient, Surgery, Hospitalization, Vaccination,
        CurrentMedication, Visit, Prescription, VitalSign,
        LabResult, ImagingResult, DoctorCard, PatientCard,
        HardwareAuditLog
    )
    
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")


def drop_db():
    """
    Drop all database tables
    ⚠️ WARNING: This will delete all data!
    
    Usage:
        from core.database import drop_db
        drop_db()
    """
    Base.metadata.drop_all(bind=engine)
    print("✅ Database tables dropped")


# Test connection
def test_connection():
    """Test database connection"""
    try:
        db = get_db()
        db.execute("SELECT 1")
        db.close()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False