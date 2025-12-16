"""
NFC Card Manager for MedLink
Handles NFC card authentication and operations
"""

from core.database import get_db
from database.models import DoctorCard, PatientCard, User, Patient
from datetime import datetime


class CardManager:
    """Manage NFC card operations"""
    
    def __init__(self):
        """Initialize card manager"""
        self.db = None
    
    def get_card(self, card_uid):
        """
        Get card information by UID (works for both doctor and patient cards)
        
        Args:
            card_uid (str): NFC card UID
            
        Returns:
            dict: Card information with user/patient data or None
        """
        db = get_db()
        try:
            # Try to find doctor card first
            doctor_card = db.query(DoctorCard).filter_by(
                card_uid=card_uid,
                is_active=True
            ).first()
            
            if doctor_card:
                # Get associated user
                user = db.query(User).filter_by(user_id=doctor_card.user_id).first()
                
                # Update last used
                doctor_card.last_used = datetime.now()
                db.commit()
                
                return {
                    'card_type': 'doctor',
                    'card_uid': doctor_card.card_uid,
                    'user_id': doctor_card.user_id,
                    'username': doctor_card.username,
                    'full_name': doctor_card.full_name,
                    'user': user,  # Full user object
                    'card': doctor_card  # Card object
                }
            
            # Try to find patient card
            patient_card = db.query(PatientCard).filter_by(
                card_uid=card_uid,
                is_active=True
            ).first()
            
            if patient_card:
                # Get associated patient
                patient = db.query(Patient).filter_by(
                    national_id=patient_card.national_id
                ).first()
                
                # Update last used
                patient_card.last_used = datetime.now()
                db.commit()
                
                return {
                    'card_type': 'patient',
                    'card_uid': patient_card.card_uid,
                    'national_id': patient_card.national_id,
                    'full_name': patient_card.full_name,
                    'patient': patient,  # Full patient object
                    'card': patient_card  # Card object
                }
            
            # Card not found
            return None
            
        finally:
            db.close()
    
    def authenticate_card(self, card_uid):
        """
        Authenticate a card and return user/patient information
        
        Args:
            card_uid (str): NFC card UID
            
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
    
    def is_doctor_card(self, card_uid):
        """Check if card is a doctor card"""
        db = get_db()
        try:
            card = db.query(DoctorCard).filter_by(card_uid=card_uid).first()
            return card is not None
        finally:
            db.close()
    
    def is_patient_card(self, card_uid):
        """Check if card is a patient card"""
        db = get_db()
        try:
            card = db.query(PatientCard).filter_by(card_uid=card_uid).first()
            return card is not None
        finally:
            db.close()
    
    def get_doctor_by_card(self, card_uid):
        """
        Get doctor (User) by card UID
        
        Args:
            card_uid (str): NFC card UID
            
        Returns:
            User: Doctor user object or None
        """
        db = get_db()
        try:
            doctor_card = db.query(DoctorCard).filter_by(
                card_uid=card_uid,
                is_active=True
            ).first()
            
            if doctor_card:
                user = db.query(User).filter_by(user_id=doctor_card.user_id).first()
                return user
            return None
        finally:
            db.close()
    
    def get_patient_by_card(self, card_uid):
        """
        Get patient by card UID
        
        Args:
            card_uid (str): NFC card UID
            
        Returns:
            Patient: Patient object or None
        """
        db = get_db()
        try:
            patient_card = db.query(PatientCard).filter_by(
                card_uid=card_uid,
                is_active=True
            ).first()
            
            if patient_card:
                patient = db.query(Patient).filter_by(
                    national_id=patient_card.national_id
                ).first()
                return patient
            return None
        finally:
            db.close()
    
    def get_card_info(self, card_uid):
        """
        Get detailed card information (alias for get_card)
        
        Args:
            card_uid (str): NFC card UID
            
        Returns:
            dict: Card information or None
        """
        return self.get_card(card_uid)
    
    def register_doctor_card(self, card_uid, user_id, username, full_name):
        """
        Register a new doctor card
        
        Args:
            card_uid (str): NFC card UID
            user_id (str): Doctor user ID
            username (str): Doctor username
            full_name (str): Doctor full name
            
        Returns:
            bool: Success status
        """
        db = get_db()
        try:
            # Check if card already exists
            existing = db.query(DoctorCard).filter_by(card_uid=card_uid).first()
            if existing:
                return False, "Card already registered"
            
            # Create new doctor card
            card = DoctorCard(
                card_uid=card_uid,
                user_id=user_id,
                username=username,
                full_name=full_name,
                is_active=True
            )
            db.add(card)
            db.commit()
            
            return True, "Doctor card registered successfully"
        except Exception as e:
            db.rollback()
            return False, f"Error: {str(e)}"
        finally:
            db.close()
    
    def register_patient_card(self, card_uid, national_id, full_name):
        """
        Register a new patient card
        
        Args:
            card_uid (str): NFC card UID
            national_id (str): Patient national ID
            full_name (str): Patient full name
            
        Returns:
            tuple: (success: bool, message: str)
        """
        db = get_db()
        try:
            # Check if card already exists
            existing = db.query(PatientCard).filter_by(card_uid=card_uid).first()
            if existing:
                return False, "Card already registered"
            
            # Create new patient card
            card = PatientCard(
                card_uid=card_uid,
                national_id=national_id,
                full_name=full_name,
                is_active=True
            )
            db.add(card)
            db.commit()
            
            return True, "Patient card registered successfully"
        except Exception as e:
            db.rollback()
            return False, f"Error: {str(e)}"
        finally:
            db.close()
    
    def deactivate_card(self, card_uid):
        """
        Deactivate a card (mark as inactive)
        
        Args:
            card_uid (str): NFC card UID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        db = get_db()
        try:
            # Try doctor card
            doctor_card = db.query(DoctorCard).filter_by(card_uid=card_uid).first()
            if doctor_card:
                doctor_card.is_active = False
                db.commit()
                return True, "Doctor card deactivated"
            
            # Try patient card
            patient_card = db.query(PatientCard).filter_by(card_uid=card_uid).first()
            if patient_card:
                patient_card.is_active = False
                db.commit()
                return True, "Patient card deactivated"
            
            return False, "Card not found"
        except Exception as e:
            db.rollback()
            return False, f"Error: {str(e)}"
        finally:
            db.close()
    
    def activate_card(self, card_uid):
        """
        Activate a card
        
        Args:
            card_uid (str): NFC card UID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        db = get_db()
        try:
            # Try doctor card
            doctor_card = db.query(DoctorCard).filter_by(card_uid=card_uid).first()
            if doctor_card:
                doctor_card.is_active = True
                db.commit()
                return True, "Doctor card activated"
            
            # Try patient card
            patient_card = db.query(PatientCard).filter_by(card_uid=card_uid).first()
            if patient_card:
                patient_card.is_active = True
                db.commit()
                return True, "Patient card activated"
            
            return False, "Card not found"
        except Exception as e:
            db.rollback()
            return False, f"Error: {str(e)}"
        finally:
            db.close()


# Create a global instance for easy access
card_manager = CardManager()