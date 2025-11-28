"""
Family history manager - Handle patient family medical history
Location: core/family_history_manager.py
"""
from typing import Dict, Optional, Tuple
from core.data_manager import data_manager
from utils.date_utils import get_current_datetime
from utils.enhanced_validators import validate_family_history


class FamilyHistoryManager:
    """Manages patient family medical history"""
    
    def __init__(self):
        self.data_manager = data_manager
    
    def get_family_history(self, national_id: str) -> Optional[Dict]:
        """
        Get family medical history for a patient
        
        Args:
            national_id: Patient's national ID
        
        Returns:
            Family history dictionary or None
        """
        # Get patient data
        patient = self.data_manager.find_item('patients', 'patients', 'national_id', national_id)
        
        if not patient:
            return None
        
        return patient.get('family_history', {})
    
    def update_family_history(self, national_id: str, family_history_data: Dict) -> Tuple[bool, str]:
        """
        Update complete family medical history
        
        Args:
            national_id: Patient's national ID
            family_history_data: Complete family history dictionary
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Validate family history data
            valid, msg = validate_family_history(family_history_data)
            if not valid:
                return False, f"Validation error: {msg}"
            
            # Get patient
            patient = self.data_manager.find_item('patients', 'patients', 'national_id', national_id)
            
            if not patient:
                return False, "Patient not found"
            
            # Add timestamp
            family_history_data['last_updated'] = get_current_datetime()
            
            # Update family history
            patient['family_history'] = family_history_data
            
            # Update patient in database
            success = self.data_manager.update_item(
                'patients',
                'patients',
                national_id,
                'national_id',
                patient
            )
            
            if success:
                return True, "Family history updated successfully"
            else:
                return False, "Failed to update family history"
        
        except Exception as e:
            return False, f"Error updating family history: {str(e)}"
    
    def update_father_info(self, national_id: str, father_data: Dict) -> Tuple[bool, str]:
        """Update father's medical information"""
        try:
            family_history = self.get_family_history(national_id) or {}
            family_history['father'] = father_data
            
            return self.update_family_history(national_id, family_history)
        except Exception as e:
            return False, f"Error updating father info: {str(e)}"
    
    def update_mother_info(self, national_id: str, mother_data: Dict) -> Tuple[bool, str]:
        """Update mother's medical information"""
        try:
            family_history = self.get_family_history(national_id) or {}
            family_history['mother'] = mother_data
            
            return self.update_family_history(national_id, family_history)
        except Exception as e:
            return False, f"Error updating mother info: {str(e)}"
    
    def add_sibling(self, national_id: str, sibling_data: Dict) -> Tuple[bool, str]:
        """Add sibling to family history"""
        try:
            family_history = self.get_family_history(national_id) or {}
            
            if 'siblings' not in family_history:
                family_history['siblings'] = []
            
            family_history['siblings'].append(sibling_data)
            
            return self.update_family_history(national_id, family_history)
        except Exception as e:
            return False, f"Error adding sibling: {str(e)}"
    
    def remove_sibling(self, national_id: str, sibling_index: int) -> Tuple[bool, str]:
        """Remove sibling from family history"""
        try:
            family_history = self.get_family_history(national_id) or {}
            
            if 'siblings' not in family_history:
                return False, "No siblings found"
            
            siblings = family_history['siblings']
            
            if sibling_index < 0 or sibling_index >= len(siblings):
                return False, "Invalid sibling index"
            
            del siblings[sibling_index]
            family_history['siblings'] = siblings
            
            return self.update_family_history(national_id, family_history)
        except Exception as e:
            return False, f"Error removing sibling: {str(e)}"
    
    def update_genetic_conditions(self, national_id: str, genetic_conditions: list) -> Tuple[bool, str]:
        """Update genetic conditions list"""
        try:
            family_history = self.get_family_history(national_id) or {}
            family_history['genetic_conditions'] = genetic_conditions
            
            return self.update_family_history(national_id, family_history)
        except Exception as e:
            return False, f"Error updating genetic conditions: {str(e)}"
    
    def get_genetic_risk_summary(self, national_id: str) -> Dict:
        """
        Get summary of genetic risks based on family history
        
        Returns:
            Dictionary with risk analysis
        """
        family_history = self.get_family_history(national_id)
        
        if not family_history:
            return {
                'has_family_history': False,
                'risk_factors': [],
                'genetic_conditions': []
            }
        
        risk_factors = []
        
        # Check father's conditions
        if 'father' in family_history:
            father = family_history['father']
            if father.get('medical_conditions'):
                risk_factors.extend(father['medical_conditions'])
        
        # Check mother's conditions
        if 'mother' in family_history:
            mother = family_history['mother']
            if mother.get('medical_conditions'):
                risk_factors.extend(mother['medical_conditions'])
        
        # Check siblings' conditions
        if 'siblings' in family_history:
            for sibling in family_history['siblings']:
                if sibling.get('medical_conditions'):
                    risk_factors.extend(sibling['medical_conditions'])
        
        # Get unique risk factors
        risk_factors = list(set(risk_factors))
        
        return {
            'has_family_history': True,
            'risk_factors': risk_factors,
            'genetic_conditions': family_history.get('genetic_conditions', []),
            'total_relatives_tracked': (
                (1 if 'father' in family_history else 0) +
                (1 if 'mother' in family_history else 0) +
                len(family_history.get('siblings', []))
            )
        }
    
    def check_hereditary_condition(self, national_id: str, condition: str) -> Dict:
        """
        Check if a specific condition runs in the family
        
        Returns:
            Dictionary with information about hereditary pattern
        """
        family_history = self.get_family_history(national_id)
        
        if not family_history:
            return {
                'found': False,
                'affected_relatives': []
            }
        
        affected_relatives = []
        condition_lower = condition.lower()
        
        # Check father
        if 'father' in family_history:
            father = family_history['father']
            for cond in father.get('medical_conditions', []):
                if condition_lower in cond.lower():
                    affected_relatives.append('Father')
                    break
        
        # Check mother
        if 'mother' in family_history:
            mother = family_history['mother']
            for cond in mother.get('medical_conditions', []):
                if condition_lower in cond.lower():
                    affected_relatives.append('Mother')
                    break
        
        # Check siblings
        if 'siblings' in family_history:
            for i, sibling in enumerate(family_history['siblings'], 1):
                for cond in sibling.get('medical_conditions', []):
                    if condition_lower in cond.lower():
                        affected_relatives.append(f"{sibling.get('relation', 'Sibling')} {i}")
                        break
        
        return {
            'found': len(affected_relatives) > 0,
            'affected_relatives': affected_relatives,
            'count': len(affected_relatives)
        }


# Global instance
family_history_manager = FamilyHistoryManager()