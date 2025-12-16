"""
Imaging Manager - Manage Imaging/Radiology Results
MySQL Version - Compatible with existing GUI
"""

from datetime import datetime, date
from core.database import get_db
from database.models import ImagingResult

class ImagingManager:
    """Manage imaging results"""
    
    def __init__(self):
        pass
    
    def create_imaging_result(self, result_data):
        """Create new imaging result"""
        with get_db() as db:
            result = ImagingResult(**result_data)
            db.add(result)
            db.commit()
            db.refresh(result)
            return result
    
    def get_imaging_result(self, imaging_id):
        """Get imaging result by ID"""
        with get_db() as db:
            return db.query(ImagingResult).filter(
                ImagingResult.imaging_id == imaging_id
            ).first()
    
    def get_patient_imaging_results(self, national_id, limit=None):
        """Get all imaging results for a patient"""
        with get_db() as db:
            query = db.query(ImagingResult).filter(
                ImagingResult.patient_national_id == national_id
            ).order_by(ImagingResult.date.desc())
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
    
    def get_imaging_by_type(self, national_id, imaging_type):
        """Get imaging results by type"""
        with get_db() as db:
            return db.query(ImagingResult).filter(
                ImagingResult.patient_national_id == national_id,
                ImagingResult.imaging_type == imaging_type
            ).order_by(ImagingResult.date.desc()).all()
    
    def update_imaging_result(self, imaging_id, update_data):
        """Update imaging result"""
        with get_db() as db:
            result = db.query(ImagingResult).filter(
                ImagingResult.imaging_id == imaging_id
            ).first()
            
            if result:
                for key, value in update_data.items():
                    if hasattr(result, key):
                        setattr(result, key, value)
                
                db.commit()
                db.refresh(result)
                return result
            
            return None
    
    def delete_imaging_result(self, imaging_id):
        """Delete imaging result"""
        with get_db() as db:
            result = db.query(ImagingResult).filter(
                ImagingResult.imaging_id == imaging_id
            ).first()
            
            if result:
                db.delete(result)
                db.commit()
                return True
            
            return False

# Global instance
imaging_manager = ImagingManager()