"""
Database connection and session management
Similar to Laravel's DB facade pattern
Location: database/connection.py
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
from database.config import DATABASE_URL, ENGINE_CONFIG, SESSION_CONFIG, DB_TYPE

# Create SQLAlchemy engine
if DB_TYPE == 'sqlite':
    # SQLite specific configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
        echo=ENGINE_CONFIG['echo']
    )
else:
    # MySQL configuration
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=ENGINE_CONFIG['pool_pre_ping'],
        pool_recycle=ENGINE_CONFIG['pool_recycle'],
        echo=ENGINE_CONFIG['echo']
    )

# Create SessionLocal class (similar to Laravel's DB::connection())
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=SESSION_CONFIG['autocommit'],
    autoflush=SESSION_CONFIG['autoflush']
)

# Create Base class for declarative models (similar to Laravel's Model)
Base = declarative_base()


def get_db():
    """
    Database session dependency (for FastAPI)
    Similar to Laravel's DB::transaction()
    
    Usage in FastAPI:
        @app.get("/patients")
        def get_patients(db: Session = Depends(get_db)):
            return db.query(Patient).all()
    
    Usage in managers:
        db = next(get_db())
        try:
            # Your database operations
            db.commit()
        except:
            db.rollback()
            raise
        finally:
            db.close()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager for database sessions (for core managers)
    Similar to Laravel's DB::transaction()
    
    Usage:
        with get_db_context() as db:
            patient = db.query(Patient).filter_by(national_id=id).first()
            # Auto-commits on success, auto-rollback on error
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def init_database():
    """
    Initialize database - create all tables
    Similar to Laravel's php artisan migrate
    """
    from database.models import Base
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database initialized successfully at: {DATABASE_URL}")


def drop_database():
    """
    Drop all tables (use with caution!)
    Similar to Laravel's php artisan migrate:fresh
    """
    from database.models import Base
    Base.metadata.drop_all(bind=engine)
    print("⚠️  All tables dropped!")


def reset_database():
    """
    Drop and recreate all tables
    Similar to Laravel's php artisan migrate:fresh
    """
    drop_database()
    init_database()
    print("✅ Database reset complete!")


# Test database connection
def test_connection():
    """Test database connection"""
    try:
        with get_db_context() as db:
            # Try to execute a simple query (SQLAlchemy 2.0 requires text())
            db.execute(text("SELECT 1"))
            print(f"✅ Database connection successful!")
            print(f"   Database type: {DB_TYPE}")
            print(f"   Database URL: {DATABASE_URL}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False