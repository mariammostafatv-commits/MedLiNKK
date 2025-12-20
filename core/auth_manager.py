"""
Authentication Manager - FINAL VERSION
Handles both doctors (user_id) and patients (national_id)
Location: core/auth_manager.py
"""

from core.database import get_db
from core.models import User, Patient
from utils.security import hash_password, verify_password
from typing import Tuple, Optional, Dict
from sqlalchemy import text


class AuthManager:
    """Manages user authentication - supports both NFC and username/password"""
    
    def __init__(self):
        self.current_user = None
    
    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """Authenticate user with username and password"""
        try:
            with get_db() as db:
                user = db.query(User).filter(User.username == username).first()
                
                if not user:
                    return False, "Invalid username or password", None
                
                if not verify_password(password, user.password_hash):
                    return False, "Invalid username or password", None
                
                # Check account status
                if hasattr(user, 'account_status'):
                    if user.account_status.value == 'inactive':
                        return False, "Account is inactive", None
                    elif user.account_status.value == 'suspended':
                        return False, "Account is suspended", None
                
                user_data = self._convert_user_to_dict(user)
                self.current_user = user_data
                
                return True, "Login successful", user_data
        
        except Exception as e:
            print(f"Login error: {e}")
            return False, f"Login error: {str(e)}", None
    
    def login_with_nfc(self, card_uid: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Authenticate user with NFC card UID
        Handles BOTH doctors (owner_id = user_id) and patients (owner_id = national_id)
        """
        try:
            with get_db() as db:
                # Query card from nfc_cards table
                result = db.execute(
                    text("""
                        SELECT card_uid, owner_id, owner_name, card_type, 
                               is_active, status
                        FROM nfc_cards 
                        WHERE card_uid = :card_uid
                    """),
                    {"card_uid": card_uid}
                ).fetchone()
                
                if not result:
                    print(f"❌ Card {card_uid} not found in database")
                    return False, "Card not recognized", None
                
                # Parse result
                db_card_uid, owner_id, owner_name, card_type, is_active, status = result
                
                print(f"✅ Card found: UID={db_card_uid}, Type={card_type}, Active={is_active}, Status={status}")
                print(f"   Owner ID: {owner_id}, Name: {owner_name}")
                
                # Check if active
                if is_active in [0, False, '0', 'false']:
                    return False, "Card is inactive", None
                
                # Check status
                if status and str(status).lower() != 'active':
                    return False, f"Card status: {status}", None
                
                # Handle based on card type
                if card_type == 'doctor':
                    # Doctor: owner_id is user_id in users table
                    user = db.query(User).filter(User.user_id == str(owner_id)).first()
                    
                    if not user:
                        return False, f"Doctor account (ID: {owner_id}) not found", None
                    
                    user_data = self._convert_user_to_dict(user)
                    
                elif card_type == 'patient':
                    # Patient: owner_id is national_id in patients table
                    patient = db.query(Patient).filter(Patient.national_id == str(owner_id)).first()
                    
                    if not patient:
                        return False, f"Patient (ID: {owner_id}) not found", None
                    
                    # Convert patient to user_data format
                    user_data = {
                        'user_id': patient.national_id,  # Use national_id as user_id
                        'username': f"patient_{patient.national_id}",
                        'full_name': patient.full_name,
                        'role': 'patient',
                        'national_id': patient.national_id,
                        'age': patient.age,
                        'gender': patient.gender.value if hasattr(patient.gender, 'value') else str(patient.gender),
                        'blood_type': patient.blood_type.value if hasattr(patient.blood_type, 'value') else str(patient.blood_type),
                        'phone': patient.phone,
                        'email': patient.email,
                        'specialization': None,
                        'license_number': None,
                        'hospital': None,
                        'department': None
                    }
                else:
                    return False, f"Unknown card type: {card_type}", None
                
                # Store current user
                self.current_user = user_data
                
                return True, f"Welcome {user_data['full_name']}", user_data
        
        except Exception as e:
            print(f"❌ NFC login error: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Card authentication failed: {str(e)}", None
    
    def _convert_user_to_dict(self, user: User) -> Dict:
        """Convert User model to dictionary"""
        return {
            'user_id': user.user_id,
            'username': user.username,
            'full_name': user.full_name,
            'role': user.role.value if hasattr(user.role, 'value') else str(user.role),
            'specialization': user.specialization if hasattr(user, 'specialization') else None,
            'license_number': user.license_number if hasattr(user, 'license_number') else None,
            'hospital': user.hospital if hasattr(user, 'hospital') else None,
            'department': user.department if hasattr(user, 'department') else None,
            'email': user.email if hasattr(user, 'email') else None,
            'phone': user.phone if hasattr(user, 'phone') else None
        }
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def get_current_user(self) -> Optional[Dict]:
        """Get currently logged in user"""
        return self.current_user
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.current_user is not None