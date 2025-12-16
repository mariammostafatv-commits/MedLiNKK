"""
NFC Card Manager - Database Version
Handles NFC card management using database instead of JSON
Location: core/card_manager.py
"""
from datetime import datetime
from database.connection import get_db_context
from database.models import NFCCard, User, Patient


class CardManager:
    """
    Manages NFC card records with database backend
    Compatible with existing GUI - same method signatures
    """
    
    def __init__(self):
        """Initialize card manager"""
        pass
    
    def get_all_cards(self):
        """
        Get all NFC cards
        
        Returns:
            dict: Dictionary with 'doctor_cards' and 'patient_cards'
        """
        with get_db_context() as db:
            all_cards = db.query(NFCCard).all()
            
            doctor_cards = {}
            patient_cards = {}
            
            for card in all_cards:
                card_dict = self._card_to_dict(card)
                if card.card_type == 'doctor':
                    doctor_cards[card.card_uid] = card_dict
                else:
                    patient_cards[card.card_uid] = card_dict
            
            return {
                'doctor_cards': doctor_cards,
                'patient_cards': patient_cards
            }
    
    def get_card(self, card_uid):
        """
        Get card by UID
        
        Args:
            card_uid: Card UID
        
        Returns:
            dict: Card data if found, None otherwise
        """
        with get_db_context() as db:
            card = db.query(NFCCard).filter_by(card_uid=card_uid).first()
            if card:
                return self._card_to_dict(card)
        return None
    
    def register_doctor_card(self, card_uid, username):
        """
        Register NFC card for doctor
        
        Args:
            card_uid: Card UID
            username: Doctor's username
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with get_db_context() as db:
                # Check if card already exists
                existing = db.query(NFCCard).filter_by(card_uid=card_uid).first()
                if existing:
                    print(f"Card {card_uid} already registered")
                    return False
                
                # Verify doctor exists
                doctor = db.query(User).filter_by(username=username, role='doctor').first()
                if not doctor:
                    print(f"Doctor {username} not found")
                    return False
                
                # Create new card
                card = NFCCard(
                    card_uid=card_uid,
                    card_type='doctor',
                    username=username,
                    national_id=None,
                    holder_name=doctor.full_name,
                    status='active',
                    created_at=datetime.now(),
                    last_used=None
                )
                
                db.add(card)
                # Auto-commits on exit
            
            return True
            
        except Exception as e:
            print(f"Error registering doctor card: {e}")
            return False
    
    def register_patient_card(self, card_uid, national_id):
        """
        Register NFC card for patient
        
        Args:
            card_uid: Card UID
            national_id: Patient's national ID
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with get_db_context() as db:
                # Check if card already exists
                existing = db.query(NFCCard).filter_by(card_uid=card_uid).first()
                if existing:
                    print(f"Card {card_uid} already registered")
                    return False
                
                # Verify patient exists
                patient = db.query(Patient).filter_by(national_id=national_id).first()
                if not patient:
                    print(f"Patient {national_id} not found")
                    return False
                
                # Create new card
                card = NFCCard(
                    card_uid=card_uid,
                    card_type='patient',
                    username=None,
                    national_id=national_id,
                    holder_name=patient.full_name,
                    status='active',
                    created_at=datetime.now(),
                    last_used=None
                )
                
                db.add(card)
                
                # Also update patient record with NFC card info
                patient.nfc_card_uid = card_uid
                patient.nfc_card_assigned = True
                patient.nfc_card_assignment_date = datetime.now().date()
                patient.nfc_card_status = 'active'
                
                # Auto-commits on exit
            
            return True
            
        except Exception as e:
            print(f"Error registering patient card: {e}")
            return False
    
    def authenticate_doctor(self, card_uid):
        """
        Authenticate doctor by NFC card
        
        Args:
            card_uid: Card UID
        
        Returns:
            dict: Doctor user data if successful, None otherwise
        """
        with get_db_context() as db:
            # Get card
            card = db.query(NFCCard).filter_by(
                card_uid=card_uid,
                card_type='doctor',
                status='active'
            ).first()
            
            if not card:
                return None
            
            # Get doctor user
            doctor = db.query(User).filter_by(username=card.username).first()
            if not doctor:
                return None
            
            # Update last used
            card.last_used = datetime.now()
            
            # Update doctor's last login
            doctor.last_login = datetime.now()
            
            # Convert doctor to dict INSIDE session
            doctor_dict = {
                'user_id': doctor.user_id,
                'username': doctor.username,
                'role': doctor.role,
                'full_name': doctor.full_name,
                'email': doctor.email,
                'phone': doctor.phone,
                'specialization': doctor.specialization,
                'hospital': doctor.hospital,
                'license_number': doctor.license_number
            }
            
            # Auto-commits on exit
        
        # Return the dictionary (after session closes)
        return doctor_dict
    
    def get_patient_by_card(self, card_uid):
        """
        Get patient by NFC card
        
        Args:
            card_uid: Card UID
        
        Returns:
            dict: Patient data if successful, None otherwise
        """
        with get_db_context() as db:
            # Get card
            card = db.query(NFCCard).filter_by(
                card_uid=card_uid,
                card_type='patient',
                status='active'
            ).first()
            
            if not card:
                return None
            
            # Get patient
            patient = db.query(Patient).filter_by(national_id=card.national_id).first()
            if not patient:
                return None
            
            # Update last used
            card.last_used = datetime.now()
            
            # Update patient's NFC scan info
            patient.nfc_card_last_scan = datetime.now()
            patient.nfc_scan_count = (patient.nfc_scan_count or 0) + 1
            
            # Convert to dict INSIDE session context before it closes!
            patient_dict = {
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
            
            # Auto-commits on exit
        
        # Return the dictionary (after session closes)
        return patient_dict
    
    def deactivate_card(self, card_uid):
        """
        Deactivate card (lost/stolen)
        
        Args:
            card_uid: Card UID
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with get_db_context() as db:
                card = db.query(NFCCard).filter_by(card_uid=card_uid).first()
                if not card:
                    return False
                
                card.status = 'deactivated'
                
                # If patient card, also update patient record
                if card.card_type == 'patient' and card.national_id:
                    patient = db.query(Patient).filter_by(national_id=card.national_id).first()
                    if patient:
                        patient.nfc_card_status = 'deactivated'
                
                # Auto-commits on exit
            
            return True
            
        except Exception as e:
            print(f"Error deactivating card: {e}")
            return False
    
    def reactivate_card(self, card_uid):
        """
        Reactivate card
        
        Args:
            card_uid: Card UID
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with get_db_context() as db:
                card = db.query(NFCCard).filter_by(card_uid=card_uid).first()
                if not card:
                    return False
                
                card.status = 'active'
                
                # If patient card, also update patient record
                if card.card_type == 'patient' and card.national_id:
                    patient = db.query(Patient).filter_by(national_id=card.national_id).first()
                    if patient:
                        patient.nfc_card_status = 'active'
                
                # Auto-commits on exit
            
            return True
            
        except Exception as e:
            print(f"Error reactivating card: {e}")
            return False
    
    def delete_card(self, card_uid):
        """
        Delete card registration
        
        Args:
            card_uid: Card UID
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with get_db_context() as db:
                card = db.query(NFCCard).filter_by(card_uid=card_uid).first()
                if not card:
                    return False
                
                # If patient card, also update patient record
                if card.card_type == 'patient' and card.national_id:
                    patient = db.query(Patient).filter_by(national_id=card.national_id).first()
                    if patient:
                        patient.nfc_card_uid = None
                        patient.nfc_card_assigned = False
                        patient.nfc_card_status = None
                
                db.delete(card)
                # Auto-commits on exit
            
            return True
            
        except Exception as e:
            print(f"Error deleting card: {e}")
            return False
    
    def get_card_count(self):
        """Get total number of registered cards"""
        with get_db_context() as db:
            return db.query(NFCCard).count()
    
    def get_active_cards_count(self):
        """Get number of active cards"""
        with get_db_context() as db:
            return db.query(NFCCard).filter_by(status='active').count()
    
    def _card_to_dict(self, card):
        """
        Convert NFCCard model to dictionary for GUI compatibility
        Call this ONLY inside a database session context
        
        Args:
            card: NFCCard SQLAlchemy model
        
        Returns:
            dict: Card data as dictionary
        """
        if not card:
            return None
        
        return {
            'card_uid': card.card_uid,
            'card_type': card.card_type,
            'username': card.username,
            'national_id': card.national_id,
            'holder_name': card.holder_name,
            'name': card.holder_name,  # Alias for compatibility
            'status': card.status,
            'created_at': str(card.created_at) if card.created_at else None,
            'last_used': str(card.last_used) if card.last_used else None
        }


# Singleton instance
_card_manager = None

def get_card_manager():
    """Get singleton instance of CardManager"""
    global _card_manager
    if _card_manager is None:
        _card_manager = CardManager()
    return _card_manager