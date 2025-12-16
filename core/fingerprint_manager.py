"""
Fingerprint Manager - Biometric Authentication
MySQL Version - Compatible with existing GUI
"""

from datetime import datetime
from core.database import get_db
from database.models import Doctor, User, HardwareAuditLog
import uuid

class FingerprintManager:
    """Manage fingerprint biometric authentication for doctors"""
    
    def __init__(self):
        pass
    
    def enroll_fingerprint(self, user_id, fingerprint_id):
        """
        Enroll fingerprint for doctor
        
        Args:
            user_id: Doctor's user_id
            fingerprint_id: Fingerprint sensor ID (from hardware)
        """
        with get_db() as db:
            doctor = db.query(Doctor).filter(Doctor.user_id == user_id).first()
            
            if not doctor:
                return {'success': False, 'message': 'Doctor not found'}
            
            # Check if fingerprint ID already used
            existing = db.query(Doctor).filter(
                Doctor.fingerprint_id == fingerprint_id,
                Doctor.fingerprint_enrolled == True
            ).first()
            
            if existing and existing.user_id != user_id:
                return {'success': False, 'message': 'Fingerprint already enrolled to another doctor'}
            
            # Enroll fingerprint
            doctor.fingerprint_id = fingerprint_id
            doctor.fingerprint_enrolled = True
            doctor.fingerprint_enrollment_date = datetime.now().date()
            doctor.biometric_enabled = True
            
            db.commit()
            
            # Log event
            self._log_fingerprint_event(user_id, 'enrollment', True)
            
            return {'success': True, 'message': 'Fingerprint enrolled successfully'}
    
    def authenticate_fingerprint(self, fingerprint_id):
        """
        Authenticate doctor by fingerprint
        
        Args:
            fingerprint_id: Fingerprint ID from sensor
        
        Returns:
            dict with user info if successful
        """
        with get_db() as db:
            doctor = db.query(Doctor).filter(
                Doctor.fingerprint_id == fingerprint_id,
                Doctor.fingerprint_enrolled == True,
                Doctor.biometric_enabled == True
            ).first()
            
            if not doctor:
                self._log_fingerprint_event(None, 'authentication_failed', False, fingerprint_id)
                return {'success': False, 'message': 'Fingerprint not recognized'}
            
            # Get user info
            user = db.query(User).filter(User.user_id == doctor.user_id).first()
            
            if not user or user.account_status != 'active':
                self._log_fingerprint_event(doctor.user_id, 'authentication_failed', False)
                return {'success': False, 'message': 'Account inactive'}
            
            # Update login info
            user.last_login = datetime.now()
            user.login_count += 1
            
            doctor.last_fingerprint_login = datetime.now()
            doctor.fingerprint_login_count += 1
            
            db.commit()
            
            # Log successful authentication
            self._log_fingerprint_event(doctor.user_id, 'authentication_success', True, fingerprint_id)
            
            return {
                'success': True,
                'user_id': user.user_id,
                'username': user.username,
                'full_name': user.full_name,
                'role': user.role,
                'specialization': doctor.specialization
            }
    
    def remove_fingerprint(self, user_id):
        """Remove fingerprint enrollment"""
        with get_db() as db:
            doctor = db.query(Doctor).filter(Doctor.user_id == user_id).first()
            
            if not doctor:
                return {'success': False, 'message': 'Doctor not found'}
            
            doctor.fingerprint_id = None
            doctor.fingerprint_enrolled = False
            doctor.biometric_enabled = False
            
            db.commit()
            
            # Log event
            self._log_fingerprint_event(user_id, 'fingerprint_removed', True)
            
            return {'success': True, 'message': 'Fingerprint removed'}
    
    def is_enrolled(self, user_id):
        """Check if doctor has fingerprint enrolled"""
        with get_db() as db:
            doctor = db.query(Doctor).filter(Doctor.user_id == user_id).first()
            return doctor and doctor.fingerprint_enrolled
    
    def enable_biometric(self, user_id):
        """Enable biometric authentication"""
        with get_db() as db:
            doctor = db.query(Doctor).filter(Doctor.user_id == user_id).first()
            
            if not doctor:
                return {'success': False, 'message': 'Doctor not found'}
            
            if not doctor.fingerprint_enrolled:
                return {'success': False, 'message': 'No fingerprint enrolled'}
            
            doctor.biometric_enabled = True
            db.commit()
            
            return {'success': True, 'message': 'Biometric enabled'}
    
    def disable_biometric(self, user_id):
        """Disable biometric authentication"""
        with get_db() as db:
            doctor = db.query(Doctor).filter(Doctor.user_id == user_id).first()
            
            if not doctor:
                return {'success': False, 'message': 'Doctor not found'}
            
            doctor.biometric_enabled = False
            db.commit()
            
            return {'success': True, 'message': 'Biometric disabled'}
    
    def get_fingerprint_stats(self, user_id):
        """Get fingerprint usage statistics"""
        with get_db() as db:
            doctor = db.query(Doctor).filter(Doctor.user_id == user_id).first()
            
            if not doctor:
                return None
            
            return {
                'enrolled': doctor.fingerprint_enrolled,
                'enabled': doctor.biometric_enabled,
                'enrollment_date': doctor.fingerprint_enrollment_date,
                'last_login': doctor.last_fingerprint_login,
                'login_count': doctor.fingerprint_login_count
            }
    
    def get_all_enrolled_doctors(self):
        """Get all doctors with fingerprint enrolled"""
        with get_db() as db:
            doctors = db.query(Doctor).filter(
                Doctor.fingerprint_enrolled == True
            ).all()
            
            return [{
                'user_id': d.user_id,
                'full_name': d.user.full_name if d.user else 'Unknown',
                'fingerprint_id': d.fingerprint_id,
                'enabled': d.biometric_enabled,
                'login_count': d.fingerprint_login_count
            } for d in doctors]
    
    def _log_fingerprint_event(self, user_id, event_type, success, fingerprint_id=None):
        """Log fingerprint event to audit log"""
        with get_db() as db:
            log = HardwareAuditLog(
                event_id=f"FP-{uuid.uuid4().hex[:12]}",
                timestamp=datetime.now(),
                event_type=f"fingerprint_{event_type}",
                user_id=user_id,
                fingerprint_id=fingerprint_id,
                accessed_by=user_id,
                access_type='fingerprint',
                success=success
            )
            db.add(log)
            db.commit()
    
    def get_fingerprint_logs(self, user_id=None, limit=50):
        """Get fingerprint authentication logs"""
        with get_db() as db:
            query = db.query(HardwareAuditLog).filter(
                HardwareAuditLog.event_type.like('fingerprint_%')
            )
            
            if user_id:
                query = query.filter(HardwareAuditLog.user_id == user_id)
            
            return query.order_by(
                HardwareAuditLog.timestamp.desc()
            ).limit(limit).all()
    
    def get_failed_attempts(self, limit=20):
        """Get recent failed fingerprint attempts"""
        with get_db() as db:
            return db.query(HardwareAuditLog).filter(
                HardwareAuditLog.event_type == 'fingerprint_authentication_failed',
                HardwareAuditLog.success == False
            ).order_by(
                HardwareAuditLog.timestamp.desc()
            ).limit(limit).all()

# Global instance
fingerprint_manager = FingerprintManager()