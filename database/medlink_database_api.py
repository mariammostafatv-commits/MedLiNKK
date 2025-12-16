"""
MedLink Database Usage Examples
How to integrate the database into your MedLink application
"""

from database_manager import DatabaseManager
from colorama import Fore, Style, init
import json

init(autoreset=True)


class MedLinkDatabaseAPI:
    """
    Simple API for MedLink application to interact with database
    Use this in your main application
    """
    
    def __init__(self):
        self.db = DatabaseManager()
    
    # ==================== PATIENT OPERATIONS ====================
    
    def get_patient_by_national_id(self, national_id):
        """
        Get complete patient information
        
        Args:
            national_id (str): Patient's national ID
            
        Returns:
            dict: Patient data or None
        """
        query = "SELECT * FROM patients WHERE national_id = %s"
        results = self.db.execute_query(query, (national_id,), fetch=True)
        
        if results:
            patient = results[0]
            # Convert JSON fields back to Python objects
            patient['emergency_contact'] = json.loads(patient.get('emergency_contact', '{}'))
            patient['chronic_diseases'] = json.loads(patient.get('chronic_diseases', '[]'))
            patient['allergies'] = json.loads(patient.get('allergies', '[]'))
            patient['family_history'] = json.loads(patient.get('family_history', '{}'))
            patient['disabilities_special_needs'] = json.loads(patient.get('disabilities_special_needs', '{}'))
            patient['emergency_directives'] = json.loads(patient.get('emergency_directives', '{}'))
            patient['lifestyle'] = json.loads(patient.get('lifestyle', '{}'))
            patient['insurance'] = json.loads(patient.get('insurance', '{}'))
            return patient
        return None
    
    def search_patients(self, search_term):
        """
        Search patients by name, national ID, or phone
        
        Args:
            search_term (str): Search term
            
        Returns:
            list: Matching patients
        """
        query = """
        SELECT national_id, full_name, date_of_birth, phone, email, blood_type
        FROM patients
        WHERE full_name LIKE %s 
           OR national_id LIKE %s 
           OR phone LIKE %s
        LIMIT 50
        """
        search_pattern = f"%{search_term}%"
        return self.db.execute_query(
            query, 
            (search_pattern, search_pattern, search_pattern), 
            fetch=True
        )
    
    def add_patient(self, patient_data):
        """
        Add new patient
        
        Args:
            patient_data (dict): Patient information
            
        Returns:
            bool: Success status
        """
        # Convert Python objects to JSON
        patient_data['emergency_contact'] = json.dumps(patient_data.get('emergency_contact', {}))
        patient_data['chronic_diseases'] = json.dumps(patient_data.get('chronic_diseases', []))
        patient_data['allergies'] = json.dumps(patient_data.get('allergies', []))
        patient_data['family_history'] = json.dumps(patient_data.get('family_history', {}))
        patient_data['disabilities_special_needs'] = json.dumps(patient_data.get('disabilities_special_needs', {}))
        patient_data['emergency_directives'] = json.dumps(patient_data.get('emergency_directives', {}))
        patient_data['lifestyle'] = json.dumps(patient_data.get('lifestyle', {}))
        patient_data['insurance'] = json.dumps(patient_data.get('insurance', {}))
        patient_data['external_links'] = json.dumps(patient_data.get('external_links', {}))
        
        query = """
        INSERT INTO patients (
            national_id, full_name, date_of_birth, age, gender, blood_type,
            phone, email, address, emergency_contact, chronic_diseases, 
            allergies, family_history, disabilities_special_needs,
            emergency_directives, lifestyle, insurance, external_links
        ) VALUES (
            %(national_id)s, %(full_name)s, %(date_of_birth)s, %(age)s, %(gender)s, %(blood_type)s,
            %(phone)s, %(email)s, %(address)s, %(emergency_contact)s, %(chronic_diseases)s,
            %(allergies)s, %(family_history)s, %(disabilities_special_needs)s,
            %(emergency_directives)s, %(lifestyle)s, %(insurance)s, %(external_links)s
        )
        """
        return self.db.execute_query(query, patient_data)
    
    # ==================== VISIT OPERATIONS ====================
    
    def get_patient_visits(self, national_id, limit=50):
        """
        Get patient's visit history
        
        Args:
            national_id (str): Patient's national ID
            limit (int): Max number of visits
            
        Returns:
            list: Visit records
        """
        query = """
        SELECT * FROM visits 
        WHERE patient_national_id = %s
        ORDER BY visit_date DESC, visit_time DESC
        LIMIT %s
        """
        return self.db.execute_query(query, (national_id, limit), fetch=True)
    
    def add_visit(self, visit_data):
        """
        Add new visit
        
        Args:
            visit_data (dict): Visit information
            
        Returns:
            bool: Success status
        """
        visit_data['attachments'] = json.dumps(visit_data.get('attachments', []))
        
        query = """
        INSERT INTO visits (
            visit_id, patient_national_id, doctor_id, doctor_name,
            visit_date, visit_time, hospital, department, visit_type,
            chief_complaint, diagnosis, treatment_plan, notes, attachments
        ) VALUES (
            %(visit_id)s, %(patient_national_id)s, %(doctor_id)s, %(doctor_name)s,
            %(visit_date)s, %(visit_time)s, %(hospital)s, %(department)s, %(visit_type)s,
            %(chief_complaint)s, %(diagnosis)s, %(treatment_plan)s, %(notes)s, %(attachments)s
        )
        """
        return self.db.execute_query(query, visit_data)
    
    def get_visit_details(self, visit_id):
        """
        Get complete visit details with prescriptions and vital signs
        
        Args:
            visit_id (str): Visit ID
            
        Returns:
            dict: Complete visit information
        """
        # Get visit
        visit_query = "SELECT * FROM visits WHERE visit_id = %s"
        visit = self.db.execute_query(visit_query, (visit_id,), fetch=True)
        
        if not visit:
            return None
        
        visit = visit[0]
        
        # Get prescriptions
        presc_query = "SELECT * FROM prescriptions WHERE visit_id = %s"
        visit['prescriptions'] = self.db.execute_query(presc_query, (visit_id,), fetch=True)
        
        # Get vital signs
        vital_query = "SELECT * FROM vital_signs WHERE visit_id = %s"
        vital_signs = self.db.execute_query(vital_query, (visit_id,), fetch=True)
        visit['vital_signs'] = vital_signs[0] if vital_signs else None
        
        return visit
    
    # ==================== LAB & IMAGING OPERATIONS ====================
    
    def get_patient_lab_results(self, national_id, limit=50):
        """Get patient's lab results"""
        query = """
        SELECT * FROM lab_results 
        WHERE patient_national_id = %s
        ORDER BY test_date DESC
        LIMIT %s
        """
        return self.db.execute_query(query, (national_id, limit), fetch=True)
    
    def get_patient_imaging(self, national_id, limit=50):
        """Get patient's imaging results"""
        query = """
        SELECT * FROM imaging_results 
        WHERE patient_national_id = %s
        ORDER BY imaging_date DESC
        LIMIT %s
        """
        return self.db.execute_query(query, (national_id, limit), fetch=True)
    
    def add_lab_result(self, lab_data):
        """Add new lab result"""
        lab_data['results'] = json.dumps(lab_data.get('results', {}))
        
        query = """
        INSERT INTO lab_results (
            result_id, patient_national_id, ordered_by, test_date,
            lab_name, test_type, status, results, notes, attachment
        ) VALUES (
            %(result_id)s, %(patient_national_id)s, %(ordered_by)s, %(test_date)s,
            %(lab_name)s, %(test_type)s, %(status)s, %(results)s, %(notes)s, %(attachment)s
        )
        """
        return self.db.execute_query(query, lab_data)
    
    def add_imaging_result(self, imaging_data):
        """Add new imaging result"""
        imaging_data['images'] = json.dumps(imaging_data.get('images', []))
        
        query = """
        INSERT INTO imaging_results (
            imaging_id, patient_national_id, ordered_by, imaging_date,
            imaging_center, imaging_type, body_part, findings, 
            radiologist, images
        ) VALUES (
            %(imaging_id)s, %(patient_national_id)s, %(ordered_by)s, %(imaging_date)s,
            %(imaging_center)s, %(imaging_type)s, %(body_part)s, %(findings)s,
            %(radiologist)s, %(images)s
        )
        """
        return self.db.execute_query(query, imaging_data)
    
    # ==================== USER AUTHENTICATION ====================
    
    def authenticate_user(self, username, password_hash):
        """
        Authenticate user (doctor or patient)
        
        Args:
            username (str): Username
            password_hash (str): Hashed password
            
        Returns:
            dict: User data or None
        """
        query = """
        SELECT * FROM users 
        WHERE username = %s AND password_hash = %s AND account_status = 'active'
        """
        results = self.db.execute_query(query, (username, password_hash), fetch=True)
        
        if results:
            # Update last login
            update_query = """
            UPDATE users 
            SET last_login = NOW(), login_count = login_count + 1
            WHERE user_id = %s
            """
            self.db.execute_query(update_query, (results[0]['user_id'],))
            return results[0]
        return None
    
    def get_doctor_by_nfc(self, nfc_card_uid):
        """Get doctor by NFC card"""
        query = """
        SELECT u.* FROM users u
        JOIN doctor_cards dc ON u.user_id = dc.user_id
        WHERE dc.card_uid = %s AND dc.is_active = TRUE
        """
        results = self.db.execute_query(query, (nfc_card_uid,), fetch=True)
        return results[0] if results else None
    
    def get_patient_by_nfc(self, card_uid):
        """Get patient by NFC card"""
        query = """
        SELECT p.* FROM patients p
        WHERE p.nfc_card_uid = %s AND p.nfc_card_status = 'active'
        """
        results = self.db.execute_query(query, (card_uid,), fetch=True)
        
        if results:
            patient = results[0]
            # Parse JSON fields
            patient['emergency_contact'] = json.loads(patient.get('emergency_contact', '{}'))
            patient['chronic_diseases'] = json.loads(patient.get('chronic_diseases', '[]'))
            patient['allergies'] = json.loads(patient.get('allergies', '[]'))
            return patient
        return None
    
    # ==================== MEDICAL HISTORY ====================
    
    def get_complete_medical_history(self, national_id):
        """
        Get complete medical history for a patient
        
        Args:
            national_id (str): Patient's national ID
            
        Returns:
            dict: Complete medical history
        """
        history = {}
        
        # Patient info
        history['patient'] = self.get_patient_by_national_id(national_id)
        
        # Visits
        history['visits'] = self.get_patient_visits(national_id, limit=100)
        
        # Lab results
        history['lab_results'] = self.get_patient_lab_results(national_id)
        
        # Imaging
        history['imaging'] = self.get_patient_imaging(national_id)
        
        # Surgeries
        surgery_query = """
        SELECT * FROM surgeries 
        WHERE patient_national_id = %s 
        ORDER BY surgery_date DESC
        """
        history['surgeries'] = self.db.execute_query(surgery_query, (national_id,), fetch=True)
        
        # Hospitalizations
        hosp_query = """
        SELECT * FROM hospitalizations 
        WHERE patient_national_id = %s 
        ORDER BY admission_date DESC
        """
        history['hospitalizations'] = self.db.execute_query(hosp_query, (national_id,), fetch=True)
        
        # Vaccinations
        vacc_query = """
        SELECT * FROM vaccinations 
        WHERE patient_national_id = %s 
        ORDER BY date_administered DESC
        """
        history['vaccinations'] = self.db.execute_query(vacc_query, (national_id,), fetch=True)
        
        # Current medications
        med_query = """
        SELECT * FROM current_medications 
        WHERE patient_national_id = %s AND is_active = TRUE
        """
        history['current_medications'] = self.db.execute_query(med_query, (national_id,), fetch=True)
        
        return history


