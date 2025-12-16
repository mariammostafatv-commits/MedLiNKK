"""
Search Engine - Advanced Search Across All Medical Records
MySQL Version - Compatible with existing GUI
"""

from datetime import datetime, date
from core.database import get_db
from database.models import *
from sqlalchemy import or_, and_

class SearchEngine:
    """Advanced search engine for medical records"""
    
    def __init__(self):
        pass
    
    def search_patients(self, query, filters=None):
        """
        Search patients
        
        Args:
            query: Search term
            filters: dict with optional filters (blood_type, gender, age_min, age_max)
        """
        with get_db() as db:
            search = f"%{query}%"
            
            # Base query
            q = db.query(Patient).filter(
                or_(
                    Patient.full_name.like(search),
                    Patient.national_id.like(search),
                    Patient.phone.like(search),
                    Patient.email.like(search),
                    Patient.address.like(search)
                )
            )
            
            # Apply filters
            if filters:
                if 'blood_type' in filters:
                    q = q.filter(Patient.blood_type == filters['blood_type'])
                
                if 'gender' in filters:
                    q = q.filter(Patient.gender == filters['gender'])
                
                if 'age_min' in filters:
                    q = q.filter(Patient.age >= filters['age_min'])
                
                if 'age_max' in filters:
                    q = q.filter(Patient.age <= filters['age_max'])
            
            return q.order_by(Patient.full_name).all()
    
    def search_doctors(self, query):
        """Search doctors by name, specialization, or hospital"""
        with get_db() as db:
            search = f"%{query}%"
            
            return db.query(Doctor).join(User).filter(
                or_(
                    User.full_name.like(search),
                    Doctor.specialization.like(search),
                    Doctor.hospital.like(search),
                    Doctor.license_number.like(search)
                )
            ).order_by(User.full_name).all()
    
    def search_visits(self, query, filters=None):
        """
        Search visits
        
        filters can include: date_from, date_to, doctor_id, visit_type
        """
        with get_db() as db:
            search = f"%{query}%"
            
            q = db.query(Visit).filter(
                or_(
                    Visit.visit_id.like(search),
                    Visit.patient_national_id.like(search),
                    Visit.doctor_name.like(search),
                    Visit.hospital.like(search),
                    Visit.chief_complaint.like(search),
                    Visit.diagnosis.like(search)
                )
            )
            
            # Apply filters
            if filters:
                if 'date_from' in filters:
                    q = q.filter(Visit.date >= filters['date_from'])
                
                if 'date_to' in filters:
                    q = q.filter(Visit.date <= filters['date_to'])
                
                if 'doctor_id' in filters:
                    q = q.filter(Visit.doctor_id == filters['doctor_id'])
                
                if 'visit_type' in filters:
                    q = q.filter(Visit.visit_type == filters['visit_type'])
            
            return q.order_by(Visit.date.desc(), Visit.time.desc()).all()
    
    def search_lab_results(self, query, filters=None):
        """
        Search lab results
        
        filters can include: date_from, date_to, test_type, status
        """
        with get_db() as db:
            search = f"%{query}%"
            
            q = db.query(LabResult).filter(
                or_(
                    LabResult.result_id.like(search),
                    LabResult.patient_national_id.like(search),
                    LabResult.lab_name.like(search),
                    LabResult.test_type.like(search)
                )
            )
            
            # Apply filters
            if filters:
                if 'date_from' in filters:
                    q = q.filter(LabResult.date >= filters['date_from'])
                
                if 'date_to' in filters:
                    q = q.filter(LabResult.date <= filters['date_to'])
                
                if 'test_type' in filters:
                    q = q.filter(LabResult.test_type == filters['test_type'])
                
                if 'status' in filters:
                    q = q.filter(LabResult.status == filters['status'])
            
            return q.order_by(LabResult.date.desc()).all()
    
    def search_imaging_results(self, query, filters=None):
        """
        Search imaging results
        
        filters can include: date_from, date_to, imaging_type
        """
        with get_db() as db:
            search = f"%{query}%"
            
            q = db.query(ImagingResult).filter(
                or_(
                    ImagingResult.imaging_id.like(search),
                    ImagingResult.patient_national_id.like(search),
                    ImagingResult.imaging_center.like(search),
                    ImagingResult.body_part.like(search),
                    ImagingResult.findings.like(search)
                )
            )
            
            # Apply filters
            if filters:
                if 'date_from' in filters:
                    q = q.filter(ImagingResult.date >= filters['date_from'])
                
                if 'date_to' in filters:
                    q = q.filter(ImagingResult.date <= filters['date_to'])
                
                if 'imaging_type' in filters:
                    q = q.filter(ImagingResult.imaging_type == filters['imaging_type'])
            
            return q.order_by(ImagingResult.date.desc()).all()
    
    def search_medications(self, query):
        """Search current medications"""
        with get_db() as db:
            search = f"%{query}%"
            
            return db.query(CurrentMedication).filter(
                CurrentMedication.is_active == True,
                CurrentMedication.medication_name.like(search)
            ).all()
    
    def search_allergies(self, allergen):
        """Find patients with specific allergy"""
        with get_db() as db:
            search = f"%{allergen}%"
            
            return db.query(Allergy).filter(
                Allergy.allergen.like(search)
            ).all()
    
    def search_chronic_diseases(self, disease):
        """Find patients with specific chronic disease"""
        with get_db() as db:
            search = f"%{disease}%"
            
            return db.query(ChronicDisease).filter(
                ChronicDisease.disease_name.like(search),
                ChronicDisease.current_status == 'active'
            ).all()
    
    def search_all(self, query):
        """
        Universal search across all entities
        Returns a dict with results from all categories
        """
        results = {
            'patients': self.search_patients(query)[:10],
            'doctors': self.search_doctors(query)[:10],
            'visits': self.search_visits(query)[:10],
            'lab_results': self.search_lab_results(query)[:10],
            'imaging_results': self.search_imaging_results(query)[:10]
        }
        
        return results
    
    def advanced_patient_search(self, criteria):
        """
        Advanced patient search with multiple criteria
        
        criteria dict can include:
        - name: partial name match
        - national_id: partial ID match
        - blood_type: exact match
        - gender: exact match
        - age_min, age_max: age range
        - has_allergy: bool
        - has_chronic_disease: bool
        - has_nfc_card: bool
        """
        with get_db() as db:
            q = db.query(Patient)
            
            if 'name' in criteria:
                q = q.filter(Patient.full_name.like(f"%{criteria['name']}%"))
            
            if 'national_id' in criteria:
                q = q.filter(Patient.national_id.like(f"%{criteria['national_id']}%"))
            
            if 'blood_type' in criteria:
                q = q.filter(Patient.blood_type == criteria['blood_type'])
            
            if 'gender' in criteria:
                q = q.filter(Patient.gender == criteria['gender'])
            
            if 'age_min' in criteria:
                q = q.filter(Patient.age >= criteria['age_min'])
            
            if 'age_max' in criteria:
                q = q.filter(Patient.age <= criteria['age_max'])
            
            if 'has_nfc_card' in criteria:
                q = q.filter(Patient.nfc_card_assigned == criteria['has_nfc_card'])
            
            patients = q.all()
            
            # Filter by relationships (allergies, chronic diseases)
            if 'has_allergy' in criteria and criteria['has_allergy']:
                patients = [p for p in patients if len(p.allergies) > 0]
            
            if 'has_chronic_disease' in criteria and criteria['has_chronic_disease']:
                patients = [p for p in patients if len(p.chronic_diseases) > 0]
            
            return patients
    
    def search_by_diagnosis(self, diagnosis):
        """Search visits by diagnosis"""
        with get_db() as db:
            search = f"%{diagnosis}%"
            
            return db.query(Visit).filter(
                Visit.diagnosis.like(search)
            ).order_by(Visit.date.desc()).all()
    
    def search_by_medication(self, medication):
        """Search patients currently taking a specific medication"""
        with get_db() as db:
            search = f"%{medication}%"
            
            medications = db.query(CurrentMedication).filter(
                CurrentMedication.medication_name.like(search),
                CurrentMedication.is_active == True
            ).all()
            
            # Get unique patients
            patient_ids = list(set([m.patient_national_id for m in medications]))
            
            return db.query(Patient).filter(
                Patient.national_id.in_(patient_ids)
            ).all()
    
    def search_by_date_range(self, start_date, end_date, record_type='visits'):
        """
        Search records by date range
        
        record_type: 'visits', 'lab_results', 'imaging'
        """
        with get_db() as db:
            if record_type == 'visits':
                return db.query(Visit).filter(
                    Visit.date.between(start_date, end_date)
                ).order_by(Visit.date.desc()).all()
            
            elif record_type == 'lab_results':
                return db.query(LabResult).filter(
                    LabResult.date.between(start_date, end_date)
                ).order_by(LabResult.date.desc()).all()
            
            elif record_type == 'imaging':
                return db.query(ImagingResult).filter(
                    ImagingResult.date.between(start_date, end_date)
                ).order_by(ImagingResult.date.desc()).all()
    
    def get_patient_timeline(self, national_id):
        """Get complete timeline of patient events"""
        with get_db() as db:
            timeline = []
            
            # Visits
            visits = db.query(Visit).filter(
                Visit.patient_national_id == national_id
            ).all()
            for v in visits:
                timeline.append({
                    'type': 'visit',
                    'date': v.date,
                    'time': v.time,
                    'description': f"{v.visit_type} - {v.chief_complaint}",
                    'details': v.diagnosis
                })
            
            # Lab Results
            labs = db.query(LabResult).filter(
                LabResult.patient_national_id == national_id
            ).all()
            for l in labs:
                timeline.append({
                    'type': 'lab_result',
                    'date': l.date,
                    'description': f"Lab Test: {l.test_type}",
                    'details': l.status
                })
            
            # Imaging
            imaging = db.query(ImagingResult).filter(
                ImagingResult.patient_national_id == national_id
            ).all()
            for i in imaging:
                timeline.append({
                    'type': 'imaging',
                    'date': i.date,
                    'description': f"{i.imaging_type} - {i.body_part}",
                    'details': i.findings
                })
            
            # Surgeries
            surgeries = db.query(Surgery).filter(
                Surgery.patient_national_id == national_id
            ).all()
            for s in surgeries:
                timeline.append({
                    'type': 'surgery',
                    'date': s.date,
                    'description': f"Surgery: {s.procedure_name}",
                    'details': s.outcome
                })
            
            # Hospitalizations
            hosps = db.query(Hospitalization).filter(
                Hospitalization.patient_national_id == national_id
            ).all()
            for h in hosps:
                timeline.append({
                    'type': 'hospitalization',
                    'date': h.admission_date,
                    'description': f"Hospitalized: {h.hospital}",
                    'details': h.diagnosis
                })
            
            # Vaccinations
            vaccines = db.query(Vaccination).filter(
                Vaccination.patient_national_id == national_id
            ).all()
            for v in vaccines:
                timeline.append({
                    'type': 'vaccination',
                    'date': v.date_administered,
                    'description': f"Vaccine: {v.vaccine_name}",
                    'details': v.dose_number
                })
            
            # Sort by date (most recent first)
            timeline.sort(key=lambda x: x['date'], reverse=True)
            
            return timeline
    
    def quick_search(self, query, limit=20):
        """
        Quick search for autocomplete/suggestions
        Returns mixed results from patients, doctors, and records
        """
        with get_db() as db:
            search = f"%{query}%"
            results = []
            
            # Patients
            patients = db.query(Patient).filter(
                or_(
                    Patient.full_name.like(search),
                    Patient.national_id.like(search)
                )
            ).limit(5).all()
            
            for p in patients:
                results.append({
                    'type': 'patient',
                    'id': p.national_id,
                    'text': p.full_name,
                    'subtitle': p.national_id
                })
            
            # Doctors
            doctors = db.query(Doctor).join(User).filter(
                User.full_name.like(search)
            ).limit(5).all()
            
            for d in doctors:
                results.append({
                    'type': 'doctor',
                    'id': d.user_id,
                    'text': d.user.full_name,
                    'subtitle': d.specialization
                })
            
            # Visits
            visits = db.query(Visit).filter(
                Visit.visit_id.like(search)
            ).limit(5).all()
            
            for v in visits:
                results.append({
                    'type': 'visit',
                    'id': v.visit_id,
                    'text': f"Visit {v.visit_id}",
                    'subtitle': f"{v.doctor_name} - {v.date}"
                })
            
            return results[:limit]

# Global instance
search_engine = SearchEngine()