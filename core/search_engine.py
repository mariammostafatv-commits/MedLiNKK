"""
FIXED Search Engine - Patient and Medical Record Search
Returns dicts instead of SQLAlchemy objects to prevent session errors

Location: core/search_engine.py (REPLACE YOUR FILE)
"""

from core.database import get_db
from core.models import (
    Patient, User, Visit, LabResult, ImagingResult,
    Surgery, Hospitalization, Vaccination
)
from sqlalchemy import or_, and_, desc, func
from typing import List, Dict, Optional
from datetime import datetime, date, timedelta


def convert_patient_to_dict(patient) -> dict:
    """
    Convert Patient SQLAlchemy object to dict within session
    This prevents DetachedInstanceError in GUI
    """
    if not patient:
        return None
    
    try:
        return {
            'id': patient.id,
            'national_id': patient.national_id,
            'full_name': patient.full_name,
            'date_of_birth': patient.date_of_birth,
            'age': patient.age,
            'gender': patient.gender.value if hasattr(patient.gender, 'value') else str(patient.gender),
            'blood_type': patient.blood_type.value if hasattr(patient.blood_type, 'value') else str(patient.blood_type),
            'phone': patient.phone,
            'email': patient.email,
            'address': patient.address,
            'city': patient.city,
            'governorate': patient.governorate,
            
            # JSON fields
            'emergency_contact': patient.emergency_contact or {},
            'allergies': patient.allergies or [],
            'chronic_diseases': patient.chronic_diseases or [],
            'family_history': patient.family_history or {},
            'disabilities_special_needs': patient.disabilities_special_needs or {},
            'emergency_directives': patient.emergency_directives or {},
            'lifestyle': patient.lifestyle or {},
            'insurance': patient.insurance or {},
            'external_links': patient.external_links or {},
            
            # Relationships - convert to dicts
            'current_medications': [
                {
                    'name': m.medication_name,
                    'dosage': m.dosage,
                    'frequency': m.frequency,
                    'started_date': str(m.started_date) if m.started_date else None
                }
                for m in patient.current_medications 
                if hasattr(m, 'is_active') and m.is_active
            ] if hasattr(patient, 'current_medications') else [],
            
            'surgeries': [
                {
                    'surgery_id': s.surgery_id,
                    'procedure': s.procedure_name,
                    'date': str(s.surgery_date) if s.surgery_date else None,
                    'hospital': s.hospital,
                    'surgeon': s.surgeon_name,
                    'complications': s.complications,
                    'notes': s.recovery_notes
                }
                for s in patient.surgeries
            ] if hasattr(patient, 'surgeries') else [],
            
            'hospitalizations': [
                {
                    'hospitalization_id': h.hospitalization_id,
                    'admission_date': str(h.admission_date) if h.admission_date else None,
                    'discharge_date': str(h.discharge_date) if h.discharge_date else None,
                    'reason': h.admission_reason,
                    'hospital': h.hospital,
                    'diagnosis': h.diagnosis,
                    'outcome': h.discharge_notes
                }
                for h in patient.hospitalizations
            ] if hasattr(patient, 'hospitalizations') else [],
            
            'vaccinations': [
                {
                    'vaccine_name': v.vaccine_name,
                    'date_administered': str(v.date_administered) if v.date_administered else None,
                    'dose_number': v.dose_number if hasattr(v, 'dose_number') else None,
                    'batch_number': v.batch_number,
                    'next_dose_due': str(v.next_dose_due) if hasattr(v, 'next_dose_due') and v.next_dose_due else None
                }
                for v in patient.vaccinations
            ] if hasattr(patient, 'vaccinations') else [],
            
            # NFC info
            'nfc_card_uid': patient.nfc_card_uid,
            'nfc_card_assigned': patient.nfc_card_assigned,
            'nfc_card_status': patient.nfc_card_status.value if hasattr(patient, 'nfc_card_status') and patient.nfc_card_status else None,
            
            # Timestamps
            'created_at': patient.created_at,
            'last_updated': patient.last_updated
        }
    except Exception as e:
        print(f"Error converting patient to dict: {e}")
        # Return minimal data if conversion fails
        return {
            'national_id': getattr(patient, 'national_id', 'Unknown'),
            'full_name': getattr(patient, 'full_name', 'Unknown'),
            'age': getattr(patient, 'age', 0),
            'gender': 'Unknown',
            'blood_type': 'Unknown'
        }


