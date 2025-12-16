"""
SQLAlchemy ORM Models for MedLink
All database models with relationships
"""

from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, Time, Boolean, 
    Enum, ForeignKey, JSON, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from core.database import Base
import enum


# ==================== ENUMS ====================

class UserRole(enum.Enum):
    """User roles"""
    doctor = "doctor"
    nurse = "nurse"
    admin = "admin"
    staff = "staff"
    patient = "patient"


class Gender(enum.Enum):
    """Gender options"""
    Male = "Male"
    Female = "Female"


class BloodType(enum.Enum):
    """Blood type options"""
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"


class VisitType(enum.Enum):
    """Visit type options"""
    Consultation = "Consultation"
    FollowUp = "Follow-up"
    Emergency = "Emergency"
    Routine = "Routine"


class TestStatus(enum.Enum):
    """Lab/imaging test status"""
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class ImagingType(enum.Enum):
    """Imaging modality types"""
    XRay = "X-Ray"
    CT = "CT"
    MRI = "MRI"
    Ultrasound = "Ultrasound"
    PET = "PET"
    Other = "Other"


class CardStatus(enum.Enum):
    """NFC card status"""
    active = "active"
    inactive = "inactive"
    lost = "lost"
    damaged = "damaged"


class AccountStatus(enum.Enum):
    """User account status"""
    active = "active"
    inactive = "inactive"
    suspended = "suspended"


class EventType(enum.Enum):
    """Hardware event types"""
    fingerprint_login = "fingerprint_login"
    nfc_card_scan = "nfc_card_scan"
    failed_login = "failed_login"
    logout = "logout"
    other = "other"


# ==================== USER MODEL ====================

