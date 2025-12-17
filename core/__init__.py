"""
MedLink Core Module
Database connection and ORM models
"""

from core.database import (
    Base,
    get_db,
    get_db_context,
    # get_engine,
    init_db,
    drop_db,
    test_connection,
    SessionLocal,
    # ScopedSession
)

from core.models import (
    # Main Models
    User,
    Patient,
    Doctor,  # Alias for User
    Surgery,
    Hospitalization,
    Vaccination,
    CurrentMedication,
    Visit,
    Prescription,
    VitalSign,
    LabResult,
    ImagingResult,
    DoctorCard,
    PatientCard,
    NFCCard,
    HardwareAuditLog,
    FamilyHistory,
    
    # Enums
    UserRole,
    Gender,
    BloodType,
    VisitType,
    TestStatus,
    ImagingType,
    CardStatus,
    AccountStatus,
    EventType,
)

__all__ = [
    # Database functions
    'Base',
    'get_db',
    'get_db_context',
    'get_engine',
    'init_db',
    'drop_db',
    'test_connection',
    'SessionLocal',
    'ScopedSession',
    
    # Models
    'User',
    'Patient',
    'Doctor',
    'Surgery',
    'Hospitalization',
    'Vaccination',
    'CurrentMedication',
    'Visit',
    'Prescription',
    'VitalSign',
    'LabResult',
    'ImagingResult',
    'DoctorCard',
    'PatientCard',
    'NFCCard',
    'HardwareAuditLog',
    'Disability',
    
    
    # Enums
    'UserRole',
    'Gender',
    'BloodType',
    'VisitType',
    'TestStatus',
    'ImagingType',
    'CardStatus',
    'AccountStatus',
    'EventType',
]

__version__ = '1.0.0'