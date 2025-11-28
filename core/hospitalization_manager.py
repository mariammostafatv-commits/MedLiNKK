"""
Hospitalization manager - Handle patient hospitalization records
Location: core/hospitalization_manager.py
"""
from typing import List, Dict, Optional, Tuple
from core.data_manager import data_manager
from utils.date_utils import get_current_datetime
from utils.enhanced_validators import validate_hospitalization_data
import uuid


class HospitalizationManager:
    """Manages patient hospitalization records"""
    
    def __init__(self):
        self.data_manager = data_manager
    
    def get_patient_hospitalizations(self, national_id: str) -> List[Dict]:
        """
        Get all hospitalizations for a patient, sorted by admission date (newest first)
        
        Args:
            national_id: Patient's national ID
        
        Returns:
            List of hospitalization dictionaries
        """
        # Get patient data
        patient = self.data_manager.find_item('patients', 'patients', 'national_id', national_id)
        
        if not patient:
            return []
        
        hospitalizations = patient.get('hospitalizations', [])
        
        # Sort by admission date (newest first)
        return sorted(hospitalizations, key=lambda x: x.get('admission_date', ''), reverse=True)
    
    def get_hospitalization_by_id(self, national_id: str, hospitalization_id: str) -> Optional[Dict]:
        """Get single hospitalization by ID"""
        hospitalizations = self.get_patient_hospitalizations(national_id)
        
        for hosp in hospitalizations:
            if hosp.get('hospitalization_id') == hospitalization_id:
                return hosp
        
        return None
    
    def add_hospitalization(self, national_id: str, hospitalization_data: Dict) -> Tuple[bool, str]:
        """
        Add new hospitalization record to patient
        
        Args:
            national_id: Patient's national ID
            hospitalization_data: Hospitalization information dictionary
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Validate hospitalization data
            valid, msg = validate_hospitalization_data(hospitalization_data)
            if not valid:
                return False, f"Validation error: {msg}"
            
            # Generate hospitalization ID if not provided
            if 'hospitalization_id' not in hospitalization_data:
                hospitalization_data['hospitalization_id'] = f"HSP{uuid.uuid4().hex[:8].upper()}"
            
            # Add timestamp
            hospitalization_data['created_at'] = get_current_datetime()
            
            # Get patient
            patient = self.data_manager.find_item('patients', 'patients', 'national_id', national_id)
            
            if not patient:
                return False, "Patient not found"
            
            # Initialize hospitalizations list if it doesn't exist
            if 'hospitalizations' not in patient:
                patient['hospitalizations'] = []
            
            # Add hospitalization to patient's list
            patient['hospitalizations'].append(hospitalization_data)
            
            # Update patient in database
            success = self.data_manager.update_item(
                'patients',
                'patients',
                national_id,
                'national_id',
                patient
            )
            
            if success:
                return True, f"Hospitalization added successfully (ID: {hospitalization_data['hospitalization_id']})"
            else:
                return False, "Failed to save hospitalization"
        
        except Exception as e:
            return False, f"Error adding hospitalization: {str(e)}"
    
    def update_hospitalization(self, national_id: str, hospitalization_id: str, 
                              hospitalization_data: Dict) -> Tuple[bool, str]:
        """
        Update existing hospitalization record
        
        Args:
            national_id: Patient's national ID
            hospitalization_id: Hospitalization ID to update
            hospitalization_data: Updated hospitalization information
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Validate hospitalization data
            valid, msg = validate_hospitalization_data(hospitalization_data)
            if not valid:
                return False, f"Validation error: {msg}"
            
            # Get patient
            patient = self.data_manager.find_item('patients', 'patients', 'national_id', national_id)
            
            if not patient:
                return False, "Patient not found"
            
            # Find and update hospitalization
            hospitalizations = patient.get('hospitalizations', [])
            hosp_found = False
            
            for i, hosp in enumerate(hospitalizations):
                if hosp.get('hospitalization_id') == hospitalization_id:
                    # Keep the original ID and created_at
                    hospitalization_data['hospitalization_id'] = hospitalization_id
                    hospitalization_data['created_at'] = hosp.get('created_at', get_current_datetime())
                    hospitalization_data['updated_at'] = get_current_datetime()
                    
                    hospitalizations[i] = hospitalization_data
                    hosp_found = True
                    break
            
            if not hosp_found:
                return False, "Hospitalization not found"
            
            # Update patient
            patient['hospitalizations'] = hospitalizations
            success = self.data_manager.update_item(
                'patients',
                'patients',
                national_id,
                'national_id',
                patient
            )
            
            if success:
                return True, "Hospitalization updated successfully"
            else:
                return False, "Failed to update hospitalization"
        
        except Exception as e:
            return False, f"Error updating hospitalization: {str(e)}"
    
    def delete_hospitalization(self, national_id: str, hospitalization_id: str) -> Tuple[bool, str]:
        """
        Delete hospitalization record
        
        Args:
            national_id: Patient's national ID
            hospitalization_id: Hospitalization ID to delete
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Get patient
            patient = self.data_manager.find_item('patients', 'patients', 'national_id', national_id)
            
            if not patient:
                return False, "Patient not found"
            
            # Remove hospitalization
            hospitalizations = patient.get('hospitalizations', [])
            initial_count = len(hospitalizations)
            
            patient['hospitalizations'] = [h for h in hospitalizations 
                                          if h.get('hospitalization_id') != hospitalization_id]
            
            if len(patient['hospitalizations']) == initial_count:
                return False, "Hospitalization not found"
            
            # Update patient
            success = self.data_manager.update_item(
                'patients',
                'patients',
                national_id,
                'national_id',
                patient
            )
            
            if success:
                return True, "Hospitalization deleted successfully"
            else:
                return False, "Failed to delete hospitalization"
        
        except Exception as e:
            return False, f"Error deleting hospitalization: {str(e)}"
    
    def get_hospitalizations_count(self, national_id: str) -> int:
        """Get total hospitalization count for a patient"""
        hospitalizations = self.get_patient_hospitalizations(national_id)
        return len(hospitalizations)
    
    def calculate_length_of_stay(self, hospitalization: Dict) -> Optional[int]:
        """Calculate length of stay in days"""
        try:
            from datetime import datetime
            
            admission = datetime.strptime(hospitalization['admission_date'], "%Y-%m-%d")
            discharge = datetime.strptime(hospitalization['discharge_date'], "%Y-%m-%d")
            
            return (discharge - admission).days
        except:
            return None
    
    def get_recent_hospitalizations(self, national_id: str, limit: int = 5) -> List[Dict]:
        """Get most recent hospitalizations"""
        hospitalizations = self.get_patient_hospitalizations(national_id)
        return hospitalizations[:limit]


# Global instance
hospitalization_manager = HospitalizationManager()