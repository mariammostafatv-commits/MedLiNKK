"""
Patient Manager
Handles all patient-related operations
"""

from datetime import datetime, date
from sqlalchemy import or_, and_
from core.database import get_db
from database.models import (
    Patient, Allergy, ChronicDisease, CurrentMedication,
    Surgery, Hospitalization, Vaccination, FamilyHistory,
    Disability, EmergencyDirective, Lifestyle, Insurance,
    Visit, LabResult, ImagingResult
)

class PatientManager:
    """Manage patient records"""
    
    def get_patient(self, national_id: str):
        """Get patient by national ID with all related data"""
        with get_db() as db:
            patient = db.query(Patient).filter(
                Patient.national_id == national_id
            ).first()
            
            if patient:
                # Load all relationships
                db.refresh(patient)
                return patient
            
            return None
    
    def get_patient_by_id(self, patient_id: int):
        """Get patient by database ID"""
        with get_db() as db:
            return db.query(Patient).filter(Patient.id == patient_id).first()
    
    def get_all_patients(self, limit=None):
        """Get all patients"""
        with get_db() as db:
            query = db.query(Patient).order_by(Patient.full_name)
            if limit:
                query = query.limit(limit)
            return query.all()
    
    def search_patients(self, search_term: str):
        """
        Search patients by name, national ID, phone, or email
        """
        with get_db() as db:
            search = f"%{search_term}%"
            patients = db.query(Patient).filter(
                or_(
                    Patient.full_name.like(search),
                    Patient.national_id.like(search),
                    Patient.phone.like(search),
                    Patient.email.like(search)
                )
            ).all()
            
            return patients
    
    def create_patient(self, patient_data: dict):
        """
        Create new patient
        patient_data should contain basic patient info
        """
        with get_db() as db:
            # Calculate age from date_of_birth
            if 'date_of_birth' in patient_data and isinstance(patient_data['date_of_birth'], str):
                dob = datetime.strptime(patient_data['date_of_birth'], '%Y-%m-%d').date()
                patient_data['date_of_birth'] = dob
                patient_data['age'] = (date.today() - dob).days // 365
            
            patient = Patient(**patient_data)
            db.add(patient)
            db.commit()
            db.refresh(patient)
            
            return patient
    
    def update_patient(self, national_id: str, update_data: dict):
        """Update patient information"""
        with get_db() as db:
            patient = db.query(Patient).filter(
                Patient.national_id == national_id
            ).first()
            
            if patient:
                for key, value in update_data.items():
                    if hasattr(patient, key):
                        setattr(patient, key, value)
                
                patient.last_updated = datetime.now()
                db.commit()
                db.refresh(patient)
                return patient
            
            return None
    
    def delete_patient(self, national_id: str):
        """Delete patient (use with caution!)"""
        with get_db() as db:
            patient = db.query(Patient).filter(
                Patient.national_id == national_id
            ).first()
            
            if patient:
                db.delete(patient)
                db.commit()
                return True
            
            return False
    
    # ========================================================================
    # ALLERGIES
    # ========================================================================
    
    def add_allergy(self, national_id: str, allergen: str, **kwargs):
        """Add allergy to patient"""
        with get_db() as db:
            allergy = Allergy(
                patient_national_id=national_id,
                allergen=allergen,
                **kwargs
            )
            db.add(allergy)
            db.commit()
            return allergy
    
    def get_allergies(self, national_id: str):
        """Get patient allergies"""
        with get_db() as db:
            return db.query(Allergy).filter(
                Allergy.patient_national_id == national_id
            ).all()
    
    def remove_allergy(self, allergy_id: int):
        """Remove allergy"""
        with get_db() as db:
            allergy = db.query(Allergy).filter(Allergy.id == allergy_id).first()
            if allergy:
                db.delete(allergy)
                db.commit()
                return True
            return False
    
    # ========================================================================
    # CHRONIC DISEASES
    # ========================================================================
    
    def add_chronic_disease(self, national_id: str, disease_name: str, **kwargs):
        """Add chronic disease to patient"""
        with get_db() as db:
            disease = ChronicDisease(
                patient_national_id=national_id,
                disease_name=disease_name,
                **kwargs
            )
            db.add(disease)
            db.commit()
            return disease
    
    def get_chronic_diseases(self, national_id: str):
        """Get patient chronic diseases"""
        with get_db() as db:
            return db.query(ChronicDisease).filter(
                ChronicDisease.patient_national_id == national_id
            ).all()
    
    # ========================================================================
    # CURRENT MEDICATIONS
    # ========================================================================
    
    def add_medication(self, national_id: str, medication_data: dict):
        """Add current medication"""
        with get_db() as db:
            medication = CurrentMedication(
                patient_national_id=national_id,
                **medication_data
            )
            db.add(medication)
            db.commit()
            return medication
    
    def get_current_medications(self, national_id: str):
        """Get active medications"""
        with get_db() as db:
            return db.query(CurrentMedication).filter(
                CurrentMedication.patient_national_id == national_id,
                CurrentMedication.is_active == True
            ).all()
    
    def stop_medication(self, medication_id: int, reason: str = None):
        """Stop a medication"""
        with get_db() as db:
            medication = db.query(CurrentMedication).filter(
                CurrentMedication.id == medication_id
            ).first()
            
            if medication:
                medication.is_active = False
                medication.stopped_date = date.today()
                medication.reason_for_stopping = reason
                db.commit()
                return True
            return False
    
    # ========================================================================
    # SURGERIES
    # ========================================================================
    
    def add_surgery(self, national_id: str, surgery_data: dict):
        """Add surgery record"""
        with get_db() as db:
            surgery = Surgery(
                patient_national_id=national_id,
                **surgery_data
            )
            db.add(surgery)
            db.commit()
            return surgery
    
    def get_surgeries(self, national_id: str):
        """Get patient surgeries"""
        with get_db() as db:
            return db.query(Surgery).filter(
                Surgery.patient_national_id == national_id
            ).order_by(Surgery.date.desc()).all()
    
    # ========================================================================
    # HOSPITALIZATIONS
    # ========================================================================
    
    def add_hospitalization(self, national_id: str, hospitalization_data: dict):
        """Add hospitalization record"""
        with get_db() as db:
            hosp = Hospitalization(
                patient_national_id=national_id,
                **hospitalization_data
            )
            db.add(hosp)
            db.commit()
            return hosp
    
    def get_hospitalizations(self, national_id: str):
        """Get patient hospitalizations"""
        with get_db() as db:
            return db.query(Hospitalization).filter(
                Hospitalization.patient_national_id == national_id
            ).order_by(Hospitalization.admission_date.desc()).all()
    
    # ========================================================================
    # VACCINATIONS
    # ========================================================================
    
    def add_vaccination(self, national_id: str, vaccination_data: dict):
        """Add vaccination record"""
        with get_db() as db:
            vaccination = Vaccination(
                patient_national_id=national_id,
                **vaccination_data
            )
            db.add(vaccination)
            db.commit()
            return vaccination
    
    def get_vaccinations(self, national_id: str):
        """Get patient vaccinations"""
        with get_db() as db:
            return db.query(Vaccination).filter(
                Vaccination.patient_national_id == national_id
            ).order_by(Vaccination.date_administered.desc()).all()
    
    # ========================================================================
    # EMERGENCY DIRECTIVES
    # ========================================================================
    
    def set_emergency_directives(self, national_id: str, directives_data: dict):
        """Set or update emergency directives"""
        with get_db() as db:
            directives = db.query(EmergencyDirective).filter(
                EmergencyDirective.patient_national_id == national_id
            ).first()
            
            if directives:
                # Update existing
                for key, value in directives_data.items():
                    if hasattr(directives, key):
                        setattr(directives, key, value)
            else:
                # Create new
                directives = EmergencyDirective(
                    patient_national_id=national_id,
                    **directives_data
                )
                db.add(directives)
            
            db.commit()
            return directives
    
    def get_emergency_directives(self, national_id: str):
        """Get emergency directives"""
        with get_db() as db:
            return db.query(EmergencyDirective).filter(
                EmergencyDirective.patient_national_id == national_id
            ).first()
    
    # ========================================================================
    # LIFESTYLE
    # ========================================================================
    
    def set_lifestyle(self, national_id: str, lifestyle_data: dict):
        """Set or update lifestyle information"""
        with get_db() as db:
            lifestyle = db.query(Lifestyle).filter(
                Lifestyle.patient_national_id == national_id
            ).first()
            
            if lifestyle:
                # Update existing
                for key, value in lifestyle_data.items():
                    if hasattr(lifestyle, key):
                        setattr(lifestyle, key, value)
            else:
                # Create new
                lifestyle = Lifestyle(
                    patient_national_id=national_id,
                    **lifestyle_data
                )
                db.add(lifestyle)
            
            db.commit()
            return lifestyle
    
    def get_lifestyle(self, national_id: str):
        """Get lifestyle information"""
        with get_db() as db:
            return db.query(Lifestyle).filter(
                Lifestyle.patient_national_id == national_id
            ).first()
    
    # ========================================================================
    # INSURANCE
    # ========================================================================
    
    def set_insurance(self, national_id: str, insurance_data: dict):
        """Set or update insurance information"""
        with get_db() as db:
            insurance = db.query(Insurance).filter(
                Insurance.patient_national_id == national_id
            ).first()
            
            if insurance:
                # Update existing
                for key, value in insurance_data.items():
                    if hasattr(insurance, key):
                        setattr(insurance, key, value)
            else:
                # Create new
                insurance = Insurance(
                    patient_national_id=national_id,
                    **insurance_data
                )
                db.add(insurance)
            
            db.commit()
            return insurance
    
    def get_insurance(self, national_id: str):
        """Get insurance information"""
        with get_db() as db:
            return db.query(Insurance).filter(
                Insurance.patient_national_id == national_id
            ).first()
    
    # ========================================================================
    # MEDICAL HISTORY SUMMARY
    # ========================================================================
    
    def get_complete_medical_history(self, national_id: str):
        """Get complete medical history for patient"""
        with get_db() as db:
            patient = db.query(Patient).filter(
                Patient.national_id == national_id
            ).first()
            
            if not patient:
                return None
            
            return {
                'patient': patient.to_dict(),
                'allergies': [a.to_dict() for a in patient.allergies],
                'chronic_diseases': [cd.disease_name for cd in patient.chronic_diseases],
                'current_medications': [m.to_dict() for m in patient.current_medications if m.is_active],
                'surgeries': [s.procedure_name for s in patient.surgeries],
                'hospitalizations': len(patient.hospitalizations),
                'vaccinations': [v.vaccine_name for v in patient.vaccinations],
                'visits': len(patient.visits),
                'lab_results': len(patient.lab_results),
                'imaging_results': len(patient.imaging_results),
            }
    
    # ========================================================================
    # STATISTICS
    # ========================================================================
    
    def get_patient_count(self):
        """Get total number of patients"""
        with get_db() as db:
            return db.query(Patient).count()
    
    def get_patients_by_blood_type(self, blood_type: str):
        """Get patients by blood type"""
        with get_db() as db:
            return db.query(Patient).filter(
                Patient.blood_type == blood_type
            ).all()

# Global instance
patient_manager = PatientManager()