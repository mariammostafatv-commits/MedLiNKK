"""
Card Manager - NFC Card Management
MySQL Version - Compatible with existing GUI
"""

from datetime import datetime, date
from core.database import get_db
from database.models import NFCCard, Patient, Doctor, User

class CardManager:
    """Manage NFC cards for patients and doctors"""
    
    def __init__(self):
        pass
    
    def register_card(self, card_uid, card_type, linked_to, name, **kwargs):
        """
        Register new NFC card
        
        Args:
            card_uid: Card UID from scanner
            card_type: 'doctor' or 'patient'
            linked_to: user_id or national_id
            name: Full name
        """
        with get_db() as db:
            # Check if card already exists
            existing = db.query(NFCCard).filter(NFCCard.card_uid == card_uid).first()
            if existing:
                return {'success': False, 'message': 'Card already registered'}
            
            card = NFCCard(
                card_uid=card_uid,
                card_type=card_type,
                linked_to=linked_to,
                name=name,
                is_active=True,
                assigned_date=date.today(),
                **kwargs
            )
            db.add(card)
            db.commit()
            db.refresh(card)
            
            return {'success': True, 'card': card, 'message': 'Card registered successfully'}
    
    def get_card(self, card_uid):
        """Get card by UID"""
        with get_db() as db:
            return db.query(NFCCard).filter(NFCCard.card_uid == card_uid).first()
    
    def get_card_by_user(self, linked_to):
        """Get card by linked user/patient"""
        with get_db() as db:
            return db.query(NFCCard).filter(
                NFCCard.linked_to == linked_to,
                NFCCard.is_active == True
            ).first()
    
    def authenticate_card(self, card_uid):
        """
        Authenticate user by NFC card
        Returns: dict with success, card_type, user_info
        """
        with get_db() as db:
            card = db.query(NFCCard).filter(
                NFCCard.card_uid == card_uid,
                NFCCard.is_active == True
            ).first()
            
            if not card:
                return {'success': False, 'message': 'Card not found or inactive'}
            
            # Update scan info
            card.last_scan = datetime.now()
            card.scan_count += 1
            db.commit()
            
            # Get user info based on card type
            if card.card_type == 'doctor':
                user = db.query(User).filter(User.user_id == card.linked_to).first()
                if user:
                    return {
                        'success': True,
                        'card_type': 'doctor',
                        'user_id': user.user_id,
                        'username': user.username,
                        'full_name': user.full_name,
                        'role': user.role
                    }
            
            elif card.card_type == 'patient':
                patient = db.query(Patient).filter(
                    Patient.national_id == card.linked_to
                ).first()
                if patient:
                    return {
                        'success': True,
                        'card_type': 'patient',
                        'national_id': patient.national_id,
                        'full_name': patient.full_name,
                        'blood_type': patient.blood_type,
                        'age': patient.age
                    }
            
            return {'success': False, 'message': 'User not found'}
    
    def update_card(self, card_uid, update_data):
        """Update card information"""
        with get_db() as db:
            card = db.query(NFCCard).filter(NFCCard.card_uid == card_uid).first()
            
            if card:
                for key, value in update_data.items():
                    if hasattr(card, key):
                        setattr(card, key, value)
                
                db.commit()
                return {'success': True, 'message': 'Card updated'}
            
            return {'success': False, 'message': 'Card not found'}
    
    def deactivate_card(self, card_uid):
        """Deactivate card (lost/stolen)"""
        with get_db() as db:
            card = db.query(NFCCard).filter(NFCCard.card_uid == card_uid).first()
            
            if card:
                card.is_active = False
                db.commit()
                return {'success': True, 'message': 'Card deactivated'}
            
            return {'success': False, 'message': 'Card not found'}
    
    def activate_card(self, card_uid):
        """Reactivate card"""
        with get_db() as db:
            card = db.query(NFCCard).filter(NFCCard.card_uid == card_uid).first()
            
            if card:
                card.is_active = True
                db.commit()
                return {'success': True, 'message': 'Card activated'}
            
            return {'success': False, 'message': 'Card not found'}
    
    def get_all_cards(self, card_type=None, active_only=True):
        """Get all cards, optionally filtered"""
        with get_db() as db:
            query = db.query(NFCCard)
            
            if card_type:
                query = query.filter(NFCCard.card_type == card_type)
            
            if active_only:
                query = query.filter(NFCCard.is_active == True)
            
            return query.order_by(NFCCard.name).all()
    
    def get_card_stats(self, card_uid):
        """Get card usage statistics"""
        with get_db() as db:
            card = db.query(NFCCard).filter(NFCCard.card_uid == card_uid).first()
            
            if card:
                return {
                    'card_uid': card.card_uid,
                    'name': card.name,
                    'card_type': card.card_type,
                    'is_active': card.is_active,
                    'assigned_date': card.assigned_date,
                    'last_scan': card.last_scan,
                    'scan_count': card.scan_count
                }
            
            return None
    
    def search_cards(self, search_term):
        """Search cards by name or UID"""
        with get_db() as db:
            search = f"%{search_term}%"
            return db.query(NFCCard).filter(
                (NFCCard.name.like(search)) |
                (NFCCard.card_uid.like(search))
            ).all()
    
    def link_card_to_patient(self, card_uid, national_id):
        """Link existing card to patient"""
        with get_db() as db:
            # Get patient
            patient = db.query(Patient).filter(
                Patient.national_id == national_id
            ).first()
            
            if not patient:
                return {'success': False, 'message': 'Patient not found'}
            
            # Get card
            card = db.query(NFCCard).filter(NFCCard.card_uid == card_uid).first()
            
            if not card:
                return {'success': False, 'message': 'Card not found'}
            
            # Link card
            card.linked_to = national_id
            card.name = patient.full_name
            card.card_type = 'patient'
            card.is_active = True
            
            # Update patient
            patient.nfc_card_uid = card_uid
            patient.nfc_card_assigned = True
            patient.nfc_card_assignment_date = date.today()
            patient.nfc_card_type = 'NFC Card'
            patient.nfc_card_status = 'active'
            
            db.commit()
            
            return {'success': True, 'message': 'Card linked to patient'}
    
    def unlink_card(self, card_uid):
        """Unlink card from user"""
        with get_db() as db:
            card = db.query(NFCCard).filter(NFCCard.card_uid == card_uid).first()
            
            if card:
                # If patient card, update patient record
                if card.card_type == 'patient':
                    patient = db.query(Patient).filter(
                        Patient.national_id == card.linked_to
                    ).first()
                    if patient:
                        patient.nfc_card_uid = None
                        patient.nfc_card_assigned = False
                        patient.nfc_card_status = 'inactive'
                
                # Delete card
                db.delete(card)
                db.commit()
                
                return {'success': True, 'message': 'Card unlinked'}
            
            return {'success': False, 'message': 'Card not found'}

# Global instance
card_manager = CardManager()