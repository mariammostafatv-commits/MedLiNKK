"""
ROBUST Card Manager - Works with ANY Patient Model Version
Handles both old models (without Phase 8-11 fields) and new models
Location: core/card_manager.py (REPLACE YOUR FILE)
"""

from core.database import get_db
from core.models import DoctorCard, PatientCard, User, Patient
from datetime import datetime


def safe_get_attr(obj, attr_name, default=None):
    """
    Safely get attribute from object with fallback
    Handles missing Phase 8-11 attributes gracefully
    """
    try:
        value = getattr(obj, attr_name, default)
        
        # Handle enums
        if hasattr(value, 'value'):
            return value.value
        
        return value if value is not None else default
    except:
        return default


class CardManager:
    """Manage NFC card operations - ROBUST version"""

    def __init__(self):
        """Initialize card manager"""
        pass

    def get_card(self, card_uid: str):
        """
        Get card information by UID (works for both doctor and patient cards)
        
        Args:
            card_uid: NFC card UID
            
        Returns:
            dict: Card information or None
        """
        db = get_db()
        try:
            # Try doctor card first
            dc = db.query(DoctorCard).filter(
                DoctorCard.card_uid == card_uid,
                DoctorCard.is_active == True
            ).first()

            if dc:
                # Update last used
                dc.last_used = datetime.now()
                db.commit()

                return {
                    "card_type": "doctor",
                    "card_uid": dc.card_uid,
                    "full_name": dc.full_name,
                    "username": dc.username,
                    "user_id": dc.user_id,
                    "user": {
                        "user_id": dc.user.user_id,
                        "username": dc.user.username,
                        "full_name": dc.user.full_name,
                        "role": safe_get_attr(dc.user, 'role', 'doctor'),
                        "specialization": safe_get_attr(dc.user, 'specialization'),
                        "hospital": safe_get_attr(dc.user, 'hospital')
                    } if dc.user else None
                }

            # Try patient card
            pc = db.query(PatientCard).filter(
                PatientCard.card_uid == card_uid,
                PatientCard.is_active == True
            ).first()

            if pc:
                # Update last used
                pc.last_used = datetime.now()
                db.commit()

                return {
                    "card_type": "patient",
                    "card_uid": pc.card_uid,
                    "full_name": pc.full_name,
                    "national_id": pc.patient_national_id,  # ✅ Correct attribute
                    "patient": {
                        "national_id": pc.patient.national_id,
                        "full_name": pc.patient.full_name,
                        "age": safe_get_attr(pc.patient, 'age', 0),
                        "gender": safe_get_attr(pc.patient, 'gender', 'Unknown'),
                        "blood_type": safe_get_attr(pc.patient, 'blood_type', 'Unknown'),
                    } if pc.patient else None
                }

            return None
        finally:
            db.close()

    def get_patient_by_card(self, card_uid: str):
        """
        Get patient data by card UID - Returns complete patient dict
        ROBUST: Handles missing Phase 8-11 attributes gracefully
        
        Args:
            card_uid: NFC card UID
            
        Returns:
            dict: Complete patient data or None
        """
        db = get_db()
        try:
            # Find patient card
            patient_card = db.query(PatientCard).filter_by(
                card_uid=card_uid,
                is_active=True
            ).first()

            if not patient_card:
                return None

            # ✅ FIXED: Use correct attribute name
            patient = db.query(Patient).filter_by(
                national_id=patient_card.patient_national_id
            ).first()

            if not patient:
                return None

            # Convert to complete dict while in session
            # ✅ ROBUST: Uses safe_get_attr for ALL attributes
            patient_dict = {
                'id': safe_get_attr(patient, 'id'),
                'national_id': safe_get_attr(patient, 'national_id', ''),
                'full_name': safe_get_attr(patient, 'full_name', 'Unknown'),
                'date_of_birth': safe_get_attr(patient, 'date_of_birth'),
                'age': safe_get_attr(patient, 'age', 0),
                'gender': safe_get_attr(patient, 'gender', 'Unknown'),
                'blood_type': safe_get_attr(patient, 'blood_type', 'Unknown'),
                'phone': safe_get_attr(patient, 'phone', ''),
                'email': safe_get_attr(patient, 'email', ''),
                'address': safe_get_attr(patient, 'address', ''),
                'city': safe_get_attr(patient, 'city', ''),
                'governorate': safe_get_attr(patient, 'governorate', ''),
            }

            # JSON fields - safe access
            patient_dict['emergency_contact'] = safe_get_attr(patient, 'emergency_contact', {}) or {}
            patient_dict['allergies'] = safe_get_attr(patient, 'allergies', []) or []
            patient_dict['chronic_diseases'] = safe_get_attr(patient, 'chronic_diseases', []) or []
            
            # Phase 8-11 fields - may not exist in older schemas
            patient_dict['family_history'] = safe_get_attr(patient, 'family_history', {}) or {}
            patient_dict['disabilities_special_needs'] = safe_get_attr(patient, 'disabilities_special_needs', {}) or {}
            patient_dict['emergency_directives'] = safe_get_attr(patient, 'emergency_directives', {}) or {}
            patient_dict['lifestyle'] = safe_get_attr(patient, 'lifestyle', {}) or {}
            patient_dict['insurance'] = safe_get_attr(patient, 'insurance', {}) or {}
            patient_dict['external_links'] = safe_get_attr(patient, 'external_links', {}) or {}

            # Relationships - convert to lists (safely)
            try:
                if hasattr(patient, 'current_medications'):
                    patient_dict['current_medications'] = [
                        {
                            'name': safe_get_attr(m, 'medication_name', 'Unknown'),
                            'dosage': safe_get_attr(m, 'dosage', ''),
                            'frequency': safe_get_attr(m, 'frequency', ''),
                            'started_date': str(m.started_date) if hasattr(m, 'started_date') and m.started_date else None
                        }
                        for m in patient.current_medications 
                        if safe_get_attr(m, 'is_active', True)
                    ]
                else:
                    patient_dict['current_medications'] = []
            except:
                patient_dict['current_medications'] = []

            try:
                if hasattr(patient, 'surgeries'):
                    patient_dict['surgeries'] = [
                        {
                            'surgery_id': safe_get_attr(s, 'surgery_id'),
                            'procedure': safe_get_attr(s, 'procedure_name', 'Unknown'),
                            'date': str(s.surgery_date) if hasattr(s, 'surgery_date') and s.surgery_date else None,
                            'hospital': safe_get_attr(s, 'hospital', ''),
                            'surgeon': safe_get_attr(s, 'surgeon_name', ''),
                            'complications': safe_get_attr(s, 'complications', ''),
                            'notes': safe_get_attr(s, 'recovery_notes', '')
                        }
                        for s in patient.surgeries
                    ]
                else:
                    patient_dict['surgeries'] = []
            except:
                patient_dict['surgeries'] = []

            try:
                if hasattr(patient, 'hospitalizations'):
                    patient_dict['hospitalizations'] = [
                        {
                            'hospitalization_id': safe_get_attr(h, 'hospitalization_id'),
                            'admission_date': str(h.admission_date) if hasattr(h, 'admission_date') and h.admission_date else None,
                            'discharge_date': str(h.discharge_date) if hasattr(h, 'discharge_date') and h.discharge_date else None,
                            'reason': safe_get_attr(h, 'admission_reason', ''),
                            'hospital': safe_get_attr(h, 'hospital', ''),
                            'diagnosis': safe_get_attr(h, 'diagnosis', ''),
                            'outcome': safe_get_attr(h, 'discharge_notes', '')
                        }
                        for h in patient.hospitalizations
                    ]
                else:
                    patient_dict['hospitalizations'] = []
            except:
                patient_dict['hospitalizations'] = []

            try:
                if hasattr(patient, 'vaccinations'):
                    patient_dict['vaccinations'] = [
                        {
                            'vaccine_name': safe_get_attr(v, 'vaccine_name', 'Unknown'),
                            'date_administered': str(v.date_administered) if hasattr(v, 'date_administered') and v.date_administered else None,
                            'dose_number': safe_get_attr(v, 'dose_number'),
                            'batch_number': safe_get_attr(v, 'batch_number', ''),
                            'next_dose_due': str(v.next_dose_due) if hasattr(v, 'next_dose_due') and v.next_dose_due else None
                        }
                        for v in patient.vaccinations
                    ]
                else:
                    patient_dict['vaccinations'] = []
            except:
                patient_dict['vaccinations'] = []

            # NFC info - safe access
            patient_dict['nfc_card_uid'] = safe_get_attr(patient, 'nfc_card_uid')
            patient_dict['nfc_card_assigned'] = safe_get_attr(patient, 'nfc_card_assigned', False)
            patient_dict['nfc_card_status'] = safe_get_attr(patient, 'nfc_card_status')

            # Timestamps - safe access
            patient_dict['created_at'] = safe_get_attr(patient, 'created_at')
            patient_dict['last_updated'] = safe_get_attr(patient, 'last_updated')

            return patient_dict

        except Exception as e:
            print(f"Error in get_patient_by_card: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            db.close()

    def get_doctor_by_card(self, card_uid: str):
        """
        Get doctor user data by card UID
        
        Args:
            card_uid: NFC card UID
            
        Returns:
            dict: Doctor user data or None
        """
        db = get_db()
        try:
            doctor_card = db.query(DoctorCard).filter_by(
                card_uid=card_uid,
                is_active=True
            ).first()

            if doctor_card:
                user = db.query(User).filter_by(
                    user_id=doctor_card.user_id).first()
                if user:
                    return {
                        'user_id': safe_get_attr(user, 'user_id'),
                        'username': safe_get_attr(user, 'username', ''),
                        'full_name': safe_get_attr(user, 'full_name', 'Unknown'),
                        'role': safe_get_attr(user, 'role', 'doctor'),
                        'national_id': safe_get_attr(user, 'national_id', ''),
                        'specialization': safe_get_attr(user, 'specialization'),
                        'hospital': safe_get_attr(user, 'hospital'),
                        'license_number': safe_get_attr(user, 'license_number'),
                        'email': safe_get_attr(user, 'email', ''),
                        'phone': safe_get_attr(user, 'phone', '')
                    }
            return None
        finally:
            db.close()

    def authenticate_card(self, card_uid: str):
        """
        Authenticate a card and return user/patient information
        
        Args:
            card_uid: NFC card UID
            
        Returns:
            tuple: (success: bool, data: dict, message: str)
        """
        card_info = self.get_card(card_uid)

        if not card_info:
            return False, None, "Card not found or inactive"

        if card_info['card_type'] == 'doctor':
            return True, card_info, f"Welcome, Dr. {card_info['full_name']}"
        else:
            return True, card_info, f"Welcome, {card_info['full_name']}"

    def is_doctor_card(self, card_uid: str):
        """Check if card is a doctor card"""
        db = get_db()
        try:
            card = db.query(DoctorCard).filter_by(
                card_uid=card_uid,
                is_active=True
            ).first()
            return card is not None
        finally:
            db.close()

    def is_patient_card(self, card_uid: str):
        """Check if card is a patient card"""
        db = get_db()
        try:
            card = db.query(PatientCard).filter_by(
                card_uid=card_uid,
                is_active=True
            ).first()
            return card is not None
        finally:
            db.close()


# Global instance
card_manager = CardManager()