class User(Base):
    """User model for doctors, staff, and patients"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, index=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(150))
    phone = Column(String(20))
    
    # Doctor-specific fields
    specialization = Column(String(100))
    hospital = Column(String(200))
    license_number = Column(String(50))
    years_experience = Column(Integer)
    
    # Biometric fields
    fingerprint_id = Column(Integer)
    fingerprint_enrolled = Column(Boolean, default=False)
    fingerprint_enrollment_date = Column(Date)
    nfc_card_uid = Column(String(50), index=True)
    biometric_enabled = Column(Boolean, default=False)
    last_fingerprint_login = Column(DateTime)
    fingerprint_login_count = Column(Integer, default=0)
    
    # Patient-specific fields (for patient users)
    national_id = Column(String(14), index=True)
    date_of_birth = Column(Date)
    
    # System fields
    created_at = Column(DateTime, default=func.now())
    last_login = Column(DateTime)
    login_count = Column(Integer, default=0)
    account_status = Column(Enum(AccountStatus), default=AccountStatus.active)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    visits_as_doctor = relationship("Visit", foreign_keys="Visit.doctor_id", back_populates="doctor")
    lab_results_ordered = relationship("LabResult", foreign_keys="LabResult.ordered_by", back_populates="ordered_by_user")
    imaging_results_ordered = relationship("ImagingResult", foreign_keys="ImagingResult.ordered_by", back_populates="ordered_by_user")
    doctor_cards = relationship("DoctorCard", back_populates="user")
    
    def __repr__(self):
        return f"<User(user_id='{self.user_id}', username='{self.username}', role='{self.role.value}')>"
    
    @property
    def is_doctor(self):
        return self.role == UserRole.doctor
    
    @property
    def is_patient(self):
        return self.role == UserRole.patient


# ==================== PATIENT MODEL ====================

class Patient(Base):
    """Patient model with complete medical information"""
    __tablename__ = 'patients'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    national_id = Column(String(14), unique=True, nullable=False, index=True)
    full_name = Column(String(200), nullable=False, index=True)
    date_of_birth = Column(Date, nullable=False)
    age = Column(Integer)
    gender = Column(Enum(Gender), nullable=False)
    blood_type = Column(Enum(BloodType))
    
    # Contact Information
    phone = Column(String(20), index=True)
    email = Column(String(150))
    address = Column(Text)
    city = Column(String(100))
    governorate = Column(String(100))
    
    # JSON Fields for complex data
    emergency_contact = Column(JSON)  # {name, relation, phone}
    chronic_diseases = Column(JSON)  # Array of diseases
    allergies = Column(JSON)  # Array of allergies
    family_history = Column(JSON)  # Complete family medical history
    disabilities_special_needs = Column(JSON)  # Disability information
    emergency_directives = Column(JSON)  # DNR, organ donor, etc.
    lifestyle = Column(JSON)  # Smoking, alcohol, exercise, etc.
    insurance = Column(JSON)  # Insurance information
    external_links = Column(JSON)  # External system links
    
    # NFC Card Information
    nfc_card_uid = Column(String(50), index=True)
    nfc_card_assigned = Column(Boolean, default=False)
    nfc_card_assignment_date = Column(Date)
    nfc_card_type = Column(String(50))
    nfc_card_status = Column(Enum(CardStatus), default=CardStatus.active)
    nfc_card_last_scan = Column(DateTime)
    nfc_scan_count = Column(Integer, default=0)
    
    # System fields
    created_at = Column(DateTime, default=func.now())
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    surgeries = relationship("Surgery", back_populates="patient", cascade="all, delete-orphan")
    hospitalizations = relationship("Hospitalization", back_populates="patient", cascade="all, delete-orphan")
    vaccinations = relationship("Vaccination", back_populates="patient", cascade="all, delete-orphan")
    current_medications = relationship("CurrentMedication", back_populates="patient", cascade="all, delete-orphan")
    visits = relationship("Visit", back_populates="patient", cascade="all, delete-orphan")
    lab_results = relationship("LabResult", back_populates="patient", cascade="all, delete-orphan")
    imaging_results = relationship("ImagingResult", back_populates="patient", cascade="all, delete-orphan")
    patient_cards = relationship("PatientCard", back_populates="patient", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Patient(national_id='{self.national_id}', name='{self.full_name}')>"


# ==================== SURGERY MODEL ====================

class Surgery(Base):
    """Patient surgery records"""
    __tablename__ = 'surgeries'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    surgery_id = Column(String(50), unique=True, nullable=False)
    patient_national_id = Column(String(14), ForeignKey('patients.national_id', ondelete='CASCADE'), nullable=False, index=True)
    surgery_type = Column(String(200), nullable=False)
    surgery_date = Column(Date, nullable=False, index=True)
    surgeon = Column(String(200))
    hospital = Column(String(200))
    reason = Column(Text)
    outcome = Column(Text)
    complications = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="surgeries")
    
    def __repr__(self):
        return f"<Surgery(id='{self.surgery_id}', type='{self.surgery_type}', date='{self.surgery_date}')>"


# ==================== HOSPITALIZATION MODEL ====================

class Hospitalization(Base):
    """Patient hospitalization records"""
    __tablename__ = 'hospitalizations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    hospitalization_id = Column(String(50), unique=True, nullable=False)
    patient_national_id = Column(String(14), ForeignKey('patients.national_id', ondelete='CASCADE'), nullable=False, index=True)
    hospital = Column(String(200), nullable=False)
    admission_date = Column(Date, nullable=False, index=True)
    discharge_date = Column(Date)
    reason = Column(Text)
    diagnosis = Column(Text)
    treatment = Column(Text)
    length_of_stay = Column(Integer)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="hospitalizations")
    
    def __repr__(self):
        return f"<Hospitalization(id='{self.hospitalization_id}', hospital='{self.hospital}')>"


# ==================== VACCINATION MODEL ====================

class Vaccination(Base):
    """Patient vaccination records"""
    __tablename__ = 'vaccinations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_national_id = Column(String(14), ForeignKey('patients.national_id', ondelete='CASCADE'), nullable=False, index=True)
    vaccine_name = Column(String(200), nullable=False, index=True)
    date_administered = Column(Date, nullable=False, index=True)
    dose_number = Column(String(50))
    location = Column(String(200))
    batch_number = Column(String(100))
    next_dose_due = Column(Date)
    administrator = Column(String(200))
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="vaccinations")
    
    def __repr__(self):
        return f"<Vaccination(vaccine='{self.vaccine_name}', date='{self.date_administered}')>"


# ==================== CURRENT MEDICATION MODEL ====================

class CurrentMedication(Base):
    """Patient current medications"""
    __tablename__ = 'current_medications'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_national_id = Column(String(14), ForeignKey('patients.national_id', ondelete='CASCADE'), nullable=False, index=True)
    medication_name = Column(String(200), nullable=False, index=True)
    dosage = Column(String(100))
    frequency = Column(String(100))
    started_date = Column(Date)
    end_date = Column(Date)
    prescribed_by = Column(String(200))
    reason = Column(Text)
    notes = Column(Text)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="current_medications")
    
    def __repr__(self):
        return f"<CurrentMedication(medication='{self.medication_name}', active={self.is_active})>"


# ==================== VISIT MODEL ====================

class Visit(Base):
    """Medical visit records"""
    __tablename__ = 'visits'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    visit_id = Column(String(50), unique=True, nullable=False, index=True)
    patient_national_id = Column(String(14), ForeignKey('patients.national_id', ondelete='CASCADE'), nullable=False, index=True)
    doctor_id = Column(String(50), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    doctor_name = Column(String(200), nullable=False)
    
    visit_date = Column(Date, nullable=False, index=True)
    visit_time = Column(Time)
    hospital = Column(String(200))
    department = Column(String(100))
    visit_type = Column(Enum(VisitType), nullable=False, index=True)
    
    chief_complaint = Column(Text)
    diagnosis = Column(Text)
    treatment_plan = Column(Text)
    notes = Column(Text)
    
    attachments = Column(JSON)  # Array of attachment paths
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="visits")
    doctor = relationship("User", foreign_keys=[doctor_id], back_populates="visits_as_doctor")
    prescriptions = relationship("Prescription", back_populates="visit", cascade="all, delete-orphan")
    vital_signs = relationship("VitalSign", back_populates="visit", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Visit(id='{self.visit_id}', date='{self.visit_date}', type='{self.visit_type.value}')>"


# ==================== PRESCRIPTION MODEL ====================

class Prescription(Base):
    """Prescriptions from visits"""
    __tablename__ = 'prescriptions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    visit_id = Column(String(50), ForeignKey('visits.visit_id', ondelete='CASCADE'), nullable=False, index=True)
    medication = Column(String(200), nullable=False)
    dosage = Column(String(100))
    frequency = Column(String(100))
    duration = Column(String(50))
    instructions = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    visit = relationship("Visit", back_populates="prescriptions")
    
    def __repr__(self):
        return f"<Prescription(medication='{self.medication}', dosage='{self.dosage}')>"


# ==================== VITAL SIGN MODEL ====================

class VitalSign(Base):
    """Vital signs from visits"""
    __tablename__ = 'vital_signs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    visit_id = Column(String(50), ForeignKey('visits.visit_id', ondelete='CASCADE'), nullable=False, index=True)
    blood_pressure = Column(String(20))
    heart_rate = Column(String(20))
    temperature = Column(String(20))
    weight = Column(String(20))
    height = Column(String(20))
    respiratory_rate = Column(String(20))
    oxygen_saturation = Column(String(20))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    visit = relationship("Visit", back_populates="vital_signs")
    
    def __repr__(self):
        return f"<VitalSign(bp='{self.blood_pressure}', hr='{self.heart_rate}')>"


# ==================== LAB RESULT MODEL ====================

class LabResult(Base):
    """Laboratory test results"""
    __tablename__ = 'lab_results'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    result_id = Column(String(50), unique=True, nullable=False, index=True)
    patient_national_id = Column(String(14), ForeignKey('patients.national_id', ondelete='CASCADE'), nullable=False, index=True)
    ordered_by = Column(String(50), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    
    test_date = Column(Date, nullable=False, index=True)
    lab_name = Column(String(200))
    test_type = Column(String(200), nullable=False)
    status = Column(Enum(TestStatus), default=TestStatus.pending, index=True)
    
    results = Column(JSON)  # Test results as key-value pairs
    notes = Column(Text)
    
    external_link = Column(String(500))
    attachment = Column(String(500))
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="lab_results")
    ordered_by_user = relationship("User", foreign_keys=[ordered_by], back_populates="lab_results_ordered")
    
    def __repr__(self):
        return f"<LabResult(id='{self.result_id}', type='{self.test_type}', status='{self.status.value}')>"


# ==================== IMAGING RESULT MODEL ====================

class ImagingResult(Base):
    """Imaging and radiology results"""
    __tablename__ = 'imaging_results'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    imaging_id = Column(String(50), unique=True, nullable=False, index=True)
    patient_national_id = Column(String(14), ForeignKey('patients.national_id', ondelete='CASCADE'), nullable=False, index=True)
    ordered_by = Column(String(50), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    
    imaging_date = Column(Date, nullable=False, index=True)
    imaging_center = Column(String(200))
    imaging_type = Column(Enum(ImagingType), nullable=False, index=True)
    body_part = Column(String(100))
    
    findings = Column(Text)
    radiologist = Column(String(200))
    
    images = Column(JSON)  # Array of image paths
    external_link = Column(String(500))
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="imaging_results")
    ordered_by_user = relationship("User", foreign_keys=[ordered_by], back_populates="imaging_results_ordered")
    
    def __repr__(self):
        return f"<ImagingResult(id='{self.imaging_id}', type='{self.imaging_type.value}', date='{self.imaging_date}')>"


# ==================== NFC CARD MODELS ====================

class DoctorCard(Base):
    """NFC cards for doctors"""
    __tablename__ = 'doctor_cards'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    card_uid = Column(String(50), unique=True, nullable=False, index=True)
    username = Column(String(100), nullable=False)
    user_id = Column(String(50), ForeignKey('users.user_id', ondelete='CASCADE'), index=True)
    full_name = Column(String(200), nullable=False)
    card_type = Column(String(20), default='doctor')
    is_active = Column(Boolean, default=True)
    issued_date = Column(DateTime, default=func.now())
    last_used = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="doctor_cards")
    
    def __repr__(self):
        return f"<DoctorCard(uid='{self.card_uid}', name='{self.full_name}')>"


class PatientCard(Base):
    """NFC cards for patients"""
    __tablename__ = 'patient_cards'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    card_uid = Column(String(50), unique=True, nullable=False, index=True)
    national_id = Column(String(14), ForeignKey('patients.national_id', ondelete='CASCADE'), nullable=False, index=True)
    full_name = Column(String(200), nullable=False)
    card_type = Column(String(20), default='patient')
    is_active = Column(Boolean, default=True)
    issued_date = Column(DateTime, default=func.now())
    last_used = Column(DateTime)
    
    # Relationships
    patient = relationship("Patient", back_populates="patient_cards")
    
    def __repr__(self):
        return f"<PatientCard(uid='{self.card_uid}', name='{self.full_name}')>"


# Convenience class for backward compatibility
class NFCCard:
    """
    Convenience class for NFC card operations
    Can work with both DoctorCard and PatientCard
    """
    
    @staticmethod
    def get_by_uid(db, card_uid):
        """Get card (doctor or patient) by UID"""
        # Try doctor card first
        doctor_card = db.query(DoctorCard).filter_by(card_uid=card_uid).first()
        if doctor_card:
            return doctor_card
        
        # Try patient card
        patient_card = db.query(PatientCard).filter_by(card_uid=card_uid).first()
        return patient_card
    
    @staticmethod
    def is_doctor_card(card):
        """Check if card is a doctor card"""
        return isinstance(card, DoctorCard)
    
    @staticmethod
    def is_patient_card(card):
        """Check if card is a patient card"""
        return isinstance(card, PatientCard)


# ==================== HARDWARE AUDIT LOG ====================

class HardwareAuditLog(Base):
    """Hardware access audit log"""
    __tablename__ = 'hardware_audit_log'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String(50), unique=True, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    event_type = Column(Enum(EventType), nullable=False, index=True)
    
    user_id = Column(String(50), index=True)
    patient_national_id = Column(String(14), index=True)
    card_uid = Column(String(50))
    fingerprint_id = Column(Integer)
    
    success = Column(Boolean, default=True)
    accessed_by = Column(String(50))
    access_type = Column(String(100))
    ip_address = Column(String(45))
    device_name = Column(String(100))
    
    additional_data = Column(JSON)
    
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<HardwareAuditLog(event='{self.event_id}', type='{self.event_type.value}', time='{self.timestamp}')>"


# ==================== CONVENIENCE ALIAS ====================

# For backward compatibility with existing code
Doctor = User  # Doctor is just a User with role='doctor'


# ==================== MODEL EXPORTS ====================

__all__ = [
    'Base',
    'User',
    'Patient',
    'Doctor',  # Alias for User
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
    'NFCCard',  # Convenience class
    'HardwareAuditLog',
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