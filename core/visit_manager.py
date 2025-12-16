"""
Visit Manager - Manage Medical Visits
MySQL Version - Compatible with existing GUI
"""

from datetime import datetime, date
from core.database import get_db
from database.models import Visit, Prescription

class VisitManager:
    """Manage medical visits"""
    
    def __init__(self):
        pass
    
    def create_visit(self, visit_data, prescriptions=None):
        """
        Create new visit
        visit_data: dict with visit information
        prescriptions: list of prescription dicts
        """
        with get_db() as db:
            visit = Visit(**visit_data)
            db.add(visit)
            db.flush()  # Get visit ID
            
            # Add prescriptions
            if prescriptions:
                for presc_data in prescriptions:
                    presc = Prescription(
                        visit_id=visit.visit_id,
                        patient_national_id=visit.patient_national_id,
                        **presc_data
                    )
                    db.add(presc)
            
            db.commit()
            db.refresh(visit)
            return visit
    
    def get_visit(self, visit_id):
        """Get visit by ID"""
        with get_db() as db:
            return db.query(Visit).filter(Visit.visit_id == visit_id).first()
    
    def get_patient_visits(self, national_id, limit=None):
        """Get all visits for a patient"""
        with get_db() as db:
            query = db.query(Visit).filter(
                Visit.patient_national_id == national_id
            ).order_by(Visit.date.desc(), Visit.time.desc())
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
    
    def get_doctor_visits(self, doctor_id, limit=None):
        """Get all visits by a doctor"""
        with get_db() as db:
            query = db.query(Visit).filter(
                Visit.doctor_id == doctor_id
            ).order_by(Visit.date.desc())
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
    
    def update_visit(self, visit_id, update_data):
        """Update visit information"""
        with get_db() as db:
            visit = db.query(Visit).filter(Visit.visit_id == visit_id).first()
            
            if visit:
                for key, value in update_data.items():
                    if hasattr(visit, key):
                        setattr(visit, key, value)
                
                db.commit()
                db.refresh(visit)
                return visit
            
            return None
    
    def delete_visit(self, visit_id):
        """Delete visit"""
        with get_db() as db:
            visit = db.query(Visit).filter(Visit.visit_id == visit_id).first()
            
            if visit:
                db.delete(visit)
                db.commit()
                return True
            
            return False
    
    def get_recent_visits(self, limit=10):
        """Get most recent visits across all patients"""
        with get_db() as db:
            return db.query(Visit).order_by(
                Visit.date.desc(), Visit.time.desc()
            ).limit(limit).all()
    
    def add_prescription(self, visit_id, prescription_data):
        """Add prescription to existing visit"""
        with get_db() as db:
            visit = db.query(Visit).filter(Visit.visit_id == visit_id).first()
            
            if not visit:
                return {'success': False, 'message': 'Visit not found'}
            
            presc = Prescription(
                visit_id=visit_id,
                patient_national_id=visit.patient_national_id,
                **prescription_data
            )
            db.add(presc)
            db.commit()
            
            return {'success': True, 'prescription': presc}

# Global instance
visit_manager = VisitManager()