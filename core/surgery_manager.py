"""
Surgery Manager - Manage Surgical Procedures
MySQL Version - Compatible with existing GUI
"""

from datetime import datetime, date
from core.database import get_db
from database.models import Surgery, Patient
import uuid

class SurgeryManager:
    """Manage patient surgeries"""
    
    def __init__(self):
        pass
    
    def add_surgery(self, national_id, surgery_data):
        """
        Add surgery record
        
        surgery_data should contain:
        - procedure_name: str
        - date: date
        - hospital: str (optional)
        - surgeon_name: str (optional)
        - anesthesia_type: str (optional)
        - duration: str (optional)
        - complications: str (optional)
        - recovery_notes: str (optional)
        - outcome: str ('successful', 'complicated', 'failed')
        """
        with get_db() as db:
            # Check if patient exists
            patient = db.query(Patient).filter(
                Patient.national_id == national_id
            ).first()
            
            if not patient:
                return {'success': False, 'message': 'Patient not found'}
            
            # Generate surgery ID
            if 'surgery_id' not in surgery_data:
                surgery_data['surgery_id'] = f"SURG-{uuid.uuid4().hex[:12].upper()}"
            
            # Convert date string to date object if needed
            if 'date' in surgery_data and isinstance(surgery_data['date'], str):
                surgery_data['date'] = datetime.strptime(surgery_data['date'], '%Y-%m-%d').date()
            
            surgery = Surgery(
                patient_national_id=national_id,
                **surgery_data
            )
            db.add(surgery)
            db.commit()
            db.refresh(surgery)
            
            return {
                'success': True,
                'surgery': surgery,
                'message': 'Surgery record added'
            }
    
    def get_surgeries(self, national_id):
        """Get all surgeries for patient"""
        with get_db() as db:
            return db.query(Surgery).filter(
                Surgery.patient_national_id == national_id
            ).order_by(Surgery.date.desc()).all()
    
    def get_surgery(self, surgery_id):
        """Get specific surgery by ID"""
        with get_db() as db:
            return db.query(Surgery).filter(
                Surgery.surgery_id == surgery_id
            ).first()
    
    def update_surgery(self, surgery_id, update_data):
        """Update surgery record"""
        with get_db() as db:
            surgery = db.query(Surgery).filter(
                Surgery.surgery_id == surgery_id
            ).first()
            
            if not surgery:
                return {'success': False, 'message': 'Surgery not found'}
            
            for key, value in update_data.items():
                if hasattr(surgery, key):
                    # Convert date string if needed
                    if key == 'date' and isinstance(value, str):
                        value = datetime.strptime(value, '%Y-%m-%d').date()
                    setattr(surgery, key, value)
            
            db.commit()
            db.refresh(surgery)
            
            return {'success': True, 'surgery': surgery, 'message': 'Surgery updated'}
    
    def delete_surgery(self, surgery_id):
        """Delete surgery record"""
        with get_db() as db:
            surgery = db.query(Surgery).filter(
                Surgery.surgery_id == surgery_id
            ).first()
            
            if surgery:
                db.delete(surgery)
                db.commit()
                return {'success': True, 'message': 'Surgery deleted'}
            
            return {'success': False, 'message': 'Surgery not found'}
    
    def get_surgeries_by_procedure(self, procedure_name):
        """Get all surgeries of a specific type"""
        with get_db() as db:
            return db.query(Surgery).filter(
                Surgery.procedure_name.like(f"%{procedure_name}%")
            ).order_by(Surgery.date.desc()).all()
    
    def get_surgeries_by_surgeon(self, surgeon_name):
        """Get all surgeries by a specific surgeon"""
        with get_db() as db:
            return db.query(Surgery).filter(
                Surgery.surgeon_name.like(f"%{surgeon_name}%")
            ).order_by(Surgery.date.desc()).all()
    
    def get_recent_surgeries(self, national_id, limit=5):
        """Get recent surgeries for patient"""
        with get_db() as db:
            return db.query(Surgery).filter(
                Surgery.patient_national_id == national_id
            ).order_by(Surgery.date.desc()).limit(limit).all()
    
    def get_surgeries_by_outcome(self, outcome):
        """Get surgeries by outcome (successful, complicated, failed)"""
        with get_db() as db:
            return db.query(Surgery).filter(
                Surgery.outcome == outcome
            ).order_by(Surgery.date.desc()).all()
    
    def get_surgery_statistics(self, national_id):
        """Get surgery statistics for patient"""
        surgeries = self.get_surgeries(national_id)
        
        if not surgeries:
            return None
        
        outcomes = {}
        for surgery in surgeries:
            outcome = surgery.outcome or 'unknown'
            outcomes[outcome] = outcomes.get(outcome, 0) + 1
        
        procedures = list(set([s.procedure_name for s in surgeries]))
        hospitals = list(set([s.hospital for s in surgeries if s.hospital]))
        
        return {
            'total_surgeries': len(surgeries),
            'procedures': procedures,
            'outcomes': outcomes,
            'hospitals': hospitals,
            'most_recent': surgeries[0] if surgeries else None
        }
    
    def search_surgeries(self, search_term):
        """Search surgeries by procedure name or surgeon"""
        with get_db() as db:
            search = f"%{search_term}%"
            return db.query(Surgery).filter(
                (Surgery.procedure_name.like(search)) |
                (Surgery.surgeon_name.like(search)) |
                (Surgery.hospital.like(search))
            ).order_by(Surgery.date.desc()).all()

# Global instance
surgery_manager = SurgeryManager()