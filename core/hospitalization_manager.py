"""
Hospitalization Manager - Manage Hospital Admissions
MySQL Version - Compatible with existing GUI
"""

from datetime import datetime, date
from core.database import get_db
from database.models import Hospitalization, Patient
import uuid

class HospitalizationManager:
    """Manage patient hospitalizations"""
    
    def __init__(self):
        pass
    
    def add_hospitalization(self, national_id, hospitalization_data):
        """
        Add hospitalization record
        
        hospitalization_data should contain:
        - admission_date: date
        - discharge_date: date (optional if still admitted)
        - hospital: str
        - department: str (optional)
        - admission_reason: str
        - diagnosis: str (optional)
        - treatment_summary: str (optional)
        - discharge_notes: str (optional)
        """
        with get_db() as db:
            # Check if patient exists
            patient = db.query(Patient).filter(
                Patient.national_id == national_id
            ).first()
            
            if not patient:
                return {'success': False, 'message': 'Patient not found'}
            
            # Generate hospitalization ID
            if 'hospitalization_id' not in hospitalization_data:
                hospitalization_data['hospitalization_id'] = f"HOSP-{uuid.uuid4().hex[:12].upper()}"
            
            # Calculate days stayed if discharge date provided
            if 'discharge_date' in hospitalization_data and hospitalization_data['discharge_date']:
                admission = hospitalization_data['admission_date']
                discharge = hospitalization_data['discharge_date']
                
                if isinstance(admission, str):
                    admission = datetime.strptime(admission, '%Y-%m-%d').date()
                if isinstance(discharge, str):
                    discharge = datetime.strptime(discharge, '%Y-%m-%d').date()
                
                hospitalization_data['days_stayed'] = (discharge - admission).days
            
            hospitalization = Hospitalization(
                patient_national_id=national_id,
                **hospitalization_data
            )
            db.add(hospitalization)
            db.commit()
            db.refresh(hospitalization)
            
            return {
                'success': True,
                'hospitalization': hospitalization,
                'message': 'Hospitalization record added'
            }
    
    def get_hospitalizations(self, national_id):
        """Get all hospitalizations for patient"""
        with get_db() as db:
            return db.query(Hospitalization).filter(
                Hospitalization.patient_national_id == national_id
            ).order_by(Hospitalization.admission_date.desc()).all()
    
    def get_hospitalization(self, hospitalization_id):
        """Get specific hospitalization by ID"""
        with get_db() as db:
            return db.query(Hospitalization).filter(
                Hospitalization.hospitalization_id == hospitalization_id
            ).first()
    
    def update_hospitalization(self, hospitalization_id, update_data):
        """Update hospitalization record"""
        with get_db() as db:
            hosp = db.query(Hospitalization).filter(
                Hospitalization.hospitalization_id == hospitalization_id
            ).first()
            
            if not hosp:
                return {'success': False, 'message': 'Hospitalization not found'}
            
            for key, value in update_data.items():
                if hasattr(hosp, key):
                    setattr(hosp, key, value)
            
            # Recalculate days stayed if dates changed
            if hosp.admission_date and hosp.discharge_date:
                hosp.days_stayed = (hosp.discharge_date - hosp.admission_date).days
            
            db.commit()
            db.refresh(hosp)
            
            return {'success': True, 'hospitalization': hosp, 'message': 'Record updated'}
    
    def delete_hospitalization(self, hospitalization_id):
        """Delete hospitalization record"""
        with get_db() as db:
            hosp = db.query(Hospitalization).filter(
                Hospitalization.hospitalization_id == hospitalization_id
            ).first()
            
            if hosp:
                db.delete(hosp)
                db.commit()
                return {'success': True, 'message': 'Hospitalization deleted'}
            
            return {'success': False, 'message': 'Hospitalization not found'}
    
    def get_current_hospitalizations(self):
        """Get all currently admitted patients"""
        with get_db() as db:
            return db.query(Hospitalization).filter(
                Hospitalization.discharge_date.is_(None)
            ).order_by(Hospitalization.admission_date.desc()).all()
    
    def discharge_patient(self, hospitalization_id, discharge_date, discharge_notes):
        """Discharge patient from hospital"""
        with get_db() as db:
            hosp = db.query(Hospitalization).filter(
                Hospitalization.hospitalization_id == hospitalization_id
            ).first()
            
            if not hosp:
                return {'success': False, 'message': 'Hospitalization not found'}
            
            if isinstance(discharge_date, str):
                discharge_date = datetime.strptime(discharge_date, '%Y-%m-%d').date()
            
            hosp.discharge_date = discharge_date
            hosp.discharge_notes = discharge_notes
            hosp.days_stayed = (discharge_date - hosp.admission_date).days
            
            db.commit()
            
            return {'success': True, 'message': 'Patient discharged'}
    
    def get_hospitalization_statistics(self, national_id):
        """Get hospitalization statistics for patient"""
        hosps = self.get_hospitalizations(national_id)
        
        if not hosps:
            return None
        
        total_days = sum([h.days_stayed or 0 for h in hosps])
        hospitals = list(set([h.hospital for h in hosps]))
        
        return {
            'total_hospitalizations': len(hosps),
            'total_days_hospitalized': total_days,
            'average_stay': total_days / len(hosps) if hosps else 0,
            'hospitals_visited': hospitals,
            'most_recent': hosps[0] if hosps else None
        }

# Global instance
hospitalization_manager = HospitalizationManager()