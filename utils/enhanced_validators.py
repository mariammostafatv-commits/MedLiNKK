"""
Enhanced validation utilities for comprehensive patient data
Validates all new medical fields: surgeries, hospitalizations, vaccinations, 
family history, disabilities, emergency directives, and lifestyle
"""
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional


def validate_surgery_data(surgery: Dict) -> Tuple[bool, str]:
    """
    Validate surgery record
    
    Args:
        surgery: Surgery information dictionary
    
    Returns:
        (is_valid: bool, message: str)
    """
    required_fields = ['date', 'procedure', 'hospital', 'surgeon']
    
    for field in required_fields:
        if field not in surgery or not surgery[field]:
            return False, f"Missing required field: {field}"
    
    # Validate date format
    try:
        datetime.strptime(surgery['date'], "%Y-%m-%d")
    except ValueError:
        return False, "Invalid date format (must be YYYY-MM-DD)"
    
    # Validate date is not in future
    if datetime.strptime(surgery['date'], "%Y-%m-%d") > datetime.now():
        return False, "Surgery date cannot be in the future"
    
    return True, "Valid"


def validate_hospitalization_data(hospitalization: Dict) -> Tuple[bool, str]:
    """
    Validate hospitalization record
    
    Args:
        hospitalization: Hospitalization information dictionary
    
    Returns:
        (is_valid: bool, message: str)
    """
    required_fields = ['admission_date', 'discharge_date', 'reason', 'hospital']
    
    for field in required_fields:
        if field not in hospitalization or not hospitalization[field]:
            return False, f"Missing required field: {field}"
    
    # Validate date formats
    try:
        admission = datetime.strptime(hospitalization['admission_date'], "%Y-%m-%d")
        discharge = datetime.strptime(hospitalization['discharge_date'], "%Y-%m-%d")
    except ValueError:
        return False, "Invalid date format (must be YYYY-MM-DD)"
    
    # Discharge must be after admission
    if discharge < admission:
        return False, "Discharge date must be after admission date"
    
    # Dates cannot be in future
    if admission > datetime.now() or discharge > datetime.now():
        return False, "Dates cannot be in the future"
    
    return True, "Valid"


def validate_vaccination_data(vaccination: Dict) -> Tuple[bool, str]:
    """
    Validate vaccination record
    
    Args:
        vaccination: Vaccination information dictionary
    
    Returns:
        (is_valid: bool, message: str)
    """
    required_fields = ['vaccine_name', 'date_administered', 'location']
    
    for field in required_fields:
        if field not in vaccination or not vaccination[field]:
            return False, f"Missing required field: {field}"
    
    # Validate date format
    try:
        vax_date = datetime.strptime(vaccination['date_administered'], "%Y-%m-%d")
    except ValueError:
        return False, "Invalid date format (must be YYYY-MM-DD)"
    
    # Date cannot be in future
    if vax_date > datetime.now():
        return False, "Vaccination date cannot be in the future"
    
    # Validate next dose date if provided
    if vaccination.get('next_dose_due'):
        try:
            next_dose = datetime.strptime(vaccination['next_dose_due'], "%Y-%m-%d")
            if next_dose < vax_date:
                return False, "Next dose date must be after administration date"
        except ValueError:
            return False, "Invalid next dose date format"
    
    return True, "Valid"


