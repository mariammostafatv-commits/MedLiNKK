"""
AUTO-CREATE ALL MISSING FILES
Creates all required __init__.py and fixes imports

Run: python auto_create_files.py
"""

from pathlib import Path

print("="*70)
print("  AUTO-CREATING MISSING FILES")
print("="*70)
print()

# File contents
UTILS_INIT = """\"\"\"
Utils Package
Utility functions for MedLink
\"\"\"

from .security import hash_password, verify_password

__all__ = ['hash_password', 'verify_password']
"""

DATABASE_INIT = """\"\"\"
Database Package
Database setup and management for MedLink
\"\"\"

from .setup_database_with_data import setup_with_data, DataSeeder

__all__ = ['setup_with_data', 'DataSeeder']
"""

UTILS_SECURITY = """\"\"\"
Security Utilities - Password hashing
\"\"\"

import hashlib
import secrets

def hash_password(password: str) -> str:
    \"\"\"Hash a password using SHA-256 with salt\"\"\"
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return f"{salt}${hashed}"

def verify_password(password: str, hashed_password: str) -> bool:
    \"\"\"Verify password against hash\"\"\"
    try:
        if '$' not in hashed_password:
            return False
        salt, stored_hash = hashed_password.split('$', 1)
        new_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        return new_hash == stored_hash
    except:
        return False
"""

# Create files
files_created = 0

try:
    # 1. Create utils/__init__.py
    utils_init = Path("utils/__init__.py")
    if not utils_init.exists():
        utils_init.write_text(UTILS_INIT, encoding='utf-8')
        print("✅ Created: utils/__init__.py")
        files_created += 1
    else:
        print("⚠️  Exists: utils/__init__.py")
    
    # 2. Check utils/security.py has hash_password
    utils_security = Path("utils/security.py")
    if utils_security.exists():
        content = utils_security.read_text(encoding='utf-8')
        if 'def hash_password' not in content:
            print("⚠️  utils/security.py missing hash_password - creating backup and fixing...")
            utils_security.rename("utils/security.py.backup")
            utils_security.write_text(UTILS_SECURITY, encoding='utf-8')
            print("✅ Fixed: utils/security.py")
            files_created += 1
        else:
            print("✅ OK: utils/security.py has hash_password")
    else:
        utils_security.write_text(UTILS_SECURITY, encoding='utf-8')
        print("✅ Created: utils/security.py")
        files_created += 1
    
    # 3. Create database/__init__.py
    db_init = Path("database/__init__.py")
    if not db_init.exists():
        db_init.write_text(DATABASE_INIT, encoding='utf-8')
        print("✅ Created: database/__init__.py")
        files_created += 1
    else:
        print("⚠️  Exists: database/__init__.py")
    
    print()
    print("="*70)
    print(f"  {files_created} FILES CREATED/FIXED")
    print("="*70)
    print()
    print("Next steps:")
    print("1. Run: python database\\db_manager.py setup")
    print("2. Test: python main.py")
    print()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
