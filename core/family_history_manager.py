"""
Family History Manager - Manage Patient Family Medical History
MySQL Version - Compatible with existing GUI
"""

from datetime import datetime
from core.database import get_db
from database.models import FamilyHistory, Patient

class FamilyHistoryManager:
    """Manage patient family medical history"""
    
    def __init__(self):
        pass
    
    def add_family_member(self, national_id, family_data):
        """
        Add family member medical history
        
        family_data should contain:
        - relation: str (e.g., 'Father', 'Mother', 'Sibling', 'Grandparent')
        - is_alive: bool
        - age: int (if alive)
        - age_at_death: int (if deceased)
        - cause_of_death: str (if deceased)
        - medical_conditions: list
        - notes: str (optional)
        """
        with get_db() as db:
            # Check if patient exists
            patient = db.query(Patient).filter(
                Patient.national_id == national_id
            ).first()
            
            if not patient:
                return {'success': False, 'message': 'Patient not found'}
            
            family_member = FamilyHistory(
                patient_national_id=national_id,
                **family_data
            )
            db.add(family_member)
            db.commit()
            db.refresh(family_member)
            
            return {'success': True, 'family_member': family_member, 'message': 'Family member added'}
    
    def get_family_history(self, national_id):
        """Get all family history for patient"""
        with get_db() as db:
            return db.query(FamilyHistory).filter(
                FamilyHistory.patient_national_id == national_id
            ).order_by(FamilyHistory.relation).all()
    
    def get_family_member(self, family_id):
        """Get specific family member by ID"""
        with get_db() as db:
            return db.query(FamilyHistory).filter(FamilyHistory.id == family_id).first()
    
    def update_family_member(self, family_id, update_data):
        """Update family member information"""
        with get_db() as db:
            family_member = db.query(FamilyHistory).filter(
                FamilyHistory.id == family_id
            ).first()
            
            if not family_member:
                return {'success': False, 'message': 'Family member not found'}
            
            for key, value in update_data.items():
                if hasattr(family_member, key):
                    setattr(family_member, key, value)
            
            db.commit()
            db.refresh(family_member)
            
            return {'success': True, 'family_member': family_member, 'message': 'Family member updated'}
    
    def delete_family_member(self, family_id):
        """Delete family member record"""
        with get_db() as db:
            family_member = db.query(FamilyHistory).filter(
                FamilyHistory.id == family_id
            ).first()
            
            if family_member:
                db.delete(family_member)
                db.commit()
                return {'success': True, 'message': 'Family member deleted'}
            
            return {'success': False, 'message': 'Family member not found'}
    
    def add_medical_condition(self, family_id, condition):
        """Add medical condition to family member"""
        with get_db() as db:
            family_member = db.query(FamilyHistory).filter(
                FamilyHistory.id == family_id
            ).first()
            
            if not family_member:
                return {'success': False, 'message': 'Family member not found'}
            
            conditions = family_member.medical_conditions or []
            
            if condition not in conditions:
                conditions.append(condition)
                family_member.medical_conditions = conditions
                db.commit()
                
                return {'success': True, 'message': 'Medical condition added'}
            
            return {'success': False, 'message': 'Condition already exists'}
    
    def remove_medical_condition(self, family_id, condition):
        """Remove medical condition from family member"""
        with get_db() as db:
            family_member = db.query(FamilyHistory).filter(
                FamilyHistory.id == family_id
            ).first()
            
            if not family_member:
                return {'success': False, 'message': 'Family member not found'}
            
            conditions = family_member.medical_conditions or []
            
            if condition in conditions:
                conditions.remove(condition)
                family_member.medical_conditions = conditions
                db.commit()
                
                return {'success': True, 'message': 'Medical condition removed'}
            
            return {'success': False, 'message': 'Condition not found'}
    
    def get_family_by_relation(self, national_id, relation):
        """Get family members by relation (e.g., all siblings)"""
        with get_db() as db:
            return db.query(FamilyHistory).filter(
                FamilyHistory.patient_national_id == national_id,
                FamilyHistory.relation == relation
            ).all()
    
    def get_living_family_members(self, national_id):
        """Get all living family members"""
        with get_db() as db:
            return db.query(FamilyHistory).filter(
                FamilyHistory.patient_national_id == national_id,
                FamilyHistory.is_alive == True
            ).all()
    
    def get_deceased_family_members(self, national_id):
        """Get all deceased family members"""
        with get_db() as db:
            return db.query(FamilyHistory).filter(
                FamilyHistory.patient_national_id == national_id,
                FamilyHistory.is_alive == False
            ).all()
    
    def search_by_condition(self, national_id, condition):
        """Search family history for specific medical condition"""
        with get_db() as db:
            family_members = db.query(FamilyHistory).filter(
                FamilyHistory.patient_national_id == national_id
            ).all()
            
            # Filter by condition in medical_conditions JSON
            matching = []
            for member in family_members:
                if member.medical_conditions:
                    if any(condition.lower() in c.lower() for c in member.medical_conditions):
                        matching.append(member)
            
            return matching
    
    def get_genetic_risk_factors(self, national_id):
        """Analyze family history for genetic risk factors"""
        with get_db() as db:
            family_members = db.query(FamilyHistory).filter(
                FamilyHistory.patient_national_id == national_id
            ).all()
            
            # Common genetic conditions to track
            genetic_conditions = [
                'diabetes', 'heart disease', 'cancer', 'hypertension',
                'stroke', 'alzheimer', 'parkinson', 'asthma'
            ]
            
            risk_factors = {}
            
            for condition in genetic_conditions:
                count = 0
                affected_relatives = []
                
                for member in family_members:
                    if member.medical_conditions:
                        for med_cond in member.medical_conditions:
                            if condition.lower() in med_cond.lower():
                                count += 1
                                affected_relatives.append(member.relation)
                
                if count > 0:
                    risk_factors[condition] = {
                        'count': count,
                        'relatives': affected_relatives,
                        'risk_level': 'High' if count >= 2 else 'Moderate'
                    }
            
            return risk_factors
    
    def get_family_summary(self, national_id):
        """Get summary of family medical history"""
        with get_db() as db:
            family_members = db.query(FamilyHistory).filter(
                FamilyHistory.patient_national_id == national_id
            ).all()
            
            # Collect all unique conditions
            all_conditions = set()
            for member in family_members:
                if member.medical_conditions:
                    all_conditions.update(member.medical_conditions)
            
            return {
                'total_members': len(family_members),
                'living_members': len([m for m in family_members if m.is_alive]),
                'deceased_members': len([m for m in family_members if not m.is_alive]),
                'unique_conditions': list(all_conditions),
                'relations': list(set([m.relation for m in family_members]))
            }

# Global instance
family_history_manager = FamilyHistoryManager()