"""
Patient Manager - Database Version
Handles patient records using database instead of JSON
Includes all medical history: surgeries, hospitalizations, vaccinations, family history, etc.
Location: core/patient_manager.py
"""
from datetime import datetime
from database.connection import get_db_context
from database.models import Patient


class PatientManager:
    """
    Manages patient records with database backend
    Compatible with existing GUI - same method signatures
    Handles complex nested medical data stored as JSON in database
    """
    
    def __init__(self):
        """Initialize patient manager"""
        pass  # No more JSON file needed!
    
    def get_all_patients(self):
        """
        Get all patients
        
        Returns:
            list: List of patient dictionaries
        """
        with get_db_context() as db:
            patients = db.query(Patient).all()
            # Convert all to dict inside session
            return [self._patient_to_dict(patient) for patient in patients]
    
    def get_patient(self, national_id):
        """
        Get patient by national ID
        
        Args:
            national_id: Egyptian national ID (14 digits)
        
        Returns:
            dict: Patient data if found, None otherwise
        """
        with get_db_context() as db:
            patient = db.query(Patient).filter_by(national_id=national_id).first()
            if patient:
                return self._patient_to_dict(patient)
        return None
    
    def search_patients(self, query):
        """
        Search patients by name or national ID
        
        Args:
            query: Search string
        
        Returns:
            list: List of matching patient dictionaries
        """
        with get_db_context() as db:
            patients = db.query(Patient).filter(
                (Patient.full_name.contains(query)) |
                (Patient.national_id.contains(query))
            ).all()
            
            # Convert all to dict inside session
            return [self._patient_to_dict(patient) for patient in patients]
    
    def add_patient(self, patient_data):
        """
        Add new patient
        
        Args:
            patient_data: Dictionary with patient information
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Parse date of birth if string
            if 'date_of_birth' in patient_data and isinstance(patient_data['date_of_birth'], str):
                from datetime import datetime
                patient_data['date_of_birth'] = datetime.strptime(
                    patient_data['date_of_birth'], "%Y-%m-%d"
                ).date()
            
            # Set timestamps
            patient_data['created_at'] = datetime.now()
            patient_data['last_updated'] = datetime.now()
            
            # Initialize empty arrays/objects if not provided
            if 'chronic_diseases' not in patient_data:
                patient_data['chronic_diseases'] = []
            if 'allergies' not in patient_data:
                patient_data['allergies'] = []
            if 'current_medications' not in patient_data:
                patient_data['current_medications'] = []
            if 'surgeries' not in patient_data:
                patient_data['surgeries'] = []
            if 'hospitalizations' not in patient_data:
                patient_data['hospitalizations'] = []
            if 'vaccinations' not in patient_data:
                patient_data['vaccinations'] = []
            if 'family_history' not in patient_data:
                patient_data['family_history'] = {}
            if 'disabilities_special_needs' not in patient_data:
                patient_data['disabilities_special_needs'] = {}
            if 'emergency_directives' not in patient_data:
                patient_data['emergency_directives'] = {}
            if 'lifestyle' not in patient_data:
                patient_data['lifestyle'] = {}
            
            with get_db_context() as db:
                # Check if patient already exists
                existing = db.query(Patient).filter_by(
                    national_id=patient_data['national_id']
                ).first()
                
                if existing:
                    return False
                
                # Create new patient
                patient = Patient(**patient_data)
                db.add(patient)
                # Auto-commits on exit
            
            return True
            
        except Exception as e:
            print(f"Error adding patient: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def update_patient(self, national_id, updates):
        """
        Update patient information
        
        Args:
            national_id: Patient's national ID
            updates: Dictionary of fields to update
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Parse date of birth if string
            if 'date_of_birth' in updates and isinstance(updates['date_of_birth'], str):
                from datetime import datetime
                updates['date_of_birth'] = datetime.strptime(
                    updates['date_of_birth'], "%Y-%m-%d"
                ).date()
            
            # Update last_updated timestamp
            updates['last_updated'] = datetime.now()
            
            with get_db_context() as db:
                patient = db.query(Patient).filter_by(national_id=national_id).first()
                if not patient:
                    return False
                
                # Update fields
                for key, value in updates.items():
                    if hasattr(patient, key):
                        setattr(patient, key, value)
                
                # Auto-commits on exit
            
            return True
            
        except Exception as e:
            print(f"Error updating patient: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def delete_patient(self, national_id):
        """
        Delete patient (with cascade to visits, lab results, imaging)
        
        Args:
            national_id: Patient's national ID
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with get_db_context() as db:
                patient = db.query(Patient).filter_by(national_id=national_id).first()
                if not patient:
                    return False
                
                db.delete(patient)
                # Auto-commits on exit
                # Related visits, lab results, imaging will be deleted due to cascade
            
            return True
            
        except Exception as e:
            print(f"Error deleting patient: {e}")
            return False
    
    # ========== SURGERIES ==========
    
    def get_surgeries(self, national_id):
        """Get patient's surgery history"""
        patient = self.get_patient(national_id)
        return patient.get('surgeries', []) if patient else []
    
    def add_surgery(self, national_id, surgery_data):
        """Add surgery to patient's history"""
        patient = self.get_patient(national_id)
        if not patient:
            return False
        
        surgeries = patient.get('surgeries', [])
        surgeries.append(surgery_data)
        
        return self.update_patient(national_id, {'surgeries': surgeries})
    
    def update_surgery(self, national_id, surgery_index, updates):
        """Update specific surgery"""
        patient = self.get_patient(national_id)
        if not patient:
            return False
        
        surgeries = patient.get('surgeries', [])
        if 0 <= surgery_index < len(surgeries):
            surgeries[surgery_index].update(updates)
            return self.update_patient(national_id, {'surgeries': surgeries})
        
        return False
    
    def delete_surgery(self, national_id, surgery_index):
        """Delete surgery from history"""
        patient = self.get_patient(national_id)
        if not patient:
            return False
        
        surgeries = patient.get('surgeries', [])
        if 0 <= surgery_index < len(surgeries):
            surgeries.pop(surgery_index)
            return self.update_patient(national_id, {'surgeries': surgeries})
        
        return False
    
    # ========== HOSPITALIZATIONS ==========
    
    def get_hospitalizations(self, national_id):
        """Get patient's hospitalization history"""
        patient = self.get_patient(national_id)
        return patient.get('hospitalizations', []) if patient else []
    
    def add_hospitalization(self, national_id, hospitalization_data):
        """Add hospitalization to patient's history"""
        patient = self.get_patient(national_id)
        if not patient:
            return False
        
        hospitalizations = patient.get('hospitalizations', [])
        hospitalizations.append(hospitalization_data)
        
        return self.update_patient(national_id, {'hospitalizations': hospitalizations})
    
    def update_hospitalization(self, national_id, hosp_index, updates):
        """Update specific hospitalization"""
        patient = self.get_patient(national_id)
        if not patient:
            return False
        
        hospitalizations = patient.get('hospitalizations', [])
        if 0 <= hosp_index < len(hospitalizations):
            hospitalizations[hosp_index].update(updates)
            return self.update_patient(national_id, {'hospitalizations': hospitalizations})
        
        return False
    
    def delete_hospitalization(self, national_id, hosp_index):
        """Delete hospitalization from history"""
        patient = self.get_patient(national_id)
        if not patient:
            return False
        
        hospitalizations = patient.get('hospitalizations', [])
        if 0 <= hosp_index < len(hospitalizations):
            hospitalizations.pop(hosp_index)
            return self.update_patient(national_id, {'hospitalizations': hospitalizations})
        
        return False
    
    # ========== VACCINATIONS ==========
    
    def get_vaccinations(self, national_id):
        """Get patient's vaccination history"""
        patient = self.get_patient(national_id)
        return patient.get('vaccinations', []) if patient else []
    
    def add_vaccination(self, national_id, vaccination_data):
        """Add vaccination to patient's history"""
        patient = self.get_patient(national_id)
        if not patient:
            return False
        
        vaccinations = patient.get('vaccinations', [])
        vaccinations.append(vaccination_data)
        
        return self.update_patient(national_id, {'vaccinations': vaccinations})
    
    def update_vaccination(self, national_id, vacc_index, updates):
        """Update specific vaccination"""
        patient = self.get_patient(national_id)
        if not patient:
            return False
        
        vaccinations = patient.get('vaccinations', [])
        if 0 <= vacc_index < len(vaccinations):
            vaccinations[vacc_index].update(updates)
            return self.update_patient(national_id, {'vaccinations': vaccinations})
        
        return False
    
    def delete_vaccination(self, national_id, vacc_index):
        """Delete vaccination from history"""
        patient = self.get_patient(national_id)
        if not patient:
            return False
        
        vaccinations = patient.get('vaccinations', [])
        if 0 <= vacc_index < len(vaccinations):
            vaccinations.pop(vacc_index)
            return self.update_patient(national_id, {'vaccinations': vaccinations})
        
        return False
    
    # ========== FAMILY HISTORY ==========
    
    def get_family_history(self, national_id):
        """Get patient's family history"""
        patient = self.get_patient(national_id)
        return patient.get('family_history', {}) if patient else {}
    
    def update_family_history(self, national_id, family_history_data):
        """Update patient's family history"""
        return self.update_patient(national_id, {'family_history': family_history_data})
    
    # ========== DISABILITIES / SPECIAL NEEDS ==========
    
    def get_disabilities(self, national_id):
        """Get patient's disabilities and special needs"""
        patient = self.get_patient(national_id)
        return patient.get('disabilities_special_needs', {}) if patient else {}
    
    def update_disabilities(self, national_id, disabilities_data):
        """Update patient's disabilities and special needs"""
        return self.update_patient(national_id, {'disabilities_special_needs': disabilities_data})
    
    # ========== EMERGENCY DIRECTIVES ==========
    
    def get_emergency_directives(self, national_id):
        """Get patient's emergency directives (DNR, organ donor, etc.)"""
        patient = self.get_patient(national_id)
        return patient.get('emergency_directives', {}) if patient else {}
    
    def update_emergency_directives(self, national_id, directives_data):
        """Update patient's emergency directives"""
        return self.update_patient(national_id, {'emergency_directives': directives_data})
    
    # ========== LIFESTYLE ==========
    
    def get_lifestyle(self, national_id):
        """Get patient's lifestyle information"""
        patient = self.get_patient(national_id)
        return patient.get('lifestyle', {}) if patient else {}
    
    def update_lifestyle(self, national_id, lifestyle_data):
        """Update patient's lifestyle information"""
        return self.update_patient(national_id, {'lifestyle': lifestyle_data})
    
    # ========== NFC CARD ==========
    
    def assign_nfc_card(self, national_id, card_uid, card_type='standard'):
        """Assign NFC card to patient"""
        updates = {
            'nfc_card_uid': card_uid,
            'nfc_card_assigned': True,
            'nfc_card_assignment_date': datetime.now().date(),
            'nfc_card_type': card_type,
            'nfc_card_status': 'active'
        }
        return self.update_patient(national_id, updates)
    
    def deactivate_nfc_card(self, national_id):
        """Deactivate patient's NFC card"""
        updates = {
            'nfc_card_status': 'deactivated'
        }
        return self.update_patient(national_id, updates)
    
    def get_patient_by_card(self, card_uid):
        """Get patient by NFC card UID"""
        with get_db_context() as db:
            patient = db.query(Patient).filter_by(
                nfc_card_uid=card_uid,
                nfc_card_assigned=True
            ).first()
            if patient:
                return self._patient_to_dict(patient)
        return None
    
    # ========== STATISTICS ==========
    
    def get_patient_count(self):
        """Get total number of patients"""
        with get_db_context() as db:
            return db.query(Patient).count()
    
    def get_patients_by_blood_type(self, blood_type):
        """Get all patients with specific blood type"""
        with get_db_context() as db:
            patients = db.query(Patient).filter_by(blood_type=blood_type).all()
            # Convert all to dict inside session
            return [self._patient_to_dict(patient) for patient in patients]
    
    def _patient_to_dict(self, patient):
        """
        Convert Patient model to dictionary for GUI compatibility
        Call this ONLY inside a database session context
        
        Args:
            patient: Patient SQLAlchemy model
        
        Returns:
            dict: Patient data as dictionary
        """
        if not patient:
            return None
        
        return {
            # Basic information
            'national_id': patient.national_id,
            'full_name': patient.full_name,
            'date_of_birth': str(patient.date_of_birth) if patient.date_of_birth else None,
            'age': patient.age,
            'gender': patient.gender,
            'blood_type': patient.blood_type,
            
            # Contact information
            'phone': patient.phone,
            'email': patient.email,
            'address': patient.address,
            
            # Emergency contact
            'emergency_contact': patient.emergency_contact or {},
            
            # Medical information (JSON arrays/objects)
            'chronic_diseases': patient.chronic_diseases or [],
            'allergies': patient.allergies or [],
            'current_medications': patient.current_medications or [],
            
            # Insurance
            'insurance': patient.insurance or {},
            
            # External links
            'external_links': patient.external_links or {},
            
            # Complex medical records (JSON)
            'surgeries': patient.surgeries or [],
            'hospitalizations': patient.hospitalizations or [],
            'vaccinations': patient.vaccinations or [],
            'family_history': patient.family_history or {},
            'disabilities_special_needs': patient.disabilities_special_needs or {},
            'emergency_directives': patient.emergency_directives or {},
            'lifestyle': patient.lifestyle or {},
            
            # NFC card information
            'nfc_card_uid': patient.nfc_card_uid,
            'nfc_card_assigned': patient.nfc_card_assigned,
            'nfc_card_assignment_date': str(patient.nfc_card_assignment_date) if patient.nfc_card_assignment_date else None,
            'nfc_card_type': patient.nfc_card_type,
            'nfc_card_status': patient.nfc_card_status,
            'nfc_card_last_scan': str(patient.nfc_card_last_scan) if patient.nfc_card_last_scan else None,
            'nfc_scan_count': patient.nfc_scan_count,
            
            # Timestamps
            'created_at': str(patient.created_at) if patient.created_at else None,
            'last_updated': str(patient.last_updated) if patient.last_updated else None
        }


# Singleton instance
_patient_manager = None

def get_patient_manager():
    """Get singleton instance of PatientManager"""
    global _patient_manager
    if _patient_manager is None:
        _patient_manager = PatientManager()
    return _patient_manager