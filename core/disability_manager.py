"""
Disability manager - Handle patient disability and special needs
Location: core/disability_manager.py
"""
from typing import Dict, Optional, Tuple
from core.data_manager import data_manager
from utils.date_utils import get_current_datetime
from utils.enhanced_validators import validate_disability_data


class DisabilityManager:
    """Manages patient disability and special needs information"""

    def __init__(self):
        self.data_manager = data_manager

    def get_disability_info(self, national_id: str) -> Optional[Dict]:
        """
        Get disability information for a patient

        Args:
            national_id: Patient's national ID

        Returns:
            Disability information dictionary or None
        """
        # Get patient data
        patient = self.data_manager.find_item(
            'patients', 'patients', 'national_id', national_id)

        if not patient:
            return None

        return patient.get('disabilities_special_needs', {})

    def update_disability_info(self, national_id: str, disability_data: Dict) -> Tuple[bool, str]:
        """
        Update complete disability and special needs information

        Args:
            national_id: Patient's national ID
            disability_data: Complete disability information dictionary

        Returns:
            (success: bool, message: str)
        """
        try:
            # Validate disability data
            valid, msg = validate_disability_data(disability_data)
            if not valid:
                return False, f"Validation error: {msg}"

            # Get patient
            patient = self.data_manager.find_item(
                'patients', 'patients', 'national_id', national_id)

            if not patient:
                return False, "Patient not found"

            # Add timestamp
            disability_data['last_updated'] = get_current_datetime()

            # Update disability information
            patient['disabilities_special_needs'] = disability_data

            # Update patient in database
            success = self.data_manager.update_item(
                'patients',
                'patients',
                national_id,
                'national_id',
                patient
            )

            if success:
                return True, "Disability information updated successfully"
            else:
                return False, "Failed to update disability information"

        except Exception as e:
            return False, f"Error updating disability info: {str(e)}"

    def set_has_disability(self, national_id: str, has_disability: bool) -> Tuple[bool, str]:
        """Update whether patient has a disability"""
        try:
            disability_info = self.get_disability_info(national_id) or {}
            disability_info['has_disability'] = has_disability

            # If setting to False, clear disability-specific fields
            if not has_disability:
                disability_info['disability_type'] = None
                disability_info['mobility_aids'] = []
                disability_info['hearing_impairment'] = False
                disability_info['visual_impairment'] = False
                disability_info['cognitive_impairment'] = False
                disability_info['communication_needs'] = []
                disability_info['accessibility_requirements'] = []
                disability_info['notes'] = None

            return self.update_disability_info(national_id, disability_info)
        except Exception as e:
            return False, f"Error setting disability status: {str(e)}"

    def add_mobility_aid(self, national_id: str, aid: str) -> Tuple[bool, str]:
        """Add mobility aid to patient's profile"""
        try:
            disability_info = self.get_disability_info(national_id) or {}

            if not disability_info.get('has_disability'):
                return False, "Patient must be marked as having a disability first"

            if 'mobility_aids' not in disability_info:
                disability_info['mobility_aids'] = []

            if aid not in disability_info['mobility_aids']:
                disability_info['mobility_aids'].append(aid)

            return self.update_disability_info(national_id, disability_info)
        except Exception as e:
            return False, f"Error adding mobility aid: {str(e)}"

    def remove_mobility_aid(self, national_id: str, aid: str) -> Tuple[bool, str]:
        """Remove mobility aid from patient's profile"""
        try:
            disability_info = self.get_disability_info(national_id) or {}

            if 'mobility_aids' in disability_info and aid in disability_info['mobility_aids']:
                disability_info['mobility_aids'].remove(aid)
                return self.update_disability_info(national_id, disability_info)

            return False, "Mobility aid not found"
        except Exception as e:
            return False, f"Error removing mobility aid: {str(e)}"

    def add_communication_need(self, national_id: str, need: str) -> Tuple[bool, str]:
        """Add communication need to patient's profile"""
        try:
            disability_info = self.get_disability_info(national_id) or {}

            if not disability_info.get('has_disability'):
                return False, "Patient must be marked as having a disability first"

            if 'communication_needs' not in disability_info:
                disability_info['communication_needs'] = []

            if need not in disability_info['communication_needs']:
                disability_info['communication_needs'].append(need)

            return self.update_disability_info(national_id, disability_info)
        except Exception as e:
            return False, f"Error adding communication need: {str(e)}"

    def add_accessibility_requirement(self, national_id: str, requirement: str) -> Tuple[bool, str]:
        """Add accessibility requirement to patient's profile"""
        try:
            disability_info = self.get_disability_info(national_id) or {}

            if not disability_info.get('has_disability'):
                return False, "Patient must be marked as having a disability first"

            if 'accessibility_requirements' not in disability_info:
                disability_info['accessibility_requirements'] = []

            if requirement not in disability_info['accessibility_requirements']:
                disability_info['accessibility_requirements'].append(
                    requirement)

            return self.update_disability_info(national_id, disability_info)
        except Exception as e:
            return False, f"Error adding accessibility requirement: {str(e)}"

    def get_accessibility_summary(self, national_id: str) -> Dict:
        """
        Get accessibility requirements summary

        Args:
            national_id: Patient's national ID

        Returns:
            Dictionary with accessibility summary
        """
        disability_info = self.get_disability_info(national_id)

        if not disability_info or not disability_info.get('has_disability'):
            return {
                'has_disability': False,
                'summary': []
            }

        summary = []

        # Mobility aids
        if disability_info.get('mobility_aids'):
            aids = ', '.join(disability_info['mobility_aids'])
            summary.append(f"Uses mobility aids: {aids}")

        # Impairments
        if disability_info.get('hearing_impairment'):
            summary.append("Hearing impairment")
        if disability_info.get('visual_impairment'):
            summary.append("Visual impairment")
        if disability_info.get('cognitive_impairment'):
            summary.append("Cognitive impairment")

        # Communication needs
        if disability_info.get('communication_needs'):
            needs = ', '.join(disability_info['communication_needs'])
            summary.append(f"Communication support: {needs}")

        # Accessibility requirements
        if disability_info.get('accessibility_requirements'):
            reqs = ', '.join(disability_info['accessibility_requirements'])
            summary.append(f"Requires: {reqs}")

        return {
            'has_disability': True,
            'disability_type': disability_info.get('disability_type'),
            'needs_accommodations': len(summary) > 0,
            'summary': summary,
            'mobility_aids': disability_info.get('mobility_aids', []),
            'communication_needs': disability_info.get('communication_needs', []),
            'accessibility_requirements': disability_info.get('accessibility_requirements', [])
        }

    def check_special_requirements(self, national_id: str) -> Dict:
        """
        Check if patient has any special requirements for medical care

        Returns:
            Dictionary with flags for various special needs
        """
        disability_info = self.get_disability_info(national_id)

        if not disability_info or not disability_info.get('has_disability'):
            return {
                'has_special_needs': False,
                'requires_wheelchair_access': False,
                'requires_interpreter': False,
                'requires_assistance': False,
                'has_communication_barrier': False
            }

        mobility_aids = disability_info.get('mobility_aids', [])
        communication_needs = disability_info.get('communication_needs', [])

        return {
            'has_special_needs': True,
            'requires_wheelchair_access': 'Wheelchair' in mobility_aids,
            'requires_interpreter': any('interpreter' in need.lower() for need in communication_needs),
            'requires_assistance': len(mobility_aids) > 0,
            'has_communication_barrier': (
                disability_info.get('hearing_impairment', False) or
                len(communication_needs) > 0
            ),
            'has_visual_impairment': disability_info.get('visual_impairment', False),
            'has_cognitive_impairment': disability_info.get('cognitive_impairment', False)
        }


# Global instance
disability_manager = DisabilityManager()
