"""
Vaccination Manager - Manage Patient Vaccinations
MySQL Version - Compatible with existing GUI
"""

from datetime import datetime, date, timedelta
from core.database import get_db
from database.models import Vaccination, Patient

class VaccinationManager:
    """Manage patient vaccinations"""
    
    def __init__(self):
        pass
    
    def add_vaccination(self, national_id, vaccination_data):
        """
        Add vaccination record
        
        vaccination_data should contain:
        - vaccine_name: str
        - date_administered: date
        - dose_number: str (optional, e.g., '1st dose', '2nd dose')
        - location: str (optional, where vaccine was given)
        - batch_number: str (optional)
        - expiry_date: date (optional)
        - next_dose_due: date (optional)
        - administered_by: str (optional)
        - notes: str (optional)
        """
        with get_db() as db:
            # Check if patient exists
            patient = db.query(Patient).filter(
                Patient.national_id == national_id
            ).first()
            
            if not patient:
                return {'success': False, 'message': 'Patient not found'}
            
            # Convert date strings if needed
            for date_field in ['date_administered', 'expiry_date', 'next_dose_due']:
                if date_field in vaccination_data and isinstance(vaccination_data[date_field], str):
                    vaccination_data[date_field] = datetime.strptime(
                        vaccination_data[date_field], '%Y-%m-%d'
                    ).date()
            
            vaccination = Vaccination(
                patient_national_id=national_id,
                **vaccination_data
            )
            db.add(vaccination)
            db.commit()
            db.refresh(vaccination)
            
            return {
                'success': True,
                'vaccination': vaccination,
                'message': 'Vaccination record added'
            }
    
    def get_vaccinations(self, national_id):
        """Get all vaccinations for patient"""
        with get_db() as db:
            return db.query(Vaccination).filter(
                Vaccination.patient_national_id == national_id
            ).order_by(Vaccination.date_administered.desc()).all()
    
    def get_vaccination(self, vaccination_id):
        """Get specific vaccination by ID"""
        with get_db() as db:
            return db.query(Vaccination).filter(
                Vaccination.id == vaccination_id
            ).first()
    
    def update_vaccination(self, vaccination_id, update_data):
        """Update vaccination record"""
        with get_db() as db:
            vaccination = db.query(Vaccination).filter(
                Vaccination.id == vaccination_id
            ).first()
            
            if not vaccination:
                return {'success': False, 'message': 'Vaccination not found'}
            
            for key, value in update_data.items():
                if hasattr(vaccination, key):
                    # Convert date strings if needed
                    if key in ['date_administered', 'expiry_date', 'next_dose_due'] and isinstance(value, str):
                        value = datetime.strptime(value, '%Y-%m-%d').date()
                    setattr(vaccination, key, value)
            
            db.commit()
            db.refresh(vaccination)
            
            return {'success': True, 'vaccination': vaccination, 'message': 'Vaccination updated'}
    
    def delete_vaccination(self, vaccination_id):
        """Delete vaccination record"""
        with get_db() as db:
            vaccination = db.query(Vaccination).filter(
                Vaccination.id == vaccination_id
            ).first()
            
            if vaccination:
                db.delete(vaccination)
                db.commit()
                return {'success': True, 'message': 'Vaccination deleted'}
            
            return {'success': False, 'message': 'Vaccination not found'}
    
    def get_vaccinations_by_vaccine(self, national_id, vaccine_name):
        """Get all doses of a specific vaccine"""
        with get_db() as db:
            return db.query(Vaccination).filter(
                Vaccination.patient_national_id == national_id,
                Vaccination.vaccine_name.like(f"%{vaccine_name}%")
            ).order_by(Vaccination.date_administered).all()
    
    def get_upcoming_vaccinations(self, national_id, days_ahead=30):
        """Get vaccinations due in next N days"""
        with get_db() as db:
            today = date.today()
            future_date = today + timedelta(days=days_ahead)
            
            return db.query(Vaccination).filter(
                Vaccination.patient_national_id == national_id,
                Vaccination.next_dose_due.isnot(None),
                Vaccination.next_dose_due.between(today, future_date)
            ).order_by(Vaccination.next_dose_due).all()
    
    def get_overdue_vaccinations(self, national_id):
        """Get vaccinations that are overdue"""
        with get_db() as db:
            today = date.today()
            
            return db.query(Vaccination).filter(
                Vaccination.patient_national_id == national_id,
                Vaccination.next_dose_due.isnot(None),
                Vaccination.next_dose_due < today
            ).order_by(Vaccination.next_dose_due).all()
    
    def get_vaccination_history(self, national_id, vaccine_name=None):
        """Get vaccination history, optionally filtered by vaccine"""
        vaccinations = self.get_vaccinations(national_id)
        
        if vaccine_name:
            vaccinations = [v for v in vaccinations if vaccine_name.lower() in v.vaccine_name.lower()]
        
        return [{
            'vaccine_name': v.vaccine_name,
            'date': v.date_administered,
            'dose_number': v.dose_number,
            'location': v.location,
            'administered_by': v.administered_by,
            'next_dose_due': v.next_dose_due
        } for v in vaccinations]
    
    def is_vaccine_current(self, national_id, vaccine_name):
        """Check if patient is current on a specific vaccine"""
        vaccinations = self.get_vaccinations_by_vaccine(national_id, vaccine_name)
        
        if not vaccinations:
            return False
        
        # Check latest vaccination
        latest = vaccinations[-1]  # Most recent
        
        # If no next dose due, vaccine is complete
        if not latest.next_dose_due:
            return True
        
        # Check if next dose is not overdue
        return latest.next_dose_due >= date.today()
    
    def get_vaccination_statistics(self, national_id):
        """Get vaccination statistics for patient"""
        vaccinations = self.get_vaccinations(national_id)
        
        if not vaccinations:
            return None
        
        # Count unique vaccines
        vaccines = {}
        for v in vaccinations:
            vaccine_name = v.vaccine_name
            if vaccine_name in vaccines:
                vaccines[vaccine_name] += 1
            else:
                vaccines[vaccine_name] = 1
        
        # Check for upcoming/overdue
        upcoming = self.get_upcoming_vaccinations(national_id)
        overdue = self.get_overdue_vaccinations(national_id)
        
        return {
            'total_vaccinations': len(vaccinations),
            'unique_vaccines': len(vaccines),
            'vaccines': vaccines,
            'upcoming_count': len(upcoming),
            'overdue_count': len(overdue),
            'most_recent': vaccinations[0] if vaccinations else None
        }
    
    def get_all_upcoming_vaccinations(self, days_ahead=30):
        """Get all upcoming vaccinations across all patients"""
        with get_db() as db:
            today = date.today()
            future_date = today + timedelta(days=days_ahead)
            
            return db.query(Vaccination).filter(
                Vaccination.next_dose_due.isnot(None),
                Vaccination.next_dose_due.between(today, future_date)
            ).order_by(Vaccination.next_dose_due).all()
    
    def search_vaccinations(self, search_term):
        """Search vaccinations by vaccine name or patient"""
        with get_db() as db:
            search = f"%{search_term}%"
            
            return db.query(Vaccination).join(Patient).filter(
                (Vaccination.vaccine_name.like(search)) |
                (Patient.full_name.like(search)) |
                (Vaccination.administered_by.like(search))
            ).order_by(Vaccination.date_administered.desc()).all()

# Global instance
vaccination_manager = VaccinationManager()