# ==================== USAGE EXAMPLES ====================

def example_usage():
    """Examples of how to use the API"""
    
    api = MedLinkDatabaseAPI()
    
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}MedLink Database API - Usage Examples{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    # Example 1: Search for patients
    print(f"{Fore.YELLOW}Example 1: Search Patients{Style.RESET_ALL}")
    patients = api.search_patients("Ahmed")
    if patients:
        print(f"{Fore.GREEN}Found {len(patients)} patients:{Style.RESET_ALL}")
        for p in patients[:3]:  # Show first 3
            print(f"  • {p['full_name']} - {p['national_id']}")
    print()
    
    # Example 2: Get patient details
    print(f"{Fore.YELLOW}Example 2: Get Patient Details{Style.RESET_ALL}")
    if patients:
        patient = api.get_patient_by_national_id(patients[0]['national_id'])
        if patient:
            print(f"{Fore.GREEN}Patient: {patient['full_name']}{Style.RESET_ALL}")
            print(f"  Blood Type: {patient['blood_type']}")
            print(f"  Allergies: {', '.join(patient['allergies']) if patient['allergies'] else 'None'}")
            print(f"  Chronic Diseases: {', '.join(patient['chronic_diseases']) if patient['chronic_diseases'] else 'None'}")
    print()
    
    # Example 3: Get visit history
    print(f"{Fore.YELLOW}Example 3: Get Visit History{Style.RESET_ALL}")
    if patients:
        visits = api.get_patient_visits(patients[0]['national_id'], limit=5)
        if visits:
            print(f"{Fore.GREEN}Found {len(visits)} visits:{Style.RESET_ALL}")
            for v in visits:
                print(f"  • {v['visit_date']} - {v['visit_type']} - Dr. {v['doctor_name']}")
        else:
            print(f"{Fore.YELLOW}  No visits found{Style.RESET_ALL}")
    print()
    
    # Example 4: Get complete medical history
    print(f"{Fore.YELLOW}Example 4: Complete Medical History{Style.RESET_ALL}")
    if patients:
        history = api.get_complete_medical_history(patients[0]['national_id'])
        print(f"{Fore.GREEN}Medical History Summary:{Style.RESET_ALL}")
        print(f"  Visits: {len(history['visits'])}")
        print(f"  Lab Results: {len(history['lab_results'])}")
        print(f"  Imaging: {len(history['imaging'])}")
        print(f"  Surgeries: {len(history['surgeries'])}")
        print(f"  Vaccinations: {len(history['vaccinations'])}")
    print()
    
    print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Examples completed successfully!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    example_usage()