def validate_family_history(family_history: Dict) -> Tuple[bool, str]:
    """
    Validate family medical history
    
    Args:
        family_history: Family history dictionary
    
    Returns:
        (is_valid: bool, message: str)
    """
    # Validate father info
    if 'father' in family_history:
        father = family_history['father']
        if not isinstance(father.get('alive'), bool):
            return False, "Father alive status must be boolean"
        
        if not father['alive']:
            if 'age_at_death' not in father or not isinstance(father['age_at_death'], int):
                return False, "Age at death required for deceased father"
            if father['age_at_death'] < 0 or father['age_at_death'] > 120:
                return False, "Invalid age at death for father"
    
    # Validate mother info
    if 'mother' in family_history:
        mother = family_history['mother']
        if not isinstance(mother.get('alive'), bool):
            return False, "Mother alive status must be boolean"
        
        if not mother['alive']:
            if 'age_at_death' not in mother or not isinstance(mother['age_at_death'], int):
                return False, "Age at death required for deceased mother"
            if mother['age_at_death'] < 0 or mother['age_at_death'] > 120:
                return False, "Invalid age at death for mother"
    
    # Validate siblings
    if 'siblings' in family_history:
        if not isinstance(family_history['siblings'], list):
            return False, "Siblings must be a list"
        
        for sibling in family_history['siblings']:
            if 'age' in sibling:
                if sibling['age'] < 0 or sibling['age'] > 120:
                    return False, "Invalid sibling age"
    
    return True, "Valid"


def validate_disability_data(disabilities: Dict) -> Tuple[bool, str]:
    """
    Validate disability/special needs information
    
    Args:
        disabilities: Disability information dictionary
    
    Returns:
        (is_valid: bool, message: str)
    """
    if 'has_disability' not in disabilities:
        return False, "Missing has_disability field"
    
    if not isinstance(disabilities['has_disability'], bool):
        return False, "has_disability must be boolean"
    
    # If has disability, require disability type
    if disabilities['has_disability'] and not disabilities.get('disability_type'):
        return False, "Disability type required when has_disability is True"
    
    # Validate boolean fields
    boolean_fields = ['hearing_impairment', 'visual_impairment', 'cognitive_impairment']
    for field in boolean_fields:
        if field in disabilities and not isinstance(disabilities[field], bool):
            return False, f"{field} must be boolean"
    
    # Validate list fields
    list_fields = ['mobility_aids', 'communication_needs', 'accessibility_requirements']
    for field in list_fields:
        if field in disabilities and not isinstance(disabilities[field], list):
            return False, f"{field} must be a list"
    
    return True, "Valid"


def validate_emergency_directives(directives: Dict) -> Tuple[bool, str]:
    """
    Validate emergency directives
    
    Args:
        directives: Emergency directives dictionary
    
    Returns:
        (is_valid: bool, message: str)
    """
    # Validate DNR status
    if 'dnr_status' not in directives:
        return False, "Missing DNR status"
    
    if not isinstance(directives['dnr_status'], bool):
        return False, "DNR status must be boolean"
    
    # If DNR is true, date should be provided
    if directives['dnr_status'] and not directives.get('dnr_date'):
        return False, "DNR date required when DNR status is True"
    
    # Validate DNR date if provided
    if directives.get('dnr_date'):
        try:
            dnr_date = datetime.strptime(directives['dnr_date'], "%Y-%m-%d")
            if dnr_date > datetime.now():
                return False, "DNR date cannot be in the future"
        except ValueError:
            return False, "Invalid DNR date format"
    
    # Validate organ donor
    if 'organ_donor' not in directives:
        return False, "Missing organ donor status"
    
    if not isinstance(directives['organ_donor'], bool):
        return False, "Organ donor status must be boolean"
    
    # Validate boolean fields
    boolean_fields = ['living_will', 'blood_transfusion_consent', 'tissue_donation']
    for field in boolean_fields:
        if field in directives and not isinstance(directives[field], bool):
            return False, f"{field} must be boolean"
    
    # Validate power of attorney
    if 'power_of_attorney' in directives:
        poa = directives['power_of_attorney']
        if not isinstance(poa.get('has_poa'), bool):
            return False, "Power of attorney has_poa must be boolean"
        
        if poa.get('has_poa'):
            required_poa_fields = ['name', 'relation', 'phone']
            for field in required_poa_fields:
                if not poa.get(field):
                    return False, f"Missing power of attorney field: {field}"
    
    return True, "Valid"


