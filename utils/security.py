"""
Security Utilities
Password hashing and verification using bcrypt
Location: utils/security.py
"""

import hashlib
import secrets
from typing import Optional

# Try to import bcrypt (better), fallback to hashlib
try:
    import bcrypt
    USE_BCRYPT = True
except ImportError:
    USE_BCRYPT = False
    print("⚠️  bcrypt not installed, using SHA-256 (less secure)")


def hash_password(password: str) -> str:
    """
    Hash a password for storing
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    if USE_BCRYPT:
        # Use bcrypt (recommended)
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    else:
        # Fallback to SHA-256 with salt
        salt = secrets.token_hex(16)
        hashed = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        return f"{salt}${hashed}"


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash
    
    Args:
        password: Plain text password to verify
        hashed_password: Stored hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    if USE_BCRYPT:
        # Use bcrypt
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False
    else:
        # Fallback to SHA-256 verification
        try:
            if '$' not in hashed_password:
                return False
            
            salt, stored_hash = hashed_password.split('$', 1)
            new_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
            return new_hash == stored_hash
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False


def generate_token(length: int = 32) -> str:
    """
    Generate a random token
    
    Args:
        length: Length of token in bytes (default: 32)
        
    Returns:
        Random token as hex string
    """
    return secrets.token_hex(length)


def generate_api_key() -> str:
    """
    Generate a secure API key
    
    Returns:
        API key string
    """
    return f"mk_{secrets.token_urlsafe(32)}"


# For backward compatibility
def encrypt_data(data: str, key: Optional[str] = None) -> str:
    """
    Simple data encryption (placeholder)
    For production, use proper encryption library like cryptography
    """
    # This is a placeholder - use proper encryption in production
    import base64
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')


def decrypt_data(encrypted_data: str, key: Optional[str] = None) -> str:
    """
    Simple data decryption (placeholder)
    For production, use proper encryption library like cryptography
    """
    # This is a placeholder - use proper encryption in production
    import base64
    try:
        return base64.b64decode(encrypted_data.encode('utf-8')).decode('utf-8')
    except Exception:
        return encrypted_data