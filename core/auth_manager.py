"""
Authentication Manager
Handles user login, registration, and authentication
"""

import hashlib
from datetime import datetime
from core.database import get_db
from database.models import User, Doctor, Patient

class AuthManager:
    """Manage user authentication"""
    
    def __init__(self):
        pass
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str):
        """
        Authenticate user
        Returns: User object if successful, None otherwise
        """
        with get_db() as db:
            password_hash = self.hash_password(password)
            
            user = db.query(User).filter(
                User.username == username,
                User.password_hash == password_hash
            ).first()
            
            if user and user.account_status == 'active':
                # Update login info
                user.last_login = datetime.now()
                user.login_count += 1
                db.commit()
                
                return user
            
            return None
    
    def get_user_by_username(self, username: str):
        """Get user by username"""
        with get_db() as db:
            return db.query(User).filter(User.username == username).first()
    
    def get_user_by_id(self, user_id: str):
        """Get user by user_id"""
        with get_db() as db:
            return db.query(User).filter(User.user_id == user_id).first()
    
    def create_user(self, user_data: dict):
        """
        Create new user
        user_data should contain: user_id, username, password, role, full_name, etc.
        """
        with get_db() as db:
            # Hash password
            user_data['password_hash'] = self.hash_password(user_data.pop('password'))
            
            # Create user
            user = User(**user_data)
            db.add(user)
            db.commit()
            db.refresh(user)
            
            return user
    
    def update_password(self, username: str, new_password: str):
        """Update user password"""
        with get_db() as db:
            user = db.query(User).filter(User.username == username).first()
            
            if user:
                user.password_hash = self.hash_password(new_password)
                db.commit()
                return True
            
            return False
    
    def check_username_exists(self, username: str) -> bool:
        """Check if username already exists"""
        with get_db() as db:
            user = db.query(User).filter(User.username == username).first()
            return user is not None
    
    def get_user_role(self, username: str) -> str:
        """Get user role"""
        with get_db() as db:
            user = db.query(User).filter(User.username == username).first()
            return user.role if user else None
    
    def activate_user(self, username: str):
        """Activate user account"""
        with get_db() as db:
            user = db.query(User).filter(User.username == username).first()
            if user:
                user.account_status = 'active'
                db.commit()
                return True
            return False
    
    def deactivate_user(self, username: str):
        """Deactivate user account"""
        with get_db() as db:
            user = db.query(User).filter(User.username == username).first()
            if user:
                user.account_status = 'inactive'
                db.commit()
                return True
            return False

# Global instance
auth_manager = AuthManager()