def validate_lifestyle_data(lifestyle: Dict) -> Tuple[bool, str]:
    """
    Validate lifestyle information
    
    Args:
        lifestyle: Lifestyle information dictionary
    
    Returns:
        (is_valid: bool, message: str)
    """
    # Validate smoking status
    if 'smoking_status' in lifestyle:
        valid_smoking_statuses = ['Never', 'Former', 'Current', 'Occasional']
        if lifestyle['smoking_status'] not in valid_smoking_statuses:
            return False, f"Invalid smoking status. Must be one of: {', '.join(valid_smoking_statuses)}"
    
    # Validate alcohol consumption
    if 'alcohol_consumption' in lifestyle:
        valid_alcohol = ['None', 'Occasional', 'Moderate', 'Heavy']
        if lifestyle['alcohol_consumption'] not in valid_alcohol:
            return False, f"Invalid alcohol consumption. Must be one of: {', '.join(valid_alcohol)}"
    
    # Validate sleep hours
    if 'sleep_hours' in lifestyle:
        if not isinstance(lifestyle['sleep_hours'], (int, float)):
            return False, "Sleep hours must be a number"
        if lifestyle['sleep_hours'] < 0 or lifestyle['sleep_hours'] > 24:
            return False, "Sleep hours must be between 0 and 24"
    
    # Validate stress level
    if 'stress_level' in lifestyle:
        valid_stress = ['Low', 'Moderate', 'Moderate to High', 'High', 'Very High']
        if lifestyle['stress_level'] not in valid_stress:
            return False, f"Invalid stress level. Must be one of: {', '.join(valid_stress)}"
    
    # Validate dietary restrictions is a list
    if 'dietary_restrictions' in lifestyle:
        if not isinstance(lifestyle['dietary_restrictions'], list):
            return False, "Dietary restrictions must be a list"
    
    return True, "Valid"


def validate_comprehensive_patient_data(patient_data: Dict) -> Tuple[bool, List[str]]:
    """
    Validate complete patient data including all new fields
    
    Args:
        patient_data: Complete patient dictionary
    
    Returns:
        (is_valid: bool, error_messages: List[str])
    """
    errors = []
    
    # Validate surgeries
    if 'surgeries' in patient_data:
        for i, surgery in enumerate(patient_data['surgeries'], 1):
            valid, msg = validate_surgery_data(surgery)
            if not valid:
                errors.append(f"Surgery {i}: {msg}")
    
    # Validate hospitalizations
    if 'hospitalizations' in patient_data:
        for i, hosp in enumerate(patient_data['hospitalizations'], 1):
            valid, msg = validate_hospitalization_data(hosp)
            if not valid:
                errors.append(f"Hospitalization {i}: {msg}")
    
    # Validate vaccinations
    if 'vaccinations' in patient_data:
        for i, vax in enumerate(patient_data['vaccinations'], 1):
            valid, msg = validate_vaccination_data(vax)
            if not valid:
                errors.append(f"Vaccination {i}: {msg}")
    
    # Validate family history
    if 'family_history' in patient_data:
        valid, msg = validate_family_history(patient_data['family_history'])
        if not valid:
            errors.append(f"Family history: {msg}")
    
    # Validate disabilities
    if 'disabilities_special_needs' in patient_data:
        valid, msg = validate_disability_data(patient_data['disabilities_special_needs'])
        if not valid:
            errors.append(f"Disabilities: {msg}")
    
    # Validate emergency directives
    if 'emergency_directives' in patient_data:
        valid, msg = validate_emergency_directives(patient_data['emergency_directives'])
        if not valid:
            errors.append(f"Emergency directives: {msg}")
    
    # Validate lifestyle
    if 'lifestyle' in patient_data:
        valid, msg = validate_lifestyle_data(patient_data['lifestyle'])
        if not valid:
            errors.append(f"Lifestyle: {msg}")
    
    return (len(errors) == 0, errors)


# Utility functions for common validations
def is_valid_date(date_str: str) -> bool:
    """Check if date string is valid YYYY-MM-DD format"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_past_date(date_str: str) -> bool:
    """Check if date is in the past"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date <= datetime.now()
    except ValueError:
        return False


def validate_date_range(start_date: str, end_date: str) -> bool:
    """Validate that end_date is after start_date"""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return end >= start
    except ValueError:
        return False
