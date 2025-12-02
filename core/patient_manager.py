"""
Patient manager - Handle patient data operations
"""
from typing import Optional, List, Dict
from core.data_manager import data_manager
from datetime import datetime


class PatientManager:
    """Manages patient records and operations"""
    
    def __init__(self):
        self.data_manager = data_manager
    
    def get_patient_by_id(self, national_id: str) -> Optional[Dict]:
        """Get patient by national ID"""
        return self.data_manager.find_item('patients', 'patients', 'national_id', national_id)
    
    def get_all_patients(self) -> List[Dict]:
        """Get all patients"""
        data = self.data_manager.load_data('patients')
        return data.get('patients', [])
    
    def search_patients(self, query: str) -> List[Dict]:
        """Search patients by name or ID"""
        all_patients = self.get_all_patients()
        query = query.lower()
        
        results = []
        for patient in all_patients:
            # Search in national ID
            if query in patient.get('national_id', '').lower():
                results.append(patient)
            # Search in full name
            elif query in patient.get('full_name', '').lower():
                results.append(patient)
        
        return results
    
    def get_patient_visits(self, national_id: str) -> List[Dict]:
        """Get all visits for a patient"""
        visits = self.data_manager.find_items('visits', 'visits', 'patient_national_id', national_id)
        # Sort by date (newest first)
        return sorted(visits, key=lambda x: x.get('date', ''), reverse=True)
    
    def get_patient_lab_results(self, national_id: str) -> List[Dict]:
        """Get lab results for a patient"""
        results = self.data_manager.find_items('lab_results', 'lab_results', 'patient_national_id', national_id)
        return sorted(results, key=lambda x: x.get('date', ''), reverse=True)
    
    def get_patient_imaging_results(self, national_id: str) -> List[Dict]:
        """Get imaging results for a patient"""
        results = self.data_manager.find_items('imaging_results', 'imaging_results', 'patient_national_id', national_id)
        return sorted(results, key=lambda x: x.get('date', ''), reverse=True)
    
    def add_patient(self, patient_data: Dict) -> bool:
        """Add new patient"""
        return self.data_manager.add_item('patients', 'patients', patient_data)
    
    def update_patient(self, national_id: str, patient_data: Dict) -> bool:
        """Update patient information"""
        return self.data_manager.update_item('patients', 'patients', national_id, 'national_id', patient_data)
    
    def get_patient_summary(self, national_id: str) -> Dict:
        """Get comprehensive patient summary"""
        patient = self.get_patient_by_id(national_id)
        if not patient:
            return {}
        
        visits = self.get_patient_visits(national_id)
        lab_results = self.get_patient_lab_results(national_id)
        imaging = self.get_patient_imaging_results(national_id)
        
        return {
            'patient': patient,
            'total_visits': len(visits),
            'recent_visits': visits[:5] if visits else [],
            'total_lab_results': len(lab_results),
            'total_imaging': len(imaging),
            'last_visit_date': visits[0].get('date') if visits else 'N/A'
        }
    
    def calculate_age(self, date_of_birth: str) -> int:
        """Calculate age from date of birth"""
        try:
            birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        except:
            return 0


# Global instance
patient_manager = PatientManager()