class SearchEngine:
    """Advanced search for patients and medical records - FIXED"""
    
    def __init__(self):
        pass
    
    # ==================== PATIENT SEARCH (All return dicts!) ====================
    
    def search_by_national_id(self, national_id: str) -> Optional[dict]:
        """
        Search patient by exact National ID
        
        Args:
            national_id: Patient National ID (14 digits)
            
        Returns:
            dict: Complete patient data or None
        """
        db = get_db()
        try:
            patient = db.query(Patient).filter_by(
                national_id=national_id
            ).first()
            
            if not patient:
                return None
            
            # Convert to dict WITHIN session
            return convert_patient_to_dict(patient)
        finally:
            db.close()
    
    def search_by_name(self, name: str, limit: int = 50) -> List[dict]:
        """
        Search patients by name (partial match, case-insensitive)
        
        Args:
            name: Patient name or partial name
            limit: Maximum results to return
            
        Returns:
            List[dict]: List of patient dicts
        """
        db = get_db()
        try:
            patients = db.query(Patient).filter(
                Patient.full_name.ilike(f"%{name}%")
            ).limit(limit).all()
            
            # Convert all to dicts WITHIN session
            return [convert_patient_to_dict(p) for p in patients]
        finally:
            db.close()
    
    def search_by_phone(self, phone: str, limit: int = 50) -> List[dict]:
        """
        Search patients by phone number
        
        Args:
            phone: Phone number or partial
            limit: Maximum results to return
            
        Returns:
            List[dict]: List of patient dicts
        """
        db = get_db()
        try:
            # Remove common phone formatting
            clean_phone = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
            
            patients = db.query(Patient).filter(
                Patient.phone.contains(clean_phone)
            ).limit(limit).all()
            
            # Convert all to dicts WITHIN session
            return [convert_patient_to_dict(p) for p in patients]
        finally:
            db.close()
    
    def search_patients(self, query: str, limit: int = 50) -> List[dict]:
        """
        Universal patient search (searches name, national_id, phone, email)
        
        Args:
            query: Search term
            limit: Maximum results to return
            
        Returns:
            List[dict]: List of patient dicts matching the query
        """
        db = get_db()
        try:
            # Clean query
            clean_query = query.strip()
            
            patients = db.query(Patient).filter(
                or_(
                    Patient.full_name.ilike(f"%{clean_query}%"),
                    Patient.national_id.contains(clean_query),
                    Patient.phone.contains(clean_query),
                    Patient.email.ilike(f"%{clean_query}%")
                )
            ).limit(limit).all()
            
            # Convert all to dicts WITHIN session
            return [convert_patient_to_dict(p) for p in patients]
        finally:
            db.close()
    
    def search_by_age_range(self, min_age: int, max_age: int, limit: int = 50) -> List[dict]:
        """
        Search patients by age range
        
        Args:
            min_age: Minimum age
            max_age: Maximum age
            limit: Maximum results
            
        Returns:
            List[dict]: Patients in age range
        """
        db = get_db()
        try:
            patients = db.query(Patient).filter(
                and_(
                    Patient.age >= min_age,
                    Patient.age <= max_age
                )
            ).limit(limit).all()
            
            return [convert_patient_to_dict(p) for p in patients]
        finally:
            db.close()
    
    def search_by_blood_type(self, blood_type: str, limit: int = 50) -> List[dict]:
        """
        Search patients by blood type
        
        Args:
            blood_type: Blood type (e.g., "O+", "A-", "AB+")
            limit: Maximum results
            
        Returns:
            List[dict]: Patients with matching blood type
        """
        db = get_db()
        try:
            from core.models import BloodType
            
            # Try to convert string to BloodType enum
            try:
                blood_type_enum = BloodType[blood_type.replace('+', '_pos').replace('-', '_neg')]
                
                patients = db.query(Patient).filter(
                    Patient.blood_type == blood_type_enum
                ).limit(limit).all()
                
                return [convert_patient_to_dict(p) for p in patients]
            except (KeyError, AttributeError):
                return []
        finally:
            db.close()
    
    def search_by_city(self, city: str, limit: int = 50) -> List[dict]:
        """
        Search patients by city
        
        Args:
            city: City name
            limit: Maximum results
            
        Returns:
            List[dict]: Patients in specified city
        """
        db = get_db()
        try:
            patients = db.query(Patient).filter(
                Patient.city.ilike(f"%{city}%")
            ).limit(limit).all()
            
            return [convert_patient_to_dict(p) for p in patients]
        finally:
            db.close()
    
    def get_all_patients(self, limit: int = 100, offset: int = 0) -> List[dict]:
        """
        Get all patients (with pagination)
        
        Args:
            limit: Number of patients to return
            offset: Number of patients to skip
            
        Returns:
            List[dict]: Patient dicts
        """
        db = get_db()
        try:
            patients = db.query(Patient).order_by(
                Patient.full_name
            ).limit(limit).offset(offset).all()
            
            return [convert_patient_to_dict(p) for p in patients]
        finally:
            db.close()
    
    def get_recent_patients(self, days: int = 30, limit: int = 50) -> List[dict]:
        """
        Get recently registered patients
        
        Args:
            days: Number of days to look back
            limit: Maximum results
            
        Returns:
            List[dict]: Recently registered patients
        """
        db = get_db()
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            patients = db.query(Patient).filter(
                Patient.created_at >= cutoff_date
            ).order_by(
                desc(Patient.created_at)
            ).limit(limit).all()
            
            return [convert_patient_to_dict(p) for p in patients]
        finally:
            db.close()
    
    # ==================== PATIENT STATISTICS ====================
    
    def get_patient_statistics(self, national_id: str) -> dict:
        """
        Get comprehensive patient statistics
        
        Args:
            national_id: Patient National ID
            
        Returns:
            dict: Statistics about patient's medical records
        """
        db = get_db()
        try:
            patient = db.query(Patient).filter(
                Patient.national_id == national_id
            ).first()
            
            if not patient:
                return {}
            
            stats = {
                'total_visits': db.query(Visit).filter(
                    Visit.patient_national_id == national_id
                ).count(),
                
                'total_lab_tests': db.query(LabResult).filter(
                    LabResult.patient_national_id == national_id
                ).count(),
                
                'total_imaging': db.query(ImagingResult).filter(
                    ImagingResult.patient_national_id == national_id
                ).count(),
                
                'total_surgeries': db.query(Surgery).filter(
                    Surgery.patient_national_id == national_id
                ).count(),
                
                'total_hospitalizations': db.query(Hospitalization).filter(
                    Hospitalization.patient_national_id == national_id
                ).count(),
                
                'total_vaccinations': db.query(Vaccination).filter(
                    Vaccination.patient_national_id == national_id
                ).count(),
                
                'has_allergies': len(patient.allergies) > 0 if patient.allergies else False,
                'allergy_count': len(patient.allergies) if patient.allergies else 0,
                
                'has_chronic_diseases': len(patient.chronic_diseases) > 0 if patient.chronic_diseases else False,
                'chronic_disease_count': len(patient.chronic_diseases) if patient.chronic_diseases else 0,
                
                'has_nfc_card': patient.nfc_card_assigned,
                'last_updated': patient.last_updated,
                'account_age_days': (datetime.now() - patient.created_at).days if patient.created_at else 0
            }
            
            return stats
        finally:
            db.close()
    
    def get_database_statistics(self) -> dict:
        """
        Get overall database statistics
        
        Returns:
            dict: Database-wide statistics
        """
        db = get_db()
        try:
            stats = {
                'total_patients': db.query(Patient).count(),
                'total_doctors': db.query(User).filter(User.role == 'doctor').count(),
                'total_visits': db.query(Visit).count(),
                'total_lab_results': db.query(LabResult).count(),
                'total_imaging_results': db.query(ImagingResult).count(),
                'total_surgeries': db.query(Surgery).count(),
                'total_hospitalizations': db.query(Hospitalization).count(),
                'total_vaccinations': db.query(Vaccination).count(),
                
                # Blood type distribution
                'blood_type_distribution': {},
                
                # Age statistics
                'avg_patient_age': db.query(func.avg(Patient.age)).scalar() or 0,
                'min_patient_age': db.query(func.min(Patient.age)).scalar() or 0,
                'max_patient_age': db.query(func.max(Patient.age)).scalar() or 0,
            }
            
            # Calculate blood type distribution
            from core.models import BloodType
            for blood_type in BloodType:
                count = db.query(Patient).filter(
                    Patient.blood_type == blood_type
                ).count()
                stats['blood_type_distribution'][blood_type.value] = count
            
            return stats
        finally:
            db.close()
    
    # ==================== ADVANCED FILTERS ====================
    
    def filter_patients(self, 
                       gender: Optional[str] = None,
                       min_age: Optional[int] = None,
                       max_age: Optional[int] = None,
                       city: Optional[str] = None,
                       blood_type: Optional[str] = None,
                       has_chronic_diseases: Optional[bool] = None,
                       has_allergies: Optional[bool] = None,
                       limit: int = 50) -> List[dict]:
        """
        Advanced patient filtering with multiple criteria
        
        Args:
            gender: Gender filter
            min_age: Minimum age
            max_age: Maximum age
            city: City name
            blood_type: Blood type
            has_chronic_diseases: Filter by chronic disease presence
            has_allergies: Filter by allergy presence
            limit: Maximum results
            
        Returns:
            List[dict]: Filtered patients
        """
        db = get_db()
        try:
            query = db.query(Patient)
            
            # Apply filters
            if gender:
                from core.models import Gender
                try:
                    gender_enum = Gender[gender]
                    query = query.filter(Patient.gender == gender_enum)
                except KeyError:
                    pass
            
            if min_age is not None:
                query = query.filter(Patient.age >= min_age)
            
            if max_age is not None:
                query = query.filter(Patient.age <= max_age)
            
            if city:
                query = query.filter(Patient.city.ilike(f"%{city}%"))
            
            if blood_type:
                from core.models import BloodType
                try:
                    blood_type_enum = BloodType[blood_type.replace('+', '_pos').replace('-', '_neg')]
                    query = query.filter(Patient.blood_type == blood_type_enum)
                except KeyError:
                    pass
            
            # Get results
            patients = query.limit(limit).all()
            
            # Convert to dicts
            result = [convert_patient_to_dict(p) for p in patients]
            
            # Apply JSON field filters (must be done after query)
            if has_chronic_diseases is not None:
                result = [p for p in result 
                         if (len(p.get('chronic_diseases', [])) > 0) == has_chronic_diseases]
            
            if has_allergies is not None:
                result = [p for p in result 
                         if (len(p.get('allergies', [])) > 0) == has_allergies]
            
            return result
        finally:
            db.close()


# Global instance
search_engine = SearchEngine()