"""
Doctor Manager
Handles doctor-related operations
"""

from datetime import datetime
from core.database import get_db
from database.models import Doctor, User, Visit

class DoctorManager:
    """Manage doctor records"""
    
    def get_doctor(self, user_id: str):
        """Get doctor by user_id"""
        with get_db() as db:
            return db.query(Doctor).filter(Doctor.user_id == user_id).first()
    
    def get_doctor_by_license(self, license_number: str):
        """Get doctor by license number"""
        with get_db() as db:
            return db.query(Doctor).filter(
                Doctor.license_number == license_number
            ).first()
    
    def get_all_doctors(self):
        """Get all doctors"""
        with get_db() as db:
            return db.query(Doctor).join(User).order_by(User.full_name).all()
    
    def create_doctor(self, doctor_data: dict):
        """Create new doctor profile"""
        with get_db() as db:
            doctor = Doctor(**doctor_data)
            db.add(doctor)
            db.commit()
            db.refresh(doctor)
            return doctor
    
    def update_doctor(self, user_id: str, update_data: dict):
        """Update doctor information"""
        with get_db() as db:
            doctor = db.query(Doctor).filter(Doctor.user_id == user_id).first()
            
            if doctor:
                for key, value in update_data.items():
                    if hasattr(doctor, key):
                        setattr(doctor, key, value)
                
                db.commit()
                db.refresh(doctor)
                return doctor
            
            return None
    
    def get_doctor_with_user(self, user_id: str):
        """Get doctor with user information"""
        with get_db() as db:
            doctor = db.query(Doctor).filter(Doctor.user_id == user_id).first()
            if doctor:
                db.refresh(doctor)
                return {
                    'doctor': doctor,
                    'user': doctor.user
                }
            return None
    
    def search_doctors(self, search_term: str):
        """Search doctors by name or specialization"""
        with get_db() as db:
            search = f"%{search_term}%"
            doctors = db.query(Doctor).join(User).filter(
                (User.full_name.like(search)) |
                (Doctor.specialization.like(search)) |
                (Doctor.hospital.like(search))
            ).all()
            
            return doctors
    
    def get_doctors_by_specialization(self, specialization: str):
        """Get doctors by specialization"""
        with get_db() as db:
            return db.query(Doctor).filter(
                Doctor.specialization == specialization
            ).all()
    
    def get_doctor_stats(self, user_id: str):
        """Get doctor statistics"""
        with get_db() as db:
            doctor = db.query(Doctor).filter(Doctor.user_id == user_id).first()
            
            if not doctor:
                return None
            
            total_visits = db.query(Visit).filter(
                Visit.doctor_id == user_id
            ).count()
            
            recent_visits = db.query(Visit).filter(
                Visit.doctor_id == user_id
            ).order_by(Visit.date.desc()).limit(10).all()
            
            return {
                'doctor': doctor,
                'total_visits': total_visits,
                'recent_visits': recent_visits,
                'fingerprint_login_count': doctor.fingerprint_login_count,
                'last_login': doctor.last_fingerprint_login
            }

# Global instance
doctor_manager = DoctorManager()