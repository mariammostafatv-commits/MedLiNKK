"""
Disability Manager - Manage Patient Disabilities
MySQL Version - Compatible with existing GUI
"""

from datetime import datetime
from core.database import get_db
from database.models import Disability, Patient

class DisabilityManager:
    """Manage patient disability information"""
    
    def __init__(self):
        pass
    
    def get_disability(self, national_id):
        """Get disability information for patient"""
        with get_db() as db:
            return db.query(Disability).filter(
                Disability.patient_national_id == national_id
            ).first()
    
    def has_disability(self, national_id):
        """Check if patient has disability record"""
        disability = self.get_disability(national_id)
        return disability and disability.has_disability
    
    def create_disability_record(self, national_id, disability_data):
        """
        Create disability record for patient
        
        disability_data should contain:
        - has_disability: bool
        - disability_type: str (optional)
        - mobility_aids: list (optional)
        - hearing_impairment: bool
        - visual_impairment: bool
        - cognitive_impairment: bool
        - communication_needs: list (optional)
        - accessibility_requirements: list (optional)
        - notes: str (optional)
        """
        with get_db() as db:
            # Check if patient exists
            patient = db.query(Patient).filter(
                Patient.national_id == national_id
            ).first()
            
            if not patient:
                return {'success': False, 'message': 'Patient not found'}
            
            # Check if disability record already exists
            existing = db.query(Disability).filter(
                Disability.patient_national_id == national_id
            ).first()
            
            if existing:
                return {'success': False, 'message': 'Disability record already exists'}
            
            disability = Disability(
                patient_national_id=national_id,
                **disability_data
            )
            db.add(disability)
            db.commit()
            db.refresh(disability)
            
            return {'success': True, 'disability': disability, 'message': 'Disability record created'}
    
    def update_disability(self, national_id, update_data):
        """Update disability information"""
        with get_db() as db:
            disability = db.query(Disability).filter(
                Disability.patient_national_id == national_id
            ).first()
            
            if not disability:
                # Create new record if doesn't exist
                return self.create_disability_record(national_id, update_data)
            
            # Update existing record
            for key, value in update_data.items():
                if hasattr(disability, key):
                    setattr(disability, key, value)
            
            disability.updated_at = datetime.now()
            db.commit()
            db.refresh(disability)
            
            return {'success': True, 'disability': disability, 'message': 'Disability record updated'}
    
    def delete_disability(self, national_id):
        """Delete disability record"""
        with get_db() as db:
            disability = db.query(Disability).filter(
                Disability.patient_national_id == national_id
            ).first()
            
            if disability:
                db.delete(disability)
                db.commit()
                return {'success': True, 'message': 'Disability record deleted'}
            
            return {'success': False, 'message': 'Disability record not found'}
    
    def add_mobility_aid(self, national_id, mobility_aid):
        """Add mobility aid to patient's record"""
        with get_db() as db:
            disability = db.query(Disability).filter(
                Disability.patient_national_id == national_id
            ).first()
            
            if not disability:
                return {'success': False, 'message': 'Disability record not found'}
            
            # Get existing mobility aids
            mobility_aids = disability.mobility_aids or []
            
            if mobility_aid not in mobility_aids:
                mobility_aids.append(mobility_aid)
                disability.mobility_aids = mobility_aids
                db.commit()
                
                return {'success': True, 'message': 'Mobility aid added'}
            
            return {'success': False, 'message': 'Mobility aid already exists'}
    
    def remove_mobility_aid(self, national_id, mobility_aid):
        """Remove mobility aid from patient's record"""
        with get_db() as db:
            disability = db.query(Disability).filter(
                Disability.patient_national_id == national_id
            ).first()
            
            if not disability:
                return {'success': False, 'message': 'Disability record not found'}
            
            mobility_aids = disability.mobility_aids or []
            
            if mobility_aid in mobility_aids:
                mobility_aids.remove(mobility_aid)
                disability.mobility_aids = mobility_aids
                db.commit()
                
                return {'success': True, 'message': 'Mobility aid removed'}
            
            return {'success': False, 'message': 'Mobility aid not found'}
    
    def add_communication_need(self, national_id, need):
        """Add communication need"""
        with get_db() as db:
            disability = db.query(Disability).filter(
                Disability.patient_national_id == national_id
            ).first()
            
            if not disability:
                return {'success': False, 'message': 'Disability record not found'}
            
            needs = disability.communication_needs or []
            
            if need not in needs:
                needs.append(need)
                disability.communication_needs = needs
                db.commit()
                
                return {'success': True, 'message': 'Communication need added'}
            
            return {'success': False, 'message': 'Communication need already exists'}
    
    def add_accessibility_requirement(self, national_id, requirement):
        """Add accessibility requirement"""
        with get_db() as db:
            disability = db.query(Disability).filter(
                Disability.patient_national_id == national_id
            ).first()
            
            if not disability:
                return {'success': False, 'message': 'Disability record not found'}
            
            requirements = disability.accessibility_requirements or []
            
            if requirement not in requirements:
                requirements.append(requirement)
                disability.accessibility_requirements = requirements
                db.commit()
                
                return {'success': True, 'message': 'Accessibility requirement added'}
            
            return {'success': False, 'message': 'Requirement already exists'}
    
    def get_patients_with_disabilities(self):
        """Get all patients with disabilities"""
        with get_db() as db:
            disabilities = db.query(Disability).filter(
                Disability.has_disability == True
            ).all()
            
            return disabilities
    
    def get_patients_by_disability_type(self, disability_type):
        """Get patients by specific disability type"""
        with get_db() as db:
            disabilities = db.query(Disability).filter(
                Disability.has_disability == True,
                Disability.disability_type.like(f"%{disability_type}%")
            ).all()
            
            return disabilities
    
    def get_patients_with_mobility_aids(self):
        """Get patients who use mobility aids"""
        with get_db() as db:
            disabilities = db.query(Disability).filter(
                Disability.has_disability == True,
                Disability.mobility_aids.isnot(None)
            ).all()
            
            return disabilities
    
    def get_disability_statistics(self):
        """Get disability statistics"""
        with get_db() as db:
            total_patients = db.query(Patient).count()
            patients_with_disabilities = db.query(Disability).filter(
                Disability.has_disability == True
            ).count()
            
            hearing_impaired = db.query(Disability).filter(
                Disability.hearing_impairment == True
            ).count()
            
            visual_impaired = db.query(Disability).filter(
                Disability.visual_impairment == True
            ).count()
            
            cognitive_impaired = db.query(Disability).filter(
                Disability.cognitive_impairment == True
            ).count()
            
            return {
                'total_patients': total_patients,
                'patients_with_disabilities': patients_with_disabilities,
                'percentage': (patients_with_disabilities / total_patients * 100) if total_patients > 0 else 0,
                'hearing_impaired': hearing_impaired,
                'visual_impaired': visual_impaired,
                'cognitive_impaired': cognitive_impaired
            }

# Global instance
disability_manager = DisabilityManager()