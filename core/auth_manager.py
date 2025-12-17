"""
FIXED Authentication Manager - Works with GUI
Location: core/auth_manager.py (REPLACE YOUR FILE)
"""

import hashlib
from datetime import datetime
from core.database import get_db, get_db_context
from core.models import User

class AuthManager:
    """Manage user authentication - COMPLETE FIX"""
    
    def __init__(self):
        self.current_user = None
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str):
        """
        Authenticate user - Returns dict or None
        BACKWARD COMPATIBLE with old code
        """
        db = get_db()
        try:
            password_hash = self.hash_password(password)
            
            user = db.query(User).filter(
                User.username == username,
                User.password_hash == password_hash
            ).first()
            
            if user and user.account_status.value == 'active':
                # Update login info
                user.last_login = datetime.now()
                user.login_count = (user.login_count or 0) + 1
                db.commit()
                
                # Convert to dict while in session (CRITICAL!)
                user_dict = {
                    'user_id': user.user_id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'email': user.email,
                    'phone': user.phone,
                    'role': user.role.value,
                    'national_id': user.national_id,
                    'specialization': user.specialization,
                    'hospital': user.hospital,
                    'license_number': user.license_number,
                    'last_login': user.last_login,
                    'login_count': user.login_count
                }
                
                self.current_user = user_dict
                return user_dict
            
            return None
            
        finally:
            db.close()
    
    def login(self, username: str, password: str, role: str = None):
        """
        Login user - Returns tuple (success, message, user_data)
        NEW METHOD for GUI compatibility
        """
        db = get_db()
        try:
            password_hash = self.hash_password(password)
            
            # Query user
            user = db.query(User).filter(
                User.username == username,
                User.password_hash == password_hash
            ).first()
            print(User.password_hash)
            if not user:
                return False, "Invalid username or password", None
            
            # Check account status
            if user.account_status.value != 'active':
                return False, "Account is inactive", None
            
            # Check role if specified
            if role and user.role.value != role:
                return False, f"This account is not a {role} account", None
            
            # Update login info
            user.last_login = datetime.now()
            user.login_count = (user.login_count or 0) + 1
            db.commit()
            
            # Convert to dict while in session
            user_data = {
                'user_id': user.user_id,
                'username': user.username,
                'full_name': user.full_name,
                'email': user.email,
                'phone': user.phone,
                'role': user.role.value,
                'national_id': user.national_id,
                'specialization': user.specialization,
                'hospital': user.hospital,
                'license_number': user.license_number,
                'last_login': user.last_login,
                'login_count': user.login_count
            }
            
            self.current_user = user_data
            return True, f"Welcome, {user.full_name}!", user_data
            
        except Exception as e:
            return False, f"Login error: {str(e)}", None
        finally:
            db.close()
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return self.current_user is not None
    
    def get_current_user(self):
        """Get current logged in user"""
        return self.current_user
    
    def get_user_by_username(self, username: str):
        """Get user by username - returns dict"""
        db = get_db()
        try:
            user = db.query(User).filter(User.username == username).first()
            
            if user:
                return {
                    'user_id': user.user_id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'role': user.role.value,
                    'national_id': user.national_id
                }
            return None
        finally:
            db.close()
    
    def get_user_by_id(self, user_id: str):
        """Get user by user_id - returns dict"""
        db = get_db()
        try:
            user = db.query(User).filter(User.user_id == user_id).first()
            
            if user:
                return {
                    'user_id': user.user_id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'role': user.role.value,
                    'specialization': user.specialization,
                    'hospital': user.hospital
                }
            return None
        finally:
            db.close()
    
    def create_user(self, user_data: dict):
        """Create new user"""
        db = get_db()
        try:
            # Hash password
            if 'password' in user_data:
                user_data['password_hash'] = self.hash_password(user_data.pop('password'))
            
            user = User(**user_data)
            db.add(user)
            db.commit()
            db.refresh(user)
            
            return {
                'user_id': user.user_id,
                'username': user.username,
                'full_name': user.full_name
            }
        except Exception as e:
            db.rollback()
            print(f"Error creating user: {e}")
            return None
        finally:
            db.close()
    
    def update_password(self, username: str, new_password: str):
        """Update user password"""
        db = get_db()
        try:
            user = db.query(User).filter(User.username == username).first()
            
            if user:
                user.password_hash = self.hash_password(new_password)
                db.commit()
                return True
            return False
        except:
            db.rollback()
            return False
        finally:
            db.close()
    
    def check_username_exists(self, username: str) -> bool:
        """Check if username already exists"""
        db = get_db()
        try:
            user = db.query(User).filter(User.username == username).first()
            return user is not None
        finally:
            db.close()
    
    def get_user_role(self, username: str) -> str:
        """Get user role"""
        db = get_db()
        try:
            user = db.query(User).filter(User.username == username).first()
            return user.role.value if user else None
        finally:
            db.close()
    
    def activate_user(self, username: str):
        """Activate user account"""
        db = get_db()
        try:
            user = db.query(User).filter(User.username == username).first()
            if user:
                user.account_status = 'active'
                db.commit()
                return True
            return False
        except:
            db.rollback()
            return False
        finally:
            db.close()
    
    def deactivate_user(self, username: str):
        """Deactivate user account"""
        db = get_db()
        try:
            user = db.query(User).filter(User.username == username).first()
            if user:
                user.account_status = 'inactive'
                db.commit()
                return True
            return False
        except:
            db.rollback()
            return False
        finally:
            db.close()
    
    def get_all_doctors(self):
        """Get all doctors - returns list of dicts"""
        db = get_db()
        try:
            doctors = db.query(User).filter(User.role == 'doctor').all()
            
            return [{
                'user_id': d.user_id,
                'username': d.username,
                'full_name': d.full_name,
                'specialization': d.specialization,
                'hospital': d.hospital,
                'license_number': d.license_number
            } for d in doctors]
        finally:
            db.close()


# Global instance
auth_manager = AuthManager()