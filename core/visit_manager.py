"""
Visit Manager - Database Version
Handles medical visits using database instead of JSON
Location: core/visit_manager.py
"""
import uuid
from datetime import datetime
from database.connection import get_db_context
from database.models import Visit, Patient


class VisitManager:
    """
    Manages medical visit records with database backend
    Compatible with existing GUI - same method signatures
    """
    
    def __init__(self):
        """Initialize visit manager"""
        pass
    
    def get_all_visits(self):
        """
        Get all visits
        
        Returns:
            list: List of visit dictionaries
        """
        with get_db_context() as db:
            visits = db.query(Visit).order_by(Visit.date.desc()).all()
            # Convert all to dict inside session
            return [self._visit_to_dict(visit) for visit in visits]
    
    def get_patient_visits(self, national_id):
        """
        Get all visits for a patient
        
        Args:
            national_id: Patient's national ID
        
        Returns:
            list: List of visit dictionaries, ordered by date descending
        """
        with get_db_context() as db:
            visits = db.query(Visit)\
                .filter_by(patient_national_id=national_id)\
                .order_by(Visit.date.desc())\
                .all()
            
            # Convert all to dict inside session
            return [self._visit_to_dict(visit) for visit in visits]
    
    def get_visit(self, visit_id):
        """
        Get visit by ID
        
        Args:
            visit_id: Visit ID
        
        Returns:
            dict: Visit data if found, None otherwise
        """
        with get_db_context() as db:
            visit = db.query(Visit).filter_by(visit_id=visit_id).first()
            if visit:
                return self._visit_to_dict(visit)
        return None
    
    def add_visit(self, visit_data):
        """
        Add new visit
        
        Args:
            visit_data: Dictionary with visit information
        
        Returns:
            str: Visit ID if successful, None otherwise
        """
        try:
            # Generate visit ID if not provided
            if 'visit_id' not in visit_data:
                visit_data['visit_id'] = f"V{uuid.uuid4().hex[:8].upper()}"
            
            # Parse date if string
            if 'date' in visit_data and isinstance(visit_data['date'], str):
                visit_data['date'] = datetime.strptime(
                    visit_data['date'], "%Y-%m-%d"
                ).date()
            
            # Set timestamps
            visit_data['created_at'] = datetime.now()
            visit_data['updated_at'] = datetime.now()
            
            # Initialize empty arrays/objects if not provided
            if 'vital_signs' not in visit_data:
                visit_data['vital_signs'] = {}
            if 'prescriptions' not in visit_data:
                visit_data['prescriptions'] = []
            if 'attachments' not in visit_data:
                visit_data['attachments'] = []
            
            with get_db_context() as db:
                # Verify patient exists
                patient = db.query(Patient).filter_by(
                    national_id=visit_data['patient_national_id']
                ).first()
                
                if not patient:
                    print(f"Error: Patient {visit_data['patient_national_id']} not found")
                    return None
                
                # Create new visit
                visit = Visit(**visit_data)
                db.add(visit)
                # Auto-commits on exit
            
            return visit_data['visit_id']
            
        except Exception as e:
            print(f"Error adding visit: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def update_visit(self, visit_id, updates):
        """
        Update visit information
        
        Args:
            visit_id: Visit ID
            updates: Dictionary of fields to update
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Parse date if string
            if 'date' in updates and isinstance(updates['date'], str):
                updates['date'] = datetime.strptime(
                    updates['date'], "%Y-%m-%d"
                ).date()
            
            # Update timestamp
            updates['updated_at'] = datetime.now()
            
            with get_db_context() as db:
                visit = db.query(Visit).filter_by(visit_id=visit_id).first()
                if not visit:
                    return False
                
                # Update fields
                for key, value in updates.items():
                    if hasattr(visit, key):
                        setattr(visit, key, value)
                
                # Auto-commits on exit
            
            return True
            
        except Exception as e:
            print(f"Error updating visit: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def delete_visit(self, visit_id):
        """
        Delete visit
        
        Args:
            visit_id: Visit ID
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with get_db_context() as db:
                visit = db.query(Visit).filter_by(visit_id=visit_id).first()
                if not visit:
                    return False
                
                db.delete(visit)
                # Auto-commits on exit
            
            return True
            
        except Exception as e:
            print(f"Error deleting visit: {e}")
            return False
    
    def get_visits_by_doctor(self, doctor_id):
        """
        Get all visits by a specific doctor
        
        Args:
            doctor_id: Doctor's user ID
        
        Returns:
            list: List of visit dictionaries
        """
        with get_db_context() as db:
            visits = db.query(Visit)\
                .filter_by(doctor_id=doctor_id)\
                .order_by(Visit.date.desc())\
                .all()
            
            # Convert all to dict inside session
            return [self._visit_to_dict(visit) for visit in visits]
    
    def get_visits_by_date_range(self, start_date, end_date):
        """
        Get visits within a date range
        
        Args:
            start_date: Start date (string or date object)
            end_date: End date (string or date object)
        
        Returns:
            list: List of visit dictionaries
        """
        # Parse dates if strings
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        with get_db_context() as db:
            visits = db.query(Visit)\
                .filter(Visit.date >= start_date)\
                .filter(Visit.date <= end_date)\
                .order_by(Visit.date.desc())\
                .all()
            
            # Convert all to dict inside session
            return [self._visit_to_dict(visit) for visit in visits]
    
    def get_visit_count(self, national_id=None):
        """
        Get visit count, optionally for a specific patient
        
        Args:
            national_id: Optional patient national ID
        
        Returns:
            int: Number of visits
        """
        with get_db_context() as db:
            query = db.query(Visit)
            
            if national_id:
                query = query.filter_by(patient_national_id=national_id)
            
            return query.count()
    
    def _visit_to_dict(self, visit):
        """
        Convert Visit model to dictionary for GUI compatibility
        Call this ONLY inside a database session context
        
        Args:
            visit: Visit SQLAlchemy model
        
        Returns:
            dict: Visit data as dictionary
        """
        if not visit:
            return None
        
        return {
            'visit_id': visit.visit_id,
            'patient_national_id': visit.patient_national_id,
            'date': str(visit.date) if visit.date else None,
            'time': visit.time,
            
            # Doctor information
            'doctor_id': visit.doctor_id,
            'doctor_name': visit.doctor_name,
            'hospital': visit.hospital,
            'department': visit.department,
            
            # Visit details
            'visit_type': visit.visit_type,
            'chief_complaint': visit.chief_complaint,
            'diagnosis': visit.diagnosis,
            'treatment_plan': visit.treatment_plan,
            'notes': visit.notes,
            
            # JSON fields
            'vital_signs': visit.vital_signs or {},
            'prescriptions': visit.prescriptions or [],
            'attachments': visit.attachments or [],
            
            # Timestamps
            'created_at': str(visit.created_at) if visit.created_at else None,
            'updated_at': str(visit.updated_at) if visit.updated_at else None
        }


# Singleton instance
_visit_manager = None

def get_visit_manager():
    """Get singleton instance of VisitManager"""
    global _visit_manager
    if _visit_manager is None:
        _visit_manager = VisitManager()
    return _visit_manager