"""
Imaging Manager
Manages imaging results and radiology studies
Location: core/imaging_manager.py
"""
from database.connection import get_db_context
from database.models import ImagingResult
from datetime import datetime, date
from typing import Optional, List, Dict, Any
import traceback


class ImagingManager:
    """
    Imaging Manager - Manages radiology imaging results
    
    Features:
    - Get all imaging results
    - Get imaging results by patient
    - Add new imaging result
    - Update imaging result
    - Delete imaging result
    - Get imaging result by ID
    - Search imaging results
    - Get results by date range
    - Get results by imaging type
    """
    
    def __init__(self):
        """Initialize Imaging Manager"""
        pass
    
    # ========== READ OPERATIONS ==========
    
    def get_all_imaging_results(self) -> List[Dict[str, Any]]:
        """
        Get all imaging results
        
        Returns:
            list: List of imaging result dictionaries, ordered by date descending
        """
        with get_db_context() as db:
            results = db.query(ImagingResult).order_by(ImagingResult.imaging_date.desc()).all()
            # Convert all to dict inside session
            return [self._imaging_result_to_dict(result) for result in results]
    
    def get_patient_imaging_results(self, national_id: str) -> List[Dict[str, Any]]:
        """
        Get all imaging results for a patient
        
        Args:
            national_id: Patient's national ID
        
        Returns:
            list: List of imaging result dictionaries, ordered by date descending
        """
        with get_db_context() as db:
            results = db.query(ImagingResult)\
                .filter_by(patient_national_id=national_id)\
                .order_by(ImagingResult.imaging_date.desc())\
                .all()
            
            # Convert all to dict inside session
            return [self._imaging_result_to_dict(result) for result in results]
    
    def get_imaging_result(self, imaging_id: str) -> Optional[Dict[str, Any]]:
        """
        Get imaging result by ID
        
        Args:
            imaging_id: Imaging result ID
        
        Returns:
            dict: Imaging result data if found, None otherwise
        """
        with get_db_context() as db:
            result = db.query(ImagingResult).filter_by(imaging_id=imaging_id).first()
            if result:
                return self._imaging_result_to_dict(result)
        return None
    
    def search_imaging_results(self, query: str) -> List[Dict[str, Any]]:
        """
        Search imaging results by imaging type, body part, or patient national ID
        
        Args:
            query: Search string
        
        Returns:
            list: List of matching imaging result dictionaries
        """
        with get_db_context() as db:
            results = db.query(ImagingResult).filter(
                (ImagingResult.imaging_type.contains(query)) |
                (ImagingResult.body_part.contains(query)) |
                (ImagingResult.patient_national_id.contains(query))
            ).order_by(ImagingResult.imaging_date.desc()).all()
            
            # Convert all to dict inside session
            return [self._imaging_result_to_dict(result) for result in results]
    
    def get_imaging_results_by_date_range(
        self, 
        start_date: Any, 
        end_date: Any,
        national_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get imaging results within a date range
        
        Args:
            start_date: Start date (string or date object)
            end_date: End date (string or date object)
            national_id: Optional patient national ID to filter
        
        Returns:
            list: List of imaging result dictionaries
        """
        # Parse dates if strings
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        with get_db_context() as db:
            query = db.query(ImagingResult)\
                .filter(ImagingResult.imaging_date >= start_date)\
                .filter(ImagingResult.imaging_date <= end_date)
            
            if national_id:
                query = query.filter_by(patient_national_id=national_id)
            
            results = query.order_by(ImagingResult.imaging_date.desc()).all()
            
            # Convert all to dict inside session
            return [self._imaging_result_to_dict(result) for result in results]
    
    def get_imaging_results_by_type(
        self, 
        imaging_type: str,
        national_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all results for a specific imaging type
        
        Args:
            imaging_type: Type of imaging (e.g., "X-Ray", "CT", "MRI", "Ultrasound")
            national_id: Optional patient national ID to filter
        
        Returns:
            list: List of imaging result dictionaries
        """
        with get_db_context() as db:
            query = db.query(ImagingResult).filter(
                ImagingResult.imaging_type.contains(imaging_type)
            )
            
            if national_id:
                query = query.filter_by(patient_national_id=national_id)
            
            results = query.order_by(ImagingResult.imaging_date.desc()).all()
            
            # Convert all to dict inside session
            return [self._imaging_result_to_dict(result) for result in results]
    
    def get_imaging_results_by_body_part(
        self, 
        body_part: str,
        national_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all imaging results for a specific body part
        
        Args:
            body_part: Body part (e.g., "Chest", "Head", "Abdomen")
            national_id: Optional patient national ID to filter
        
        Returns:
            list: List of imaging result dictionaries
        """
        with get_db_context() as db:
            query = db.query(ImagingResult).filter(
                ImagingResult.body_part.contains(body_part)
            )
            
            if national_id:
                query = query.filter_by(patient_national_id=national_id)
            
            results = query.order_by(ImagingResult.imaging_date.desc()).all()
            
            # Convert all to dict inside session
            return [self._imaging_result_to_dict(result) for result in results]
    
    # ========== CREATE OPERATIONS ==========
    
    def add_imaging_result(self, result_data: Dict[str, Any]) -> Optional[str]:
        """
        Add new imaging result
        
        Args:
            result_data: Dictionary with imaging result data
                Required fields:
                - patient_national_id: str
                - imaging_date: date or str
                - imaging_type: str (X-Ray, CT, MRI, Ultrasound, etc.)
                - body_part: str
                Optional fields:
                - findings: str
                - impression: str
                - radiologist: str
                - facility: str
                - notes: str
                - attachments: list
        
        Returns:
            str: Imaging ID if successful, None otherwise
        """
        try:
            with get_db_context() as db:
                # Parse date if string
                imaging_date = result_data.get('imaging_date')
                if isinstance(imaging_date, str):
                    imaging_date = datetime.strptime(imaging_date, "%Y-%m-%d").date()
                
                # Create new result
                imaging_result = ImagingResult(
                    patient_national_id=result_data['patient_national_id'],
                    imaging_date=imaging_date,
                    imaging_type=result_data['imaging_type'],
                    body_part=result_data['body_part'],
                    findings=result_data.get('findings'),
                    impression=result_data.get('impression'),
                    radiologist=result_data.get('radiologist'),
                    facility=result_data.get('facility'),
                    notes=result_data.get('notes'),
                    attachments=result_data.get('attachments', [])
                )
                
                db.add(imaging_result)
                db.flush()  # Get the ID before commit
                
                imaging_id = imaging_result.imaging_id
                
                # Auto-commits on exit
            
            return imaging_id
            
        except Exception as e:
            print(f"Error adding imaging result: {e}")
            traceback.print_exc()
            return None
    
    # ========== UPDATE OPERATIONS ==========
    
    def update_imaging_result(self, imaging_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update imaging result
        
        Args:
            imaging_id: Imaging result ID
            updates: Dictionary of fields to update
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with get_db_context() as db:
                result = db.query(ImagingResult).filter_by(imaging_id=imaging_id).first()
                if not result:
                    return False
                
                # Update fields
                for key, value in updates.items():
                    if hasattr(result, key):
                        # Parse date if needed
                        if key == 'imaging_date' and isinstance(value, str):
                            value = datetime.strptime(value, "%Y-%m-%d").date()
                        
                        setattr(result, key, value)
                
                # Auto-commits on exit
            
            return True
            
        except Exception as e:
            print(f"Error updating imaging result: {e}")
            traceback.print_exc()
            return False
    
    # ========== DELETE OPERATIONS ==========
    
    def delete_imaging_result(self, imaging_id: str) -> bool:
        """
        Delete imaging result
        
        Args:
            imaging_id: Imaging result ID
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with get_db_context() as db:
                result = db.query(ImagingResult).filter_by(imaging_id=imaging_id).first()
                if not result:
                    return False
                
                db.delete(result)
                # Auto-commits on exit
            
            return True
            
        except Exception as e:
            print(f"Error deleting imaging result: {e}")
            traceback.print_exc()
            return False
    
    # ========== STATISTICS ==========
    
    def get_imaging_result_count(self, national_id: Optional[str] = None) -> int:
        """
        Get imaging result count, optionally for a specific patient
        
        Args:
            national_id: Optional patient national ID
        
        Returns:
            int: Number of imaging results
        """
        with get_db_context() as db:
            query = db.query(ImagingResult)
            
            if national_id:
                query = query.filter_by(patient_national_id=national_id)
            
            return query.count()
    
    def get_imaging_type_statistics(self, national_id: Optional[str] = None) -> Dict[str, int]:
        """
        Get count of each imaging type
        
        Args:
            national_id: Optional patient national ID to filter
        
        Returns:
            dict: Dictionary with imaging type as key and count as value
        """
        with get_db_context() as db:
            query = db.query(ImagingResult)
            
            if national_id:
                query = query.filter_by(patient_national_id=national_id)
            
            results = query.all()
            
            # Count by type
            stats = {}
            for result in results:
                imaging_type = result.imaging_type or 'Unknown'
                stats[imaging_type] = stats.get(imaging_type, 0) + 1
            
            return stats
    
    # ========== HELPER METHODS ==========
    
    def _imaging_result_to_dict(self, result: ImagingResult) -> Dict[str, Any]:
        """
        Convert ImagingResult model to dictionary for GUI compatibility
        Call this ONLY inside a database session context
        
        Args:
            result: ImagingResult SQLAlchemy model
        
        Returns:
            dict: Imaging result data as dictionary
        """
        if not result:
            return None
        
        return {
            'imaging_id': result.imaging_id,
            'patient_national_id': result.patient_national_id,
            'imaging_date': str(result.imaging_date) if result.imaging_date else None,
            'imaging_type': result.imaging_type,
            'body_part': result.body_part,
            'findings': result.findings,
            'impression': result.impression,
            'radiologist': result.radiologist,
            'facility': result.facility,
            'notes': result.notes,
            'attachments': result.attachments or [],
            'created_at': str(result.created_at) if result.created_at else None,
            'last_updated': str(result.last_updated) if result.last_updated else None
        }


# Singleton instance
_imaging_manager = None

def get_imaging_manager():
    """Get singleton instance of ImagingManager"""
    global _imaging_manager
    if _imaging_manager is None:
        _imaging_manager = ImagingManager()
    return _imaging_manager