"""
Vaccination manager - Handle patient vaccination records
Location: core/vaccination_manager.py
"""
from typing import List, Dict, Optional, Tuple
from core.data_manager import data_manager
from utils.date_utils import get_current_datetime
from utils.enhanced_validators import validate_vaccination_data
import uuid


class VaccinationManager:
    """Manages patient vaccination records"""
    
    def __init__(self):
        self.data_manager = data_manager
    
    def get_patient_vaccinations(self, national_id: str) -> List[Dict]:
        """
        Get all vaccinations for a patient, sorted by date (newest first)
        
        Args:
            national_id: Patient's national ID
        
        Returns:
            List of vaccination dictionaries
        """
        # Get patient data
        patient = self.data_manager.find_item('patients', 'patients', 'national_id', national_id)
        
        if not patient:
            return []
        
        vaccinations = patient.get('vaccinations', [])
        
        # Sort by date administered (newest first)
        return sorted(vaccinations, key=lambda x: x.get('date_administered', ''), reverse=True)
    
    def add_vaccination(self, national_id: str, vaccination_data: Dict) -> Tuple[bool, str]:
        """
        Add new vaccination record to patient
        
        Args:
            national_id: Patient's national ID
            vaccination_data: Vaccination information dictionary
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Validate vaccination data
            valid, msg = validate_vaccination_data(vaccination_data)
            if not valid:
                return False, f"Validation error: {msg}"
            
            # Add timestamp
            vaccination_data['created_at'] = get_current_datetime()
            
            # Get patient
            patient = self.data_manager.find_item('patients', 'patients', 'national_id', national_id)
            
            if not patient:
                return False, "Patient not found"
            
            # Initialize vaccinations list if it doesn't exist
            if 'vaccinations' not in patient:
                patient['vaccinations'] = []
            
            # Add vaccination to patient's list
            patient['vaccinations'].append(vaccination_data)
            
            # Update patient in database
            success = self.data_manager.update_item(
                'patients',
                'patients',
                national_id,
                'national_id',
                patient
            )
            
            if success:
                return True, f"Vaccination added successfully ({vaccination_data['vaccine_name']})"
            else:
                return False, "Failed to save vaccination"
        
        except Exception as e:
            return False, f"Error adding vaccination: {str(e)}"
    
    def update_vaccination(self, national_id: str, vaccine_index: int, 
                          vaccination_data: Dict) -> Tuple[bool, str]:
        """
        Update existing vaccination record
        
        Args:
            national_id: Patient's national ID
            vaccine_index: Index of vaccination in list
            vaccination_data: Updated vaccination information
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Validate vaccination data
            valid, msg = validate_vaccination_data(vaccination_data)
            if not valid:
                return False, f"Validation error: {msg}"
            
            # Get patient
            patient = self.data_manager.find_item('patients', 'patients', 'national_id', national_id)
            
            if not patient:
                return False, "Patient not found"
            
            # Get vaccinations
            vaccinations = patient.get('vaccinations', [])
            
            if vaccine_index < 0 or vaccine_index >= len(vaccinations):
                return False, "Vaccination index out of range"
            
            # Update vaccination
            vaccination_data['updated_at'] = get_current_datetime()
            vaccinations[vaccine_index] = vaccination_data
            
            # Update patient
            patient['vaccinations'] = vaccinations
            success = self.data_manager.update_item(
                'patients',
                'patients',
                national_id,
                'national_id',
                patient
            )
            
            if success:
                return True, "Vaccination updated successfully"
            else:
                return False, "Failed to update vaccination"
        
        except Exception as e:
            return False, f"Error updating vaccination: {str(e)}"
    
    def delete_vaccination(self, national_id: str, vaccine_index: int) -> Tuple[bool, str]:
        """
        Delete vaccination record
        
        Args:
            national_id: Patient's national ID
            vaccine_index: Index of vaccination to delete
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Get patient
            patient = self.data_manager.find_item('patients', 'patients', 'national_id', national_id)
            
            if not patient:
                return False, "Patient not found"
            
            # Get vaccinations
            vaccinations = patient.get('vaccinations', [])
            
            if vaccine_index < 0 or vaccine_index >= len(vaccinations):
                return False, "Vaccination index out of range"
            
            # Remove vaccination
            del vaccinations[vaccine_index]
            patient['vaccinations'] = vaccinations
            
            # Update patient
            success = self.data_manager.update_item(
                'patients',
                'patients',
                national_id,
                'national_id',
                patient
            )
            
            if success:
                return True, "Vaccination deleted successfully"
            else:
                return False, "Failed to delete vaccination"
        
        except Exception as e:
            return False, f"Error deleting vaccination: {str(e)}"
    
    def get_vaccinations_count(self, national_id: str) -> int:
        """Get total vaccination count for a patient"""
        vaccinations = self.get_patient_vaccinations(national_id)
        return len(vaccinations)
    
    def get_vaccinations_by_name(self, national_id: str, vaccine_name: str) -> List[Dict]:
        """Get all vaccinations of a specific type"""
        all_vaccinations = self.get_patient_vaccinations(national_id)
        
        return [v for v in all_vaccinations if vaccine_name.lower() in v.get('vaccine_name', '').lower()]
    
    def get_due_vaccinations(self, national_id: str) -> List[Dict]:
        """Get vaccinations with upcoming due dates"""
        from datetime import datetime
        
        all_vaccinations = self.get_patient_vaccinations(national_id)
        today = datetime.now()
        
        due_vaccines = []
        for vaccine in all_vaccinations:
            if vaccine.get('next_dose_due'):
                try:
                    due_date = datetime.strptime(vaccine['next_dose_due'], "%Y-%m-%d")
                    if due_date >= today:
                        due_vaccines.append(vaccine)
                except:
                    pass
        
        return due_vaccines
    
    def check_vaccination_status(self, national_id: str, vaccine_name: str) -> Dict:
        """
        Check vaccination status for a specific vaccine
        
        Returns:
            Dictionary with vaccination status information
        """
        vaccinations = self.get_vaccinations_by_name(national_id, vaccine_name)
        
        if not vaccinations:
            return {
                'vaccinated': False,
                'doses': 0,
                'last_dose_date': None,
                'next_dose_due': None
            }
        
        # Sort by date
        sorted_vaccines = sorted(vaccinations, 
                                key=lambda x: x.get('date_administered', ''), 
                                reverse=True)
        
        latest = sorted_vaccines[0]
        
        return {
            'vaccinated': True,
            'doses': len(vaccinations),
            'last_dose_date': latest.get('date_administered'),
            'next_dose_due': latest.get('next_dose_due'),
            'location': latest.get('location'),
            'batch_number': latest.get('batch_number')
        }


# Global instance
vaccination_manager = VaccinationManager()