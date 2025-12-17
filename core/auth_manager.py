"""
Authentication Manager - FIXED FOR DATABASE
Handles user authentication with correct password verification

Location: core/auth_manager.py
"""

from core.database import get_db
from core.models import User, Doctor
from utils.security import verify_password
from datetime import datetime


class AuthManager:
    """Manage user authentication"""
    
    def __init__(self):
        pass
    
    def authenticate(self, username: str, password: str) -> dict:
        """
        Authenticate user with username and password
        
        Args:
            username: User's username
            password: Plain text password
            
        Returns:
            dict with 'success', 'user', and 'message' keys
        """
        try:
            with get_db() as db:
                # Step 1: Find user by username ONLY
                user = db.query(User).filter(
                    User.username == username
                ).first()
                
                # Step 2: Check if user exists
                if not user:
                    return {
                        'success': False,
                        'user': None,
                        'message': 'Invalid username or password'
                    }
                
                # Step 3: Check if user is active
                if not user.is_active:
                    return {
                        'success': False,
                        'user': None,
                        'message': 'Account is inactive'
                    }
                
                # Step 4: Verify password using verify_password function
                # ✅ CORRECT WAY - Use verify_password()
                if not verify_password(password, user.password_hash):
                    return {
                        'success': False,
                        'user': None,
                        'message': 'Invalid username or password'
                    }
                
                # Step 5: Update last login
                user.last_login = datetime.now()
                db.commit()
                
                # Step 6: Get additional user info
                user_dict = {
                    'user_id': user.user_id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'email': user.email,
                    'phone': user.phone,
                    'role': user.role.value,
                    'is_active': user.is_active
                }
                
                # If doctor, add doctor info
                if user.role.value == 'doctor':
                    doctor = db.query(Doctor).filter(
                        Doctor.user_id == user.user_id
                    ).first()
                    
                    if doctor:
                        user_dict.update({
                            'doctor_id': doctor.doctor_id,
                            'national_id': doctor.national_id,
                            'specialization': doctor.specialization,
                            'license_number': doctor.license_number,
                            'hospital': doctor.hospital
                        })
                
                return {
                    'success': True,
                    'user': user,  # Return SQLAlchemy object for session
                    'user_dict': user_dict,  # Return dict for display
                    'message': 'Login successful'
                }
        
        except Exception as e:
            print(f"Authentication error: {e}")
            return {
                'success': False,
                'user': None,
                'message': f'Authentication error: {str(e)}'
            }
    
    def get_user_by_id(self, user_id: int):
        """Get user by ID"""
        with get_db() as db:
            return db.query(User).filter(User.user_id == user_id).first()
    
    def get_user_by_username(self, username: str):
        """Get user by username"""
        with get_db() as db:
            return db.query(User).filter(User.username == username).first()
    
    def login(self, username: str, password: str):
        """
        Login method for backward compatibility with login_window.py
        Returns: (success, message, user_data)
        """
        result = self.authenticate(username, password)
        
        if result['success']:
            return (
                True,
                result['message'],
                result.get('user_dict', result['user'])
            )
        else:
            return (
                False,
                result['message'],
                None
            )
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> dict:
        """Change user password"""
        from utils.security import hash_password
        
        try:
            with get_db() as db:
                user = db.query(User).filter(User.user_id == user_id).first()
                
                if not user:
                    return {'success': False, 'message': 'User not found'}
                
                # Verify old password
                if not verify_password(old_password, user.password_hash):
                    return {'success': False, 'message': 'Current password is incorrect'}
                
                # Set new password
                user.password_hash = hash_password(new_password)
                db.commit()
                
                return {'success': True, 'message': 'Password changed successfully'}
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}


# Global instance
auth_manager = AuthManager()


# For backward compatibility
def get_auth_manager():
    """Get global auth manager instance"""
    return auth_manager