"""
Authentication Manager - Database Version
Handles user authentication using database instead of JSON
Location: core/auth_manager.py
"""
import hashlib
from datetime import datetime
from database.connection import get_db_context
from database.models import User
from utils.security import security


class AuthManager:
    """
    Manages user authentication with database backend
    Compatible with existing GUI - same method signatures
    """
    
    def __init__(self):
        """Initialize authentication manager"""
        self.current_user = None
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, username, password, remember_me=False):
        """
        Authenticate user with username and password
        
        Args:
            username: Username
            password: Plain text password
            remember_me: Optional remember me flag (for GUI compatibility)
        
        Returns:
            dict: User data if successful, None otherwise
        """
        password_hash = self.hash_password(password)
        
        with get_db_context() as db:
            user = db.query(User).filter_by(
                username=username,
                password_hash=password_hash
            ).first()
            
            if user:
                # Update last login
                user.last_login = datetime.now()
                
                # Convert to dictionary INSIDE session context
                user_dict = self._user_to_dict(user)
                
                # Auto-commits on exit
            else:
                return None
        
        # Set current user and return (after session closes)
        if not user:
            return False, "Invalid username or role", None

            # Verify password
        if not security.verify_password(password, user.password_hash):
                return False, "Invalid password", None

            # Set session
        self.current_user = user
        self.session_start = datetime.now()

        return True, "Login successful", user
        
    def login_with_fingerprint(self, fingerprint_id):
        """
        Authenticate user with fingerprint
        
        Args:
            fingerprint_id: Fingerprint identifier
        
        Returns:
            dict: User data if successful, None otherwise
        """
        with get_db_context() as db:
            user = db.query(User).filter_by(
                fingerprint_id=fingerprint_id,
                fingerprint_enrolled=True
            ).first()
            
            if user:
                # Update last fingerprint login
                user.last_fingerprint_login = datetime.now()
                user.last_login = datetime.now()
                
                # Convert to dictionary INSIDE session context
                user_dict = self._user_to_dict(user)
                
                # Auto-commits on exit
            else:
                return None
        
        # Set current user and return (after session closes)
        self.current_user = user_dict
        return self.current_user
    
    def register_user(self, user_data):
        """
        Register new user
        
        Args:
            user_data: Dictionary with user information
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Hash password
            if 'password' in user_data:
                user_data['password_hash'] = self.hash_password(user_data.pop('password'))
            
            # Set created timestamp
            user_data['created_at'] = datetime.now()
            
            with get_db_context() as db:
                # Check if username already exists
                existing = db.query(User).filter_by(username=user_data['username']).first()
                if existing:
                    return False
                
                # Create new user
                user = User(**user_data)
                db.add(user)
                # Auto-commits on exit
            
            return True
            
        except Exception as e:
            print(f"Error registering user: {e}")
            return False
    
    def get_user(self, username):
        """
        Get user by username
        
        Args:
            username: Username
        
        Returns:
            dict: User data if found, None otherwise
        """
        with get_db_context() as db:
            user = db.query(User).filter_by(username=username).first()
            if user:
                return self._user_to_dict(user)
        return None
    
    def get_user_by_id(self, user_id):
        """
        Get user by user_id
        
        Args:
            user_id: User ID
        
        Returns:
            dict: User data if found, None otherwise
        """
        with get_db_context() as db:
            user = db.query(User).filter_by(user_id=user_id).first()
            if user:
                return self._user_to_dict(user)
        return None
    
    def update_user(self, username, updates):
        """
        Update user information
        
        Args:
            username: Username
            updates: Dictionary of fields to update
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Hash password if being updated
            if 'password' in updates:
                updates['password_hash'] = self.hash_password(updates.pop('password'))
            
            with get_db_context() as db:
                user = db.query(User).filter_by(username=username).first()
                if not user:
                    return False
                
                # Update fields
                for key, value in updates.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                
                # Auto-commits on exit
            
            return True
            
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def enroll_fingerprint(self, username, fingerprint_id):
        """
        Enroll fingerprint for user
        
        Args:
            username: Username
            fingerprint_id: Fingerprint identifier
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with get_db_context() as db:
                user = db.query(User).filter_by(username=username).first()
                if not user:
                    return False
                
                user.fingerprint_id = fingerprint_id
                user.fingerprint_enrolled = True
                user.fingerprint_enrollment_date = datetime.now().date()
                
                # Auto-commits on exit
            
            return True
            
        except Exception as e:
            print(f"Error enrolling fingerprint: {e}")
            return False
    
    def get_all_users(self, role=None):
        """
        Get all users, optionally filtered by role
        
        Args:
            role: Optional role filter (doctor, patient, admin, nurse)
        
        Returns:
            list: List of user dictionaries
        """
        with get_db_context() as db:
            query = db.query(User)
            
            if role:
                query = query.filter_by(role=role)
            
            users = query.all()
            # Convert all to dict inside session
            return [self._user_to_dict(user) for user in users]
    
    def get_all_doctors(self):
        """Get all doctor users"""
        return self.get_all_users(role='doctor')
    
    def get_all_patients(self):
        """Get all patient users (for login accounts)"""
        return self.get_all_users(role='patient')
    
    def delete_user(self, username):
        """
        Delete user
        
        Args:
            username: Username
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with get_db_context() as db:
                user = db.query(User).filter_by(username=username).first()
                if not user:
                    return False
                
                db.delete(user)
                # Auto-commits on exit
            
            return True
            
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return self.current_user is not None
    
    def _user_to_dict(self, user):
        """
        Convert User model to dictionary (helper method)
        Call this ONLY inside a database session context
        
        Args:
            user: User SQLAlchemy model
        
        Returns:
            dict: User data as dictionary
        """
        if not user:
            return None
        
        return {
            'user_id': user.user_id,
            'username': user.username,
            'password_hash': user.password_hash,
            'role': user.role,
            'full_name': user.full_name,
            'email': user.email,
            'phone': user.phone,
            
            # Doctor-specific fields
            'specialization': user.specialization,
            'hospital': user.hospital,
            'license_number': user.license_number,
            
            # Patient-specific fields
            'national_id': user.national_id,
            
            # Fingerprint fields
            'fingerprint_id': user.fingerprint_id,
            'fingerprint_enrolled': user.fingerprint_enrolled,
            'fingerprint_enrollment_date': str(user.fingerprint_enrollment_date) if user.fingerprint_enrollment_date else None,
            'last_fingerprint_login': str(user.last_fingerprint_login) if user.last_fingerprint_login else None,
            
            # Timestamps
            'created_at': str(user.created_at) if user.created_at else None,
            'last_login': str(user.last_login) if user.last_login else None
        }


# Singleton instance
_auth_manager = None

def get_auth_manager():
    """Get singleton instance of AuthManager"""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager