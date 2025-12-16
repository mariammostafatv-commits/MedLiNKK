"""
SQLAlchemy Database Models
MedLink database schema - Similar to Laravel's Eloquent models
Location: database/models.py
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, JSON, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base


# ============================================
# USER MODEL
# ============================================
class User(Base):
    """
    User authentication model
    Supports: doctors, patients, admins
    """
    __tablename__ = 'users'
    
    user_id = Column(String(50), primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, index=True)  # doctor, patient, admin
    
    # Common fields
    full_name = Column(String(200), nullable=False)
    email = Column(String(150), index=True)
    phone = Column(String(20))
    
    # Doctor-specific fields
    specialization = Column(String(100))
    hospital = Column(String(200))
    license_number = Column(String(50))
    
    # Patient-specific fields
    national_id = Column(String(14), unique=True, index=True)
    
    # Fingerprint authentication
    fingerprint_id = Column(Integer)
    fingerprint_enrolled = Column(Boolean, default=False)
    fingerprint_enrollment_date = Column(Date)
    last_fingerprint_login = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime)
    
    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


# ============================================
# PATIENT MODEL (Main)
# ============================================
class Patient(Base):
    """
    Patient master record
    Contains all patient information including medical history
    """
    __tablename__ = 'patients'
    
    # Primary identification
    national_id = Column(String(14), primary_key=True, index=True)
    full_name = Column(String(200), nullable=False, index=True)
    
    # Demographics
    date_of_birth = Column(Date, nullable=False)
    age = Column(Integer)
    gender = Column(String(10))  # Male, Female
    blood_type = Column(String(5))  # A+, B+, O+, AB+, etc.
    
    # Contact information
    phone = Column(String(20))
    email = Column(String(150))
    address = Column(Text)
    
    # Emergency contact (stored as JSON)
    emergency_contact = Column(JSON)  # {name, relation, phone}
    
    # Medical information (arrays as JSON)
    chronic_diseases = Column(JSON)  # List of chronic diseases
    allergies = Column(JSON)  # List of allergies
    current_medications = Column(JSON)  # List of current medications with dosage
    
    # Insurance (stored as JSON)
    insurance = Column(JSON)  # {provider, policy_number, expiry, coverage_type}
    
    # External links
    external_links = Column(JSON)  # {lab_account, imaging_account}
    
    # NFC Card information
    nfc_card_uid = Column(String(50), unique=True, index=True)
    nfc_card_assigned = Column(Boolean, default=False)
    nfc_card_assignment_date = Column(Date)
    nfc_card_type = Column(String(50))
    nfc_card_status = Column(String(20))  # active, lost, unassigned
    nfc_card_last_scan = Column(DateTime)
    nfc_scan_count = Column(Integer, default=0)
    
    # Nested medical records (stored as JSON for flexibility)
    # These are complex nested structures - storing as JSON is more efficient
    surgeries = Column(JSON)  # List of surgery records
    hospitalizations = Column(JSON)  # List of hospitalization records
    vaccinations = Column(JSON)  # List of vaccination records
    family_history = Column(JSON)  # Family medical history object
    disabilities_special_needs = Column(JSON)  # Disability information object
    emergency_directives = Column(JSON)  # DNR, organ donor, etc.
    lifestyle = Column(JSON)  # Smoking, exercise, diet, etc.
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    visits = relationship("Visit", back_populates="patient", cascade="all, delete-orphan")
    lab_results = relationship("LabResult", back_populates="patient", cascade="all, delete-orphan")
    imaging_results = relationship("ImagingResult", back_populates="patient", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Patient {self.full_name} ({self.national_id})>"


# ============================================
# VISIT MODEL
# ============================================
class Visit(Base):
    """
    Medical visit records
    Tracks doctor visits and consultations
    """
    __tablename__ = 'visits'
    
    visit_id = Column(String(50), primary_key=True, index=True)
    patient_national_id = Column(String(14), ForeignKey('patients.national_id'), nullable=False, index=True)
    
    # Visit details
    date = Column(Date, nullable=False, index=True)
    time = Column(String(10))
    
    # Doctor information
    doctor_id = Column(String(50), nullable=False, index=True)
    doctor_name = Column(String(200), nullable=False)
    hospital = Column(String(200))
    department = Column(String(100))
    
    # Visit type
    visit_type = Column(String(50))  # Consultation, Emergency, Follow-up, etc.
    
    # Medical details
    chief_complaint = Column(Text)
    diagnosis = Column(Text)
    treatment_plan = Column(Text)
    notes = Column(Text)
    
    # Vital signs (stored as JSON)
    vital_signs = Column(JSON)  # {blood_pressure, heart_rate, temperature, weight}
    
    # Prescriptions (stored as JSON array)
    prescriptions = Column(JSON)  # [{medication, dosage, frequency, duration}]
    
    # Attachments
    attachments = Column(JSON)  # List of file paths
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    patient = relationship("Patient", back_populates="visits")
    
    def __repr__(self):
        return f"<Visit {self.visit_id} - {self.patient_national_id} on {self.date}>"


# ============================================
# LAB RESULT MODEL
# ============================================
class LabResult(Base):
    """
    Laboratory test results
    """
    __tablename__ = 'lab_results'
    
    result_id = Column(String(50), primary_key=True, index=True)
    patient_national_id = Column(String(14), ForeignKey('patients.national_id'), nullable=False, index=True)
    
    # Lab details
    date = Column(Date, nullable=False, index=True)
    lab_name = Column(String(200), nullable=False)
    test_type = Column(String(200), nullable=False)
    
    # Status
    status = Column(String(20))  # completed, pending
    
    # Results (stored as JSON for flexibility)
    results = Column(JSON)  # {test_name: value}
    
    # Additional information
    notes = Column(Text)
    external_link = Column(String(500))
    attachment = Column(String(500))  # File path
    
    # Ordered by
    ordered_by = Column(String(50))  # Doctor ID
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    patient = relationship("Patient", back_populates="lab_results")
    
    def __repr__(self):
        return f"<LabResult {self.result_id} - {self.test_type}>"


# ============================================
# IMAGING RESULT MODEL
# ============================================
class ImagingResult(Base):
    """
    Imaging test results (X-Ray, CT, MRI, Ultrasound)
    """
    __tablename__ = 'imaging_results'
    
    imaging_id = Column(String(50), primary_key=True, index=True)
    patient_national_id = Column(String(14), ForeignKey('patients.national_id'), nullable=False, index=True)
    
    # Imaging details
    date = Column(Date, nullable=False, index=True)
    imaging_center = Column(String(200), nullable=False)
    imaging_type = Column(String(50), nullable=False)  # X-Ray, CT, MRI, Ultrasound
    body_part = Column(String(100))
    
    # Results
    findings = Column(Text)
    radiologist = Column(String(200))
    
    # Additional information
    external_link = Column(String(500))
    images = Column(JSON)  # List of image file paths
    
    # Ordered by
    ordered_by = Column(String(50))  # Doctor ID
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    patient = relationship("Patient", back_populates="imaging_results")
    
    def __repr__(self):
        return f"<ImagingResult {self.imaging_id} - {self.imaging_type}>"


# ============================================
# NFC CARD MODEL
# ============================================
class NFCCard(Base):
    """
    NFC card mappings for doctors and patients
    """
    __tablename__ = 'nfc_cards'
    
    card_uid = Column(String(50), primary_key=True, index=True)
    
    # Card type
    card_type = Column(String(20), nullable=False)  # doctor, patient
    
    # User mapping
    username = Column(String(100))  # For doctors
    national_id = Column(String(14))  # For patients
    
    # Card holder information
    holder_name = Column(String(200))
    
    # Card status
    status = Column(String(20), default='active')  # active, lost, deactivated
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    last_used = Column(DateTime)
    
    def __repr__(self):
        return f"<NFCCard {self.card_uid} ({self.card_type})>"


# ============================================
# HARDWARE AUDIT LOG MODEL
# ============================================
class HardwareAuditLog(Base):
    """
    Audit log for hardware events (NFC scans, fingerprint scans)
    """
    __tablename__ = 'hardware_audit_logs'
    
    event_id = Column(String(50), primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now, index=True)
    
    # Event details
    event_type = Column(String(50), nullable=False)  # nfc_scan, fingerprint_login, etc.
    
    # User/Patient identification
    user_id = Column(String(50))
    patient_national_id = Column(String(14))
    
    # Hardware details
    card_uid = Column(String(50))
    fingerprint_id = Column(Integer)
    
    # Event result
    success = Column(Boolean, default=False)
    error_message = Column(Text)
    
    # Additional context
    ip_address = Column(String(50))
    device_name = Column(String(100))
    accessed_by = Column(String(50))  # Doctor who accessed
    access_type = Column(String(50))
    confidence = Column(Integer)  # For fingerprint confidence score
    
    def __repr__(self):
        return f"<HardwareAuditLog {self.event_id} - {self.event_type}>"