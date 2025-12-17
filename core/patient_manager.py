"""
FIXED Patient Manager - Works with GUI
Location: core/patient_manager.py (REPLACE YOUR FILE)
"""

from core.database import get_db
from core.models import User ,Patient, Surgery, Hospitalization, Vaccination, CurrentMedication
from datetime import datetime

class PatientManager:
    """Manage patient records - COMPLETE FIX"""
    
    def get_patient(self, national_id: str):
        """
        Get patient by national ID - returns dict
        
        Args:
            national_id: Patient national ID
            
        Returns:
            dict: Complete patient data or None
        """
        db = get_db()
        try:
            patient = db.query(Patient).filter_by(national_id=national_id).first()
            
            if not patient:
                return None
            
            # Convert to dict while in session (CRITICAL!)
            return self._patient_to_dict(patient)
        finally:
            db.close()
    
    def get_patient_by_id(self, national_id: str):
        """Alias for get_patient (for compatibility)"""
        return self.get_patient(national_id)
    
    def get_all_patients(self):
        """Get all patients - returns list of dicts"""
        db = get_db()
        try:
            patients = db.query(Patient).order_by(Patient.full_name).all()
            return [self._patient_to_dict(p) for p in patients]
        finally:
            db.close()
    
    def search_patients(self, search_term: str):
        """Search patients by name or national ID"""
        db = get_db()
        try:
            search = f"%{search_term}%"
            patients = db.query(Patient).filter(
                (Patient.full_name.ilike(search)) |
                (Patient.national_id.ilike(search)) |
                (Patient.phone.ilike(search))
            ).limit(50).all()
            
            return [self._patient_to_dict(p) for p in patients]
        finally:
            db.close()
    
    def create_patient(self, patient_data: dict):
        """Create new patient"""
        db = get_db()
        try:
            patient = Patient(**patient_data)
            db.add(patient)
            db.commit()
            db.refresh(patient)
            return self._patient_to_dict(patient)
        except Exception as e:
            db.rollback()
            print(f"Error creating patient: {e}")
            return None
        finally:
            db.close()
    
    def update_patient(self, national_id: str, update_data: dict):
        """Update patient information"""
        db = get_db()
        try:
            patient = db.query(Patient).filter_by(national_id=national_id).first()
            
            if not patient:
                return None
            
            for key, value in update_data.items():
                if hasattr(patient, key):
                    setattr(patient, key, value)
            
            patient.last_updated = datetime.now()
            db.commit()
            db.refresh(patient)
            
            return self._patient_to_dict(patient)
        except Exception as e:
            db.rollback()
            print(f"Error updating patient: {e}")
            return None
        finally:
            db.close()
    
    def get_surgeries(self, national_id: str):
        """Get patient surgeries"""
        db = get_db()
        try:
            surgeries = db.query(Surgery).filter_by(
                patient_national_id=national_id
            ).order_by(Surgery.date.desc()).all()
            
            return [{
                'surgery_id': s.surgery_id,
                'procedure_name': s.procedure_name,
                'date': s.date,
                'surgeon_name': s.surgeon_name,
                'hospital': s.hospital,
                'outcome': s.outcome,
                'complications': s.complications,
                'recovery_notes': s.recovery_notes
            } for s in surgeries]
        finally:
            db.close()
    
    def get_hospitalizations(self, national_id: str):
        """Get patient hospitalizations"""
        db = get_db()
        try:
            hosps = db.query(Hospitalization).filter_by(
                patient_national_id=national_id
            ).order_by(Hospitalization.admission_date.desc()).all()
            
            return [{
                'hospitalization_id': h.hospitalization_id,
                'hospital': h.hospital,
                'department': h.department,
                'admission_date': h.admission_date,
                'discharge_date': h.discharge_date,
                'admission_reason': h.admission_reason,
                'diagnosis': h.diagnosis,
                'treatment_summary': h.treatment_summary,
                'days_stayed': h.days_stayed
            } for h in hosps]
        finally:
            db.close()
    
    def get_vaccinations(self, national_id: str):
        """Get patient vaccinations"""
        db = get_db()
        try:
            vaccs = db.query(Vaccination).filter_by(
                patient_national_id=national_id
            ).order_by(Vaccination.date_administered.desc()).all()
            
            return [{
                'id': v.id,
                'vaccine_name': v.vaccine_name,
                'date_administered': v.date_administered,
                'dose_number': v.dose_number,
                'location': v.location,
                'batch_number': v.batch_number,
                'next_dose_due': v.next_dose_due,
                'administered_by': v.administered_by
            } for v in vaccs]
        finally:
            db.close()
    
    def get_current_medications(self, national_id: str):
        """Get patient's active medications"""
        db = get_db()
        try:
            meds = db.query(CurrentMedication).filter_by(
                patient_national_id=national_id,
                is_active=True
            ).all()
            
            return [{
                'id': m.id,
                'medication_name': m.medication_name,
                'dosage': m.dosage,
                'frequency': m.frequency,
                'started_date': m.started_date,
                'prescribed_by': m.prescribed_by,
                'notes': m.notes
            } for m in meds]
        finally:
            db.close()
    
    def get_patient_count(self):
        """Get total number of patients"""
        db = get_db()
        try:
            return db.query(Patient).count()
        finally:
            db.close()
    
    def _patient_to_dict(self, patient):
        """
        Convert Patient ORM object to dict
        MUST be called while session is active!
        """
        return {
            'id': patient.id,
            'national_id': patient.national_id,
            'full_name': patient.full_name,
            'date_of_birth': patient.date_of_birth,
            'age': patient.age,
            'gender': patient.gender.value if patient.gender else None,
            'blood_type': patient.blood_type.value if patient.blood_type else None,
            'phone': patient.phone,
            'email': patient.email,
            'address': patient.address,
            'city': patient.city,
            'governorate': patient.governorate,
            
            # JSON fields - directly accessible
            'emergency_contact': patient.emergency_contact or {},
            'chronic_diseases': patient.chronic_diseases or [],
            'allergies': patient.allergies or [],
            'family_history': patient.family_history or {},
            'disabilities_special_needs': patient.disabilities_special_needs or {},
            'emergency_directives': patient.emergency_directives or {},
            'lifestyle': patient.lifestyle or {},
            'insurance': patient.insurance or {},
            'external_links': patient.external_links or {},
            
            # NFC card info
            'nfc_card_uid': patient.nfc_card_uid,
            'nfc_card_assigned': patient.nfc_card_assigned,
            'nfc_card_status': patient.nfc_card_status.value if patient.nfc_card_status else None,
            
            # Timestamps
            'created_at': patient.created_at,
            'last_updated': patient.last_updated
        }


# Global instance
patient_manager = PatientManager()