"""
Surgery manager - Handle patient surgery records
Location: core/surgery_manager.py
"""
from typing import List, Dict, Optional, Tuple
from core.data_manager import data_manager
from utils.date_utils import get_current_datetime
from utils.enhanced_validators import validate_surgery_data
import uuid


class SurgeryManager:
    """Manages patient surgery records"""
    
    def __init__(self):
        self.data_manager = data_manager
    
    def get_patient_surgeries(self, national_id: str) -> List[Dict]:
        """
        Get all surgeries for a patient, sorted by date (newest first)
        
        Args:
            national_id: Patient's national ID
        
        Returns:
            List of surgery dictionaries
        """
        # Get patient data
        patient = self.data_manager.find_item('patients', 'patients', 'national_id', national_id)
        
        if not patient:
            return []
        
        surgeries = patient.get('surgeries', [])
        
        # Sort by date (newest first)
        return sorted(surgeries, key=lambda x: x.get('date', ''), reverse=True)
    
    def get_surgery_by_id(self, national_id: str, surgery_id: str) -> Optional[Dict]:
        """Get single surgery by ID"""
        surgeries = self.get_patient_surgeries(national_id)
        
        for surgery in surgeries:
            if surgery.get('surgery_id') == surgery_id:
                return surgery
        
        return None
    
    def add_surgery(self, national_id: str, surgery_data: Dict) -> Tuple[bool, str]:
        """
        Add new surgery record to patient
        
        Args:
            national_id: Patient's national ID
            surgery_data: Surgery information dictionary
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Validate surgery data
            valid, msg = validate_surgery_data(surgery_data)
            if not valid:
                return False, f"Validation error: {msg}"
            
            # Generate surgery ID if not provided
            if 'surgery_id' not in surgery_data:
                surgery_data['surgery_id'] = f"SRG{uuid.uuid4().hex[:8].upper()}"
            
            # Add timestamp
            surgery_data['created_at'] = get_current_datetime()
            
            # Get patient
            patient = self.data_manager.find_item('patients', 'patients', 'national_id', national_id)
            
            if not patient:
                return False, "Patient not found"
            
            # Initialize surgeries list if it doesn't exist
            if 'surgeries' not in patient:
                patient['surgeries'] = []
            
            # Add surgery to patient's surgeries list
            patient['surgeries'].append(surgery_data)
            
            # Update patient in database
            success = self.data_manager.update_item(
                'patients',
                'patients',
                national_id,
                'national_id',
                patient
            )
            
            if success:
                return True, f"Surgery added successfully (ID: {surgery_data['surgery_id']})"
            else:
                return False, "Failed to save surgery"
        
        except Exception as e:
            return False, f"Error adding surgery: {str(e)}"
    
    def update_surgery(self, national_id: str, surgery_id: str, surgery_data: Dict) -> Tuple[bool, str]:
        """
        Update existing surgery record
        
        Args:
            national_id: Patient's national ID
            surgery_id: Surgery ID to update
            surgery_data: Updated surgery information
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Validate surgery data
            valid, msg = validate_surgery_data(surgery_data)
            if not valid:
                return False, f"Validation error: {msg}"
            
            # Get patient
            patient = self.data_manager.find_item('patients', 'patients', 'national_id', national_id)
            
            if not patient:
                return False, "Patient not found"
            
            # Find and update surgery
            surgeries = patient.get('surgeries', [])
            surgery_found = False
            
            for i, surgery in enumerate(surgeries):
                if surgery.get('surgery_id') == surgery_id:
                    # Keep the original surgery_id and created_at
                    surgery_data['surgery_id'] = surgery_id
                    surgery_data['created_at'] = surgery.get('created_at', get_current_datetime())
                    surgery_data['updated_at'] = get_current_datetime()
                    
                    surgeries[i] = surgery_data
                    surgery_found = True
                    break
            
            if not surgery_found:
                return False, "Surgery not found"
            
            # Update patient
            patient['surgeries'] = surgeries
            success = self.data_manager.update_item(
                'patients',
                'patients',
                national_id,
                'national_id',
                patient
            )
            
            if success:
                return True, "Surgery updated successfully"
            else:
                return False, "Failed to update surgery"
        
        except Exception as e:
            return False, f"Error updating surgery: {str(e)}"
    
    def delete_surgery(self, national_id: str, surgery_id: str) -> Tuple[bool, str]:
        """
        Delete surgery record
        
        Args:
            national_id: Patient's national ID
            surgery_id: Surgery ID to delete
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Get patient
            patient = self.data_manager.find_item('patients', 'patients', 'national_id', national_id)
            
            if not patient:
                return False, "Patient not found"
            
            # Remove surgery
            surgeries = patient.get('surgeries', [])
            initial_count = len(surgeries)
            
            patient['surgeries'] = [s for s in surgeries if s.get('surgery_id') != surgery_id]
            
            if len(patient['surgeries']) == initial_count:
                return False, "Surgery not found"
            
            # Update patient
            success = self.data_manager.update_item(
                'patients',
                'patients',
                national_id,
                'national_id',
                patient
            )
            
            if success:
                return True, "Surgery deleted successfully"
            else:
                return False, "Failed to delete surgery"
        
        except Exception as e:
            return False, f"Error deleting surgery: {str(e)}"
    
    def get_surgeries_count(self, national_id: str) -> int:
        """Get total surgery count for a patient"""
        surgeries = self.get_patient_surgeries(national_id)
        return len(surgeries)
    
    def get_surgeries_by_procedure(self, national_id: str, procedure: str) -> List[Dict]:
        """Get surgeries filtered by procedure type"""
        all_surgeries = self.get_patient_surgeries(national_id)
        
        return [s for s in all_surgeries if procedure.lower() in s.get('procedure', '').lower()]
    
    def get_recent_surgeries(self, national_id: str, limit: int = 5) -> List[Dict]:
        """Get most recent surgeries"""
        surgeries = self.get_patient_surgeries(national_id)
        return surgeries[:limit]


# Global instance
surgery_manager = SurgeryManager()