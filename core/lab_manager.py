"""
Lab Manager
Manages lab results and laboratory tests
Location: core/lab_manager.py
"""
from database.connection import get_db_context
from database.models import LabResult
from datetime import datetime, date
from typing import Optional, List, Dict, Any
import traceback


class LabManager:
    """
    Lab Manager - Manages laboratory results
    
    Features:
    - Get all lab results
    - Get lab results by patient
    - Add new lab result
    - Update lab result
    - Delete lab result
    - Get lab result by ID
    - Search lab results
    - Get results by date range
    """
    
    def __init__(self):
        """Initialize Lab Manager"""
        pass
    
    # ========== READ OPERATIONS ==========
    
    def get_all_lab_results(self) -> List[Dict[str, Any]]:
        """
        Get all lab results
        
        Returns:
            list: List of lab result dictionaries, ordered by date descending
        """
        with get_db_context() as db:
            results = db.query(LabResult).order_by(LabResult.test_date.desc()).all()
            # Convert all to dict inside session
            return [self._lab_result_to_dict(result) for result in results]
    
    def get_patient_lab_results(self, national_id: str) -> List[Dict[str, Any]]:
        """
        Get all lab results for a patient
        
        Args:
            national_id: Patient's national ID
        
        Returns:
            list: List of lab result dictionaries, ordered by date descending
        """
        with get_db_context() as db:
            results = db.query(LabResult)\
                .filter_by(patient_national_id=national_id)\
                .order_by(LabResult.test_date.desc())\
                .all()
            
            # Convert all to dict inside session
            return [self._lab_result_to_dict(result) for result in results]
    
    def get_lab_result(self, result_id: str) -> Optional[Dict[str, Any]]:
        """
        Get lab result by ID
        
        Args:
            result_id: Lab result ID
        
        Returns:
            dict: Lab result data if found, None otherwise
        """
        with get_db_context() as db:
            result = db.query(LabResult).filter_by(result_id=result_id).first()
            if result:
                return self._lab_result_to_dict(result)
        return None
    
    def search_lab_results(self, query: str) -> List[Dict[str, Any]]:
        """
        Search lab results by test name or patient national ID
        
        Args:
            query: Search string
        
        Returns:
            list: List of matching lab result dictionaries
        """
        with get_db_context() as db:
            results = db.query(LabResult).filter(
                (LabResult.test_name.contains(query)) |
                (LabResult.patient_national_id.contains(query))
            ).order_by(LabResult.test_date.desc()).all()
            
            # Convert all to dict inside session
            return [self._lab_result_to_dict(result) for result in results]
    
    def get_lab_results_by_date_range(
        self, 
        start_date: Any, 
        end_date: Any,
        national_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get lab results within a date range
        
        Args:
            start_date: Start date (string or date object)
            end_date: End date (string or date object)
            national_id: Optional patient national ID to filter
        
        Returns:
            list: List of lab result dictionaries
        """
        # Parse dates if strings
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        with get_db_context() as db:
            query = db.query(LabResult)\
                .filter(LabResult.test_date >= start_date)\
                .filter(LabResult.test_date <= end_date)
            
            if national_id:
                query = query.filter_by(patient_national_id=national_id)
            
            results = query.order_by(LabResult.test_date.desc()).all()
            
            # Convert all to dict inside session
            return [self._lab_result_to_dict(result) for result in results]
    
    def get_lab_results_by_test_name(
        self, 
        test_name: str,
        national_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all results for a specific test name
        
        Args:
            test_name: Name of the test (e.g., "CBC", "Glucose")
            national_id: Optional patient national ID to filter
        
        Returns:
            list: List of lab result dictionaries
        """
        with get_db_context() as db:
            query = db.query(LabResult).filter(
                LabResult.test_name.contains(test_name)
            )
            
            if national_id:
                query = query.filter_by(patient_national_id=national_id)
            
            results = query.order_by(LabResult.test_date.desc()).all()
            
            # Convert all to dict inside session
            return [self._lab_result_to_dict(result) for result in results]
    
    # ========== CREATE OPERATIONS ==========
    
    def add_lab_result(self, result_data: Dict[str, Any]) -> Optional[str]:
        """
        Add new lab result
        
        Args:
            result_data: Dictionary with lab result data
                Required fields:
                - patient_national_id: str
                - test_date: date or str
                - test_name: str
                - result_value: str
                Optional fields:
                - test_type: str
                - laboratory: str
                - reference_range: str
                - unit: str
                - status: str (normal/abnormal/critical)
                - notes: str
                - attachments: list
        
        Returns:
            str: Result ID if successful, None otherwise
        """
        try:
            with get_db_context() as db:
                # Parse date if string
                test_date = result_data.get('test_date')
                if isinstance(test_date, str):
                    test_date = datetime.strptime(test_date, "%Y-%m-%d").date()
                
                # Create new result
                lab_result = LabResult(
                    patient_national_id=result_data['patient_national_id'],
                    test_date=test_date,
                    test_name=result_data['test_name'],
                    test_type=result_data.get('test_type'),
                    result_value=result_data['result_value'],
                    unit=result_data.get('unit'),
                    reference_range=result_data.get('reference_range'),
                    status=result_data.get('status', 'normal'),
                    laboratory=result_data.get('laboratory'),
                    notes=result_data.get('notes'),
                    attachments=result_data.get('attachments', [])
                )
                
                db.add(lab_result)
                db.flush()  # Get the ID before commit
                
                result_id = lab_result.result_id
                
                # Auto-commits on exit
            
            return result_id
            
        except Exception as e:
            print(f"Error adding lab result: {e}")
            traceback.print_exc()
            return None
    
    # ========== UPDATE OPERATIONS ==========
    
    def update_lab_result(self, result_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update lab result
        
        Args:
            result_id: Lab result ID
            updates: Dictionary of fields to update
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with get_db_context() as db:
                result = db.query(LabResult).filter_by(result_id=result_id).first()
                if not result:
                    return False
                
                # Update fields
                for key, value in updates.items():
                    if hasattr(result, key):
                        # Parse date if needed
                        if key == 'test_date' and isinstance(value, str):
                            value = datetime.strptime(value, "%Y-%m-%d").date()
                        
                        setattr(result, key, value)
                
                # Auto-commits on exit
            
            return True
            
        except Exception as e:
            print(f"Error updating lab result: {e}")
            traceback.print_exc()
            return False
    
    # ========== DELETE OPERATIONS ==========
    
    def delete_lab_result(self, result_id: str) -> bool:
        """
        Delete lab result
        
        Args:
            result_id: Lab result ID
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with get_db_context() as db:
                result = db.query(LabResult).filter_by(result_id=result_id).first()
                if not result:
                    return False
                
                db.delete(result)
                # Auto-commits on exit
            
            return True
            
        except Exception as e:
            print(f"Error deleting lab result: {e}")
            traceback.print_exc()
            return False
    
    # ========== STATISTICS ==========
    
    def get_lab_result_count(self, national_id: Optional[str] = None) -> int:
        """
        Get lab result count, optionally for a specific patient
        
        Args:
            national_id: Optional patient national ID
        
        Returns:
            int: Number of lab results
        """
        with get_db_context() as db:
            query = db.query(LabResult)
            
            if national_id:
                query = query.filter_by(patient_national_id=national_id)
            
            return query.count()
    
    def get_abnormal_results(self, national_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all abnormal or critical lab results
        
        Args:
            national_id: Optional patient national ID to filter
        
        Returns:
            list: List of abnormal lab result dictionaries
        """
        with get_db_context() as db:
            query = db.query(LabResult).filter(
                (LabResult.status == 'abnormal') |
                (LabResult.status == 'critical')
            )
            
            if national_id:
                query = query.filter_by(patient_national_id=national_id)
            
            results = query.order_by(LabResult.test_date.desc()).all()
            
            # Convert all to dict inside session
            return [self._lab_result_to_dict(result) for result in results]
    
    # ========== HELPER METHODS ==========
    
    def _lab_result_to_dict(self, result: LabResult) -> Dict[str, Any]:
        """
        Convert LabResult model to dictionary for GUI compatibility
        Call this ONLY inside a database session context
        
        Args:
            result: LabResult SQLAlchemy model
        
        Returns:
            dict: Lab result data as dictionary
        """
        if not result:
            return None
        
        return {
            'result_id': result.result_id,
            'patient_national_id': result.patient_national_id,
            'test_date': str(result.test_date) if result.test_date else None,
            'test_name': result.test_name,
            'test_type': result.test_type,
            'result_value': result.result_value,
            'unit': result.unit,
            'reference_range': result.reference_range,
            'status': result.status,
            'laboratory': result.laboratory,
            'notes': result.notes,
            'attachments': result.attachments or [],
            'created_at': str(result.created_at) if result.created_at else None,
            'last_updated': str(result.last_updated) if result.last_updated else None
        }


# Singleton instance
_lab_manager = None

def get_lab_manager():
    """Get singleton instance of LabManager"""
    global _lab_manager
    if _lab_manager is None:
        _lab_manager = LabManager()
    return _lab_manager