"""
    Authentication Manager - FIXED with CORRECT column names
    Uses actual database structure: username (not user_id)
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
                
                if not hash_password(user.password_hash, password):
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
        """Authenticate user with NFC card UID - FIXED with correct column names"""
        try:
            with get_db() as db:
                # Use actual column names from screenshot: username (not user_id)
                result = db.execute(
                    text("""
                        SELECT card_uid, username, full_name, card_type, 
                               specialization, is_active, status
                        FROM nfc_cards 
                        WHERE card_uid = :card_uid
                    """),
                    {"card_uid": card_uid}
                ).fetchone()
                
                if not result:
                    print(f"❌ Card {card_uid} not found in database")
                    return False, "Card not recognized", None
                
                # Parse result (CORRECT column order)
                db_card_uid, username, full_name, card_type, specialization, is_active, status = result
                
                print(f"✅ Card found: UID={db_card_uid}, Type={card_type}, Active={is_active}, Status={status}")
                print(f"   Username: {username}, Name: {full_name}")
                
                # Check if active (handle integer 0/1 or boolean)
                if is_active in [0, False, '0', 'false']:
                    return False, "Card is inactive", None
                
                # Check status
                if status and str(status).lower() != 'active':
                    return False, f"Card status: {status}", None
                
                # Get user by username (from nfc_cards table)
                user = db.query(User).filter(User.username == username).first()
                
                if not user:
                    return False, f"User account '{username}' not found", None
                
                # Convert to dict
                user_data = self._convert_user_to_dict(user)
                
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