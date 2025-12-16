"""
JSON Data Importer for MedLink
Import existing JSON data files into MySQL database
"""

import json
import mysql.connector
from mysql.connector import Error
from pathlib import Path
from colorama import Fore, Style, init
from datetime import datetime
import sys

sys.path.append(str(Path(__file__).parent.parent))

from config.database_config import DATABASE_CONFIG

init(autoreset=True)


class JSONDataImporter:
    """Import JSON data files into database"""
    
    def __init__(self, data_folder="data"):
        """
        Initialize importer
        
        Args:
            data_folder (str): Path to folder containing JSON files
        """
        self.data_folder = Path(data_folder)
        self.connection = None
        self.cursor = None
        self.stats = {
            'users': 0,
            'patients': 0,
            'surgeries': 0,
            'hospitalizations': 0,
            'vaccinations': 0,
            'current_medications': 0,
            'visits': 0,
            'prescriptions': 0,
            'vital_signs': 0,
            'lab_results': 0,
            'imaging_results': 0,
            'doctor_cards': 0,
            'patient_cards': 0,
            'hardware_events': 0
        }
    
    def connect(self):
        """Connect to database"""
        try:
            self.connection = mysql.connector.connect(**DATABASE_CONFIG)
            self.cursor = self.connection.cursor(dictionary=True)
            return True
        except Error as e:
            print(f"{Fore.RED}❌ Connection Error: {e}{Style.RESET_ALL}")
            return False
    
    def disconnect(self):
        """Disconnect from database"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def load_json_file(self, filename):
        """Load JSON file"""
        filepath = self.data_folder / filename
        if not filepath.exists():
            print(f"{Fore.YELLOW}⚠️  File not found: {filepath}{Style.RESET_ALL}")
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"{Fore.RED}❌ Error loading {filename}: {e}{Style.RESET_ALL}")
            return None
    
    def import_users(self):
        """Import users from users.json"""
        print(f"\n{Fore.CYAN}📥 Importing Users...{Style.RESET_ALL}")
        
        data = self.load_json_file('users.json')
        if not data or 'users' not in data:
            return False
        
        try:
            query = """
            INSERT INTO users (
                user_id, username, password_hash, role, full_name, email, phone,
                specialization, hospital, license_number, years_experience,
                fingerprint_id, fingerprint_enrolled, fingerprint_enrollment_date,
                nfc_card_uid, biometric_enabled, last_fingerprint_login, fingerprint_login_count,
                national_id, date_of_birth, created_at, last_login, login_count, account_status
            ) VALUES (
                %(user_id)s, %(username)s, %(password_hash)s, %(role)s, %(full_name)s, %(email)s, %(phone)s,
                %(specialization)s, %(hospital)s, %(license_number)s, %(years_experience)s,
                %(fingerprint_id)s, %(fingerprint_enrolled)s, %(fingerprint_enrollment_date)s,
                %(nfc_card_uid)s, %(biometric_enabled)s, %(last_fingerprint_login)s, %(fingerprint_login_count)s,
                %(national_id)s, %(date_of_birth)s, %(created_at)s, %(last_login)s, %(login_count)s, %(account_status)s
            )
            """
            
            for user in data['users']:
                try:
                    self.cursor.execute(query, user)
                    self.stats['users'] += 1
                except Error as e:
                    if "Duplicate entry" not in str(e):
                        print(f"{Fore.YELLOW}⚠️  Error importing user {user.get('username')}: {e}{Style.RESET_ALL}")
            
            self.connection.commit()
            print(f"{Fore.GREEN}✅ Imported {self.stats['users']} users{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error importing users: {e}{Style.RESET_ALL}")
            return False
    
    def import_patients(self):
        """Import patients from patients.json"""
        print(f"\n{Fore.CYAN}📥 Importing Patients...{Style.RESET_ALL}")
        
        data = self.load_json_file('patients.json')
        if not data or 'patients' not in data:
            return False
        
        try:
            # Main patient data
            patient_query = """
            INSERT INTO patients (
                national_id, full_name, date_of_birth, age, gender, blood_type,
                phone, email, address, city, governorate,
                emergency_contact, chronic_diseases, allergies,
                family_history, disabilities_special_needs, emergency_directives,
                lifestyle, insurance, external_links,
                nfc_card_uid, nfc_card_assigned, nfc_card_assignment_date,
                nfc_card_type, nfc_card_status, nfc_card_last_scan, nfc_scan_count,
                created_at, last_updated
            ) VALUES (
                %(national_id)s, %(full_name)s, %(date_of_birth)s, %(age)s, %(gender)s, %(blood_type)s,
                %(phone)s, %(email)s, %(address)s, %(city)s, %(governorate)s,
                %(emergency_contact)s, %(chronic_diseases)s, %(allergies)s,
                %(family_history)s, %(disabilities_special_needs)s, %(emergency_directives)s,
                %(lifestyle)s, %(insurance)s, %(external_links)s,
                %(nfc_card_uid)s, %(nfc_card_assigned)s, %(nfc_card_assignment_date)s,
                %(nfc_card_type)s, %(nfc_card_status)s, %(nfc_card_last_scan)s, %(nfc_scan_count)s,
                %(created_at)s, %(last_updated)s
            )
            """
            
            for patient in data['patients']:
                try:
                    # Convert nested objects to JSON
                    patient_data = patient.copy()
                    patient_data['emergency_contact'] = json.dumps(patient.get('emergency_contact', {}))
                    patient_data['chronic_diseases'] = json.dumps(patient.get('chronic_diseases', []))
                    patient_data['allergies'] = json.dumps(patient.get('allergies', []))
                    patient_data['family_history'] = json.dumps(patient.get('family_history', {}))
                    patient_data['disabilities_special_needs'] = json.dumps(patient.get('disabilities_special_needs', {}))
                    patient_data['emergency_directives'] = json.dumps(patient.get('emergency_directives', {}))
                    patient_data['lifestyle'] = json.dumps(patient.get('lifestyle', {}))
                    patient_data['insurance'] = json.dumps(patient.get('insurance', {}))
                    patient_data['external_links'] = json.dumps(patient.get('external_links', {}))
                    
                    self.cursor.execute(patient_query, patient_data)
                    self.stats['patients'] += 1
                    
                    # Import surgeries
                    if 'surgeries' in patient and patient['surgeries']:
                        self.import_surgeries(patient['national_id'], patient['surgeries'])
                    
                    # Import hospitalizations
                    if 'hospitalizations' in patient and patient['hospitalizations']:
                        self.import_hospitalizations(patient['national_id'], patient['hospitalizations'])
                    
                    # Import vaccinations
                    if 'vaccinations' in patient and patient['vaccinations']:
                        self.import_vaccinations(patient['national_id'], patient['vaccinations'])
                    
                    # Import current medications
                    if 'current_medications' in patient and patient['current_medications']:
                        self.import_current_medications(patient['national_id'], patient['current_medications'])
                    
                except Error as e:
                    if "Duplicate entry" not in str(e):
                        print(f"{Fore.YELLOW}⚠️  Error importing patient {patient.get('national_id')}: {e}{Style.RESET_ALL}")
            
            self.connection.commit()
            print(f"{Fore.GREEN}✅ Imported {self.stats['patients']} patients{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error importing patients: {e}{Style.RESET_ALL}")
            return False
    
    def import_surgeries(self, patient_national_id, surgeries):
        """Import surgeries for a patient"""
        query = """
        INSERT INTO surgeries (
            surgery_id, patient_national_id, surgery_type, surgery_date,
            surgeon, hospital, reason, outcome, complications, notes
        ) VALUES (
            %(surgery_id)s, %(patient_national_id)s, %(surgery_type)s, %(surgery_date)s,
            %(surgeon)s, %(hospital)s, %(reason)s, %(outcome)s, %(complications)s, %(notes)s
        )
        """
        
        for surgery in surgeries:
            try:
                surgery['patient_national_id'] = patient_national_id
                self.cursor.execute(query, surgery)
                self.stats['surgeries'] += 1
            except Error as e:
                if "Duplicate entry" not in str(e):
                    print(f"{Fore.YELLOW}⚠️  Error importing surgery: {e}{Style.RESET_ALL}")
    
    def import_hospitalizations(self, patient_national_id, hospitalizations):
        """Import hospitalizations for a patient"""
        query = """
        INSERT INTO hospitalizations (
            hospitalization_id, patient_national_id, hospital, admission_date,
            discharge_date, reason, diagnosis, treatment, length_of_stay, notes
        ) VALUES (
            %(hospitalization_id)s, %(patient_national_id)s, %(hospital)s, %(admission_date)s,
            %(discharge_date)s, %(reason)s, %(diagnosis)s, %(treatment)s, %(length_of_stay)s, %(notes)s
        )
        """
        
        for hosp in hospitalizations:
            try:
                hosp['patient_national_id'] = patient_national_id
                self.cursor.execute(query, hosp)
                self.stats['hospitalizations'] += 1
            except Error as e:
                if "Duplicate entry" not in str(e):
                    print(f"{Fore.YELLOW}⚠️  Error importing hospitalization: {e}{Style.RESET_ALL}")
    
    def import_vaccinations(self, patient_national_id, vaccinations):
        """Import vaccinations for a patient"""
        query = """
        INSERT INTO vaccinations (
            patient_national_id, vaccine_name, date_administered,
            dose_number, location, batch_number, next_dose_due
        ) VALUES (
            %(patient_national_id)s, %(vaccine_name)s, %(date_administered)s,
            %(dose_number)s, %(location)s, %(batch_number)s, %(next_dose_due)s
        )
        """
        
        for vacc in vaccinations:
            try:
                vacc['patient_national_id'] = patient_national_id
                self.cursor.execute(query, vacc)
                self.stats['vaccinations'] += 1
            except Error as e:
                print(f"{Fore.YELLOW}⚠️  Error importing vaccination: {e}{Style.RESET_ALL}")
    
    def import_current_medications(self, patient_national_id, medications):
        """Import current medications for a patient"""
        query = """
        INSERT INTO current_medications (
            patient_national_id, medication_name, dosage, frequency, started_date
        ) VALUES (
            %(patient_national_id)s, %(name)s, %(dosage)s, %(frequency)s, %(started_date)s
        )
        """
        
        for med in medications:
            try:
                med['patient_national_id'] = patient_national_id
                self.cursor.execute(query, med)
                self.stats['current_medications'] += 1
            except Error as e:
                print(f"{Fore.YELLOW}⚠️  Error importing medication: {e}{Style.RESET_ALL}")
    
    def import_visits(self):
        """Import visits from visits.json"""
        print(f"\n{Fore.CYAN}📥 Importing Visits...{Style.RESET_ALL}")
        
        data = self.load_json_file('visits.json')
        if not data or 'visits' not in data:
            return False
        
        try:
            visit_query = """
            INSERT INTO visits (
                visit_id, patient_national_id, doctor_id, doctor_name,
                visit_date, visit_time, hospital, department, visit_type,
                chief_complaint, diagnosis, treatment_plan, notes, attachments, created_at
            ) VALUES (
                %(visit_id)s, %(patient_national_id)s, %(doctor_id)s, %(doctor_name)s,
                %(date)s, %(time)s, %(hospital)s, %(department)s, %(visit_type)s,
                %(chief_complaint)s, %(diagnosis)s, %(treatment_plan)s, %(notes)s, %(attachments)s, %(created_at)s
            )
            """
            
            for visit in data['visits']:
                try:
                    # Convert attachments to JSON
                    visit['attachments'] = json.dumps(visit.get('attachments', []))
                    
                    self.cursor.execute(visit_query, visit)
                    self.stats['visits'] += 1
                    
                    # Import prescriptions
                    if 'prescriptions' in visit and visit['prescriptions']:
                        self.import_prescriptions(visit['visit_id'], visit['prescriptions'])
                    
                    # Import vital signs
                    if 'vital_signs' in visit and visit['vital_signs']:
                        self.import_vital_signs(visit['visit_id'], visit['vital_signs'])
                    
                except Error as e:
                    if "Duplicate entry" not in str(e):
                        print(f"{Fore.YELLOW}⚠️  Error importing visit {visit.get('visit_id')}: {e}{Style.RESET_ALL}")
            
            self.connection.commit()
            print(f"{Fore.GREEN}✅ Imported {self.stats['visits']} visits{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error importing visits: {e}{Style.RESET_ALL}")
            return False
    
    def import_prescriptions(self, visit_id, prescriptions):
        """Import prescriptions for a visit"""
        query = """
        INSERT INTO prescriptions (
            visit_id, medication, dosage, frequency, duration, instructions
        ) VALUES (
            %(visit_id)s, %(medication)s, %(dosage)s, %(frequency)s, %(duration)s, %(instructions)s
        )
        """
        
        for presc in prescriptions:
            try:
                presc['visit_id'] = visit_id
                presc['instructions'] = presc.get('instructions', '')
                self.cursor.execute(query, presc)
                self.stats['prescriptions'] += 1
            except Error as e:
                print(f"{Fore.YELLOW}⚠️  Error importing prescription: {e}{Style.RESET_ALL}")
    
    def import_vital_signs(self, visit_id, vital_signs):
        """Import vital signs for a visit"""
        query = """
        INSERT INTO vital_signs (
            visit_id, blood_pressure, heart_rate, temperature, weight, height
        ) VALUES (
            %(visit_id)s, %(blood_pressure)s, %(heart_rate)s, %(temperature)s, %(weight)s, %(height)s
        )
        """
        
        try:
            vital_signs['visit_id'] = visit_id
            vital_signs['height'] = vital_signs.get('height', None)
            self.cursor.execute(query, vital_signs)
            self.stats['vital_signs'] += 1
        except Error as e:
            print(f"{Fore.YELLOW}⚠️  Error importing vital signs: {e}{Style.RESET_ALL}")
    
    def import_lab_results(self):
        """Import lab results from lab_results.json"""
        print(f"\n{Fore.CYAN}📥 Importing Lab Results...{Style.RESET_ALL}")
        
        data = self.load_json_file('lab_results.json')
        if not data or 'lab_results' not in data:
            return False
        
        try:
            query = """
            INSERT INTO lab_results (
                result_id, patient_national_id, ordered_by, test_date,
                lab_name, test_type, status, results, notes, attachment, created_at
            ) VALUES (
                %(result_id)s, %(patient_national_id)s, %(ordered_by)s, %(date)s,
                %(lab_name)s, %(test_type)s, %(status)s, %(results)s, %(notes)s, %(attachment)s, %(created_at)s
            )
            """
            
            for result in data['lab_results']:
                try:
                    # Convert results to JSON
                    result['results'] = json.dumps(result.get('results', {}))
                    self.cursor.execute(query, result)
                    self.stats['lab_results'] += 1
                except Error as e:
                    if "Duplicate entry" not in str(e):
                        print(f"{Fore.YELLOW}⚠️  Error importing lab result: {e}{Style.RESET_ALL}")
            
            self.connection.commit()
            print(f"{Fore.GREEN}✅ Imported {self.stats['lab_results']} lab results{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error importing lab results: {e}{Style.RESET_ALL}")
            return False
    
    def import_imaging_results(self):
        """Import imaging results from imaging_results.json"""
        print(f"\n{Fore.CYAN}📥 Importing Imaging Results...{Style.RESET_ALL}")
        
        data = self.load_json_file('imaging_results.json')
        if not data or 'imaging_results' not in data:
            return False
        
        try:
            query = """
            INSERT INTO imaging_results (
                imaging_id, patient_national_id, ordered_by, imaging_date,
                imaging_center, imaging_type, body_part, findings, radiologist,
                images, created_at
            ) VALUES (
                %(imaging_id)s, %(patient_national_id)s, %(ordered_by)s, %(date)s,
                %(imaging_center)s, %(imaging_type)s, %(body_part)s, %(findings)s, %(radiologist)s,
                %(images)s, %(created_at)s
            )
            """
            
            for result in data['imaging_results']:
                try:
                    # Convert images to JSON
                    result['images'] = json.dumps(result.get('images', []))
                    self.cursor.execute(query, result)
                    self.stats['imaging_results'] += 1
                except Error as e:
                    if "Duplicate entry" not in str(e):
                        print(f"{Fore.YELLOW}⚠️  Error importing imaging result: {e}{Style.RESET_ALL}")
            
            self.connection.commit()
            print(f"{Fore.GREEN}✅ Imported {self.stats['imaging_results']} imaging results{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error importing imaging results: {e}{Style.RESET_ALL}")
            return False
    
    def import_cards(self):
        """Import NFC cards from cards.json"""
        print(f"\n{Fore.CYAN}📥 Importing NFC Cards...{Style.RESET_ALL}")
        
        data = self.load_json_file('cards.json')
        if not data:
            return False
        
        try:
            # Import doctor cards
            if 'doctor_cards' in data:
                doctor_query = """
                INSERT INTO doctor_cards (
                    card_uid, username, full_name, card_type
                ) VALUES (
                    %(card_uid)s, %(username)s, %(name)s, %(type)s
                )
                """
                
                for card_uid, card_data in data['doctor_cards'].items():
                    try:
                        card_data['card_uid'] = card_uid
                        self.cursor.execute(doctor_query, card_data)
                        self.stats['doctor_cards'] += 1
                    except Error as e:
                        if "Duplicate entry" not in str(e):
                            print(f"{Fore.YELLOW}⚠️  Error importing doctor card: {e}{Style.RESET_ALL}")
            
            # Import patient cards
            if 'patient_cards' in data:
                patient_query = """
                INSERT INTO patient_cards (
                    card_uid, national_id, full_name, card_type
                ) VALUES (
                    %(card_uid)s, %(national_id)s, %(name)s, %(type)s
                )
                """
                
                for card_uid, card_data in data['patient_cards'].items():
                    try:
                        card_data['card_uid'] = card_uid
                        self.cursor.execute(patient_query, card_data)
                        self.stats['patient_cards'] += 1
                    except Error as e:
                        if "Duplicate entry" not in str(e):
                            print(f"{Fore.YELLOW}⚠️  Error importing patient card: {e}{Style.RESET_ALL}")
            
            self.connection.commit()
            print(f"{Fore.GREEN}✅ Imported {self.stats['doctor_cards']} doctor cards, {self.stats['patient_cards']} patient cards{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error importing cards: {e}{Style.RESET_ALL}")
            return False
    
    def import_hardware_audit_log(self):
        """Import hardware audit log from hardware_audit_log.json"""
        print(f"\n{Fore.CYAN}📥 Importing Hardware Audit Log...{Style.RESET_ALL}")
        
        data = self.load_json_file('hardware_audit_log.json')
        if not data or 'hardware_events' not in data:
            return False
        
        try:
            query = """
            INSERT INTO hardware_audit_log (
                event_id, timestamp, event_type, user_id, patient_national_id,
                card_uid, fingerprint_id, success, accessed_by, access_type,
                ip_address, device_name
            ) VALUES (
                %(event_id)s, %(timestamp)s, %(event_type)s, %(user_id)s, %(patient_national_id)s,
                %(card_uid)s, %(fingerprint_id)s, %(success)s, %(accessed_by)s, %(access_type)s,
                %(ip_address)s, %(device_name)s
            )
            """
            
            for event in data['hardware_events']:
                try:
                    # Fill optional fields with None
                    event.setdefault('user_id', None)
                    event.setdefault('patient_national_id', None)
                    event.setdefault('card_uid', None)
                    event.setdefault('fingerprint_id', None)
                    event.setdefault('accessed_by', None)
                    event.setdefault('access_type', None)
                    event.setdefault('ip_address', None)
                    event.setdefault('device_name', None)
                    
                    self.cursor.execute(query, event)
                    self.stats['hardware_events'] += 1
                except Error as e:
                    if "Duplicate entry" not in str(e):
                        print(f"{Fore.YELLOW}⚠️  Error importing hardware event: {e}{Style.RESET_ALL}")
            
            self.connection.commit()
            print(f"{Fore.GREEN}✅ Imported {self.stats['hardware_events']} hardware events{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error importing hardware audit log: {e}{Style.RESET_ALL}")
            return False
    
    def import_all(self):
        """Import all data from JSON files"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📦 MedLink JSON Data Import{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        if not self.connect():
            return False
        
        # Import in correct order (respecting foreign keys)
        self.import_users()
        self.import_patients()
        self.import_visits()
        self.import_lab_results()
        self.import_imaging_results()
        self.import_cards()
        self.import_hardware_audit_log()
        
        self.disconnect()
        
        # Print summary
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Import Complete!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}📊 Import Summary:{Style.RESET_ALL}\n")
        for key, value in self.stats.items():
            if value > 0:
                print(f"{Fore.WHITE}  • {key.replace('_', ' ').title():.<30} {value:>6,}{Style.RESET_ALL}")
        
        total = sum(self.stats.values())
        print(f"\n{Fore.GREEN}  Total Records Imported: {total:,}{Style.RESET_ALL}\n")
        
        return True


def main():
    """CLI interface"""
    importer = JSONDataImporter()
    importer.import_all()


if __name__ == "__main__":
    main()
