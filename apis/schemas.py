"""
Pydantic Schemas for API Request/Response
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date, datetime

# ============ AUTH SCHEMAS ============
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None  # For doctors
    hospital: Optional[str] = None  # For doctors
    national_id: Optional[str] = None  # For patients

# ============ PATIENT SCHEMAS ============
class PatientCreate(BaseModel):
    national_id: str = Field(..., min_length=14, max_length=14)
    full_name: str
    date_of_birth: Optional[date] = None
    gender: str
    blood_type: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[Dict] = None
    chronic_diseases: Optional[List[str]] = []
    allergies: Optional[List[str]] = []
    current_medications: Optional[List[Dict]] = []

class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[Dict] = None
    chronic_diseases: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    current_medications: Optional[List[Dict]] = None

class PatientResponse(BaseModel):
    national_id: str
    full_name: str
    age: Optional[int]
    gender: str
    blood_type: Optional[str]
    phone: Optional[str]
    # ... all other fields

# ============ VISIT SCHEMAS ============
class VisitCreate(BaseModel):
    patient_national_id: str
    date: date
    time: Optional[str] = None
    doctor_id: str
    doctor_name: str
    visit_type: str
    chief_complaint: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment_plan: Optional[str] = None
    vital_signs: Optional[Dict] = {}
    prescriptions: Optional[List[Dict]] = []

class VisitResponse(BaseModel):
    visit_id: str
    patient_national_id: str
    date: date
    doctor_name: str
    visit_type: str
    diagnosis: Optional[str]
    # ... all other fields

# ============ MEDICAL RECORD SCHEMAS ============
class SurgeryCreate(BaseModel):
    surgery_type: str
    date: date
    hospital: str
    surgeon: Optional[str] = None
    outcome: Optional[str] = None

class HospitalizationCreate(BaseModel):
    admission_date: date
    discharge_date: Optional[date] = None
    hospital: str
    reason: str
    outcome: Optional[str] = None

class VaccinationCreate(BaseModel):
    vaccine_name: str
    date: date
    dose_number: Optional[int] = None
    next_dose_date: Optional[date] = None

# ... more schemas