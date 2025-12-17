"""
COMPLETE RELATIONSHIP FIX - User ↔ Doctor
Fixes all SQLAlchemy relationship errors

Run: python fix_relationships.py
"""

from pathlib import Path
import re

print("="*70)
print("  FIXING USER ↔ DOCTOR RELATIONSHIPS")
print("="*70)
print()

# Check models.py exists
models_file = Path("core/models.py")
if not models_file.exists():
    print("❌ core/models.py not found!")
    exit(1)

print("✅ Found core/models.py")

# Read content
content = models_file.read_text(encoding='utf-8')

# Backup
backup_file = Path("core/models.py.backup_relationships")
if not backup_file.exists():
    print("💾 Creating backup: core/models.py.backup_relationships")
    backup_file.write_text(content, encoding='utf-8')

print("\n🔍 Checking relationships...\n")

# Check User model
user_has_doctor = 'doctor = relationship("Doctor"' in content or "doctor = relationship('Doctor'" in content
print(f"   User model 'doctor' relationship: {'✅ Found' if user_has_doctor else '❌ Missing'}")

# Check Doctor model
doctor_has_user = 'user = relationship("User"' in content or "user = relationship('User'" in content
print(f"   Doctor model 'user' relationship: {'✅ Found' if doctor_has_user else '❌ Missing'}")

if user_has_doctor and doctor_has_user:
    print("\n✅ Both relationships exist!")
    print("   The issue might be elsewhere. Checking...")
    
    # Check if they reference each other correctly
    user_section = content[content.find('class User(Base):'):content.find('class User(Base):') + 2000]
    doctor_section = content[content.find('class Doctor(Base):'):content.find('class Doctor(Base):') + 2000]
    
    user_backpop = 'back_populates="user"' in user_section or "back_populates='user'" in user_section
    doctor_backpop = 'back_populates="doctor"' in doctor_section or "back_populates='doctor'" in doctor_section
    
    print(f"\n   User.doctor back_populates='user': {'✅' if user_backpop else '❌'}")
    print(f"   Doctor.user back_populates='doctor': {'✅' if doctor_backpop else '❌'}")
    
    if user_backpop and doctor_backpop:
        print("\n✅ Relationships are correctly configured!")
        print("\n⚠️  If you're still getting errors, try:")
        print("   1. Delete __pycache__: rmdir /s /q core\\__pycache__")
        print("   2. Recreate database: python database\\db_manager.py setup")
        print("   3. Restart Python: Close terminal and reopen")
    else:
        print("\n❌ Relationships exist but back_populates is wrong!")
        print("   Fixing...")

print("\n🔧 Applying fixes...\n")

fixes_applied = 0

# Fix 1: Ensure User model has doctor relationship
if not user_has_doctor:
    print("   📝 Adding 'doctor' relationship to User model...")
    
    # Find User class and add relationship before __repr__
    user_class_start = content.find('class User(Base):')
    if user_class_start != -1:
        repr_pos = content.find('def __repr__(self):', user_class_start)
        if repr_pos != -1:
            # Insert before __repr__
            relationship_code = '''    
    # Relationships
    doctor = relationship("Doctor", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
'''
            content = content[:repr_pos] + relationship_code + content[repr_pos:]
            fixes_applied += 1
            print("      ✅ Added User.doctor relationship")

# Fix 2: Ensure Doctor model has user relationship
if not doctor_has_user:
    print("   📝 Adding 'user' relationship to Doctor model...")
    
    # Find Doctor class and add relationship before __repr__
    doctor_class_start = content.find('class Doctor(Base):')
    if doctor_class_start != -1:
        repr_pos = content.find('def __repr__(self):', doctor_class_start)
        if repr_pos != -1:
            # Insert before __repr__
            relationship_code = '''    
    # Relationships
    user = relationship("User", back_populates="doctor")
    visits = relationship("Visit", back_populates="doctor", cascade="all, delete-orphan")
    
'''
            content = content[:repr_pos] + relationship_code + content[repr_pos:]
            fixes_applied += 1
            print("      ✅ Added Doctor.user relationship")

if fixes_applied > 0:
    # Write fixed content
    models_file.write_text(content, encoding='utf-8')
    print(f"\n✅ Applied {fixes_applied} fix(es)!")
else:
    print("\n✅ No fixes needed!")

print()
print("="*70)
print("  NEXT STEPS")
print("="*70)
print()
print("1. ✅ Clear Python cache:")
print("   rmdir /s /q core\\__pycache__")
print("   rmdir /s /q database\\__pycache__")
print()
print("2. ✅ Recreate database:")
print("   python database\\db_manager.py setup")
print()
print("3. ✅ Test NFC login:")
print("   python main.py")
print()
print("Expected: ✅ NFC card login works!")
print()
