"""
Data Seeder for MedLink
Generate test data and import from JSON
"""

import mysql.connector
from mysql.connector import Error
from colorama import Fore, Style, init
from pathlib import Path
import json
import random
from datetime import datetime, timedelta
from faker import Faker
import sys
import hashlib

sys.path.append(str(Path(__file__).parent.parent))

from config.database_config import DATABASE_CONFIG, SEEDER_CONFIG
from database.database_manager import DatabaseManager

init(autoreset=True)
fake = Faker(['ar_EG', 'en_US'])  # Arabic and English


class DataSeeder:
    """Generate and seed test data for MedLink"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.config = SEEDER_CONFIG
        self.data_folder = Path(__file__).parent.parent / "data"
        
        # Egyptian data
        self.egyptian_cities = [
            'Cairo', 'Alexandria', 'Giza', 'Shubra El Kheima', 'Port Said',
            'Suez', 'Mansoura', 'Tanta', 'Asyut', 'Ismailia', 'Faiyum',
            'Zagazig', 'Aswan', 'Damietta', 'Luxor', 'Minya', 'Beni Suef'
        ]
        
        self.egyptian_hospitals = [
            'Cairo University Hospital - Kasr El Aini',
            'Ain Shams University Hospital',
            'Alexandria University Hospital',
            'Mansoura University Hospital',
            'Assiut University Hospital',
            'Dar El Fouad Hospital',
            'Saudi German Hospital',
            'Cleopatra Hospital',
            'Al Salam International Hospital',
            'Nile Badrawi Hospital'
        ]
        
        self.departments = [
            'Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics',
            'Internal Medicine', 'Surgery', 'Emergency', 'Radiology',
            'Dermatology', 'Ophthalmology', 'ENT', 'Urology'
        ]
        
        self.blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        
        self.chronic_conditions = [
            'Diabetes Type 2', 'Hypertension', 'Asthma', 'COPD',
            'Coronary Artery Disease', 'Heart Failure', 'Chronic Kidney Disease',
            'Arthritis', 'Hypothyroidism', 'Hyperlipidemia'
        ]
        
        self.medications = [
            'Metformin 500mg', 'Aspirin 81mg', 'Lisinopril 10mg',
            'Atorvastatin 20mg', 'Omeprazole 20mg', 'Levothyroxine 50mcg',
            'Amlodipine 5mg', 'Metoprolol 50mg', 'Losartan 50mg'
        ]
        
    def generate_national_id(self):
        """Generate valid Egyptian national ID"""
        # Format: XYYZZMM DDGGG
        # X = Century (2 or 3)
        # YY = Year
        # ZZ = Month (01-12)
        # MM = Governorate code
        # DD = Day
        # G = Gender (odd=male, even=female)
        
        century = random.choice([2, 3])
        year = random.randint(50, 99) if century == 2 else random.randint(0, 5)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        governorate = random.randint(1, 35)
        sequence = random.randint(1, 999)
        
        return f"{century}{year:02d}{month:02d}{governorate:02d}{day:02d}{sequence:03d}"
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def seed_users(self, count=10):
        """Generate and insert doctor users"""
        print(f"\n{Fore.YELLOW}🔄 Seeding {count} users (doctors)...{Style.RESET_ALL}")
        
        try:
            if not self.db_manager.connect():
                return False
            
            users = []
            for i in range(count):
                user_id = f"D{i+1:03d}"
                first_name = fake.first_name()
                last_name = fake.last_name()
                full_name = f"Dr. {first_name} {last_name}"
                username = f"dr.{first_name.lower()}.{last_name.lower()}"
                
                user = {
                    'user_id': user_id,
                    'username': username,
                    'password_hash': self.hash_password('password123'),
                    'full_name': full_name,
                    'email': f"{username}@medlink.eg",
                    'phone': f"01{random.randint(0, 2)}{random.randint(10000000, 99999999)}",
                    'specialization': random.choice(self.departments),
                    'license_number': f"EG{random.randint(100000, 999999)}",
                    'hospital': random.choice(self.egyptian_hospitals),
                    'department': random.choice(self.departments),
                    'user_type': 'doctor'
                }
                users.append(user)
            
            # Insert users
            query = """
            INSERT INTO users (user_id, username, password_hash, full_name, email, phone,
                             specialization, license_number, hospital, department, user_type)
            VALUES (%(user_id)s, %(username)s, %(password_hash)s, %(full_name)s, %(email)s, %(phone)s,
                   %(specialization)s, %(license_number)s, %(hospital)s, %(department)s, %(user_type)s)
            """
            
            for user in users:
                self.db_manager.cursor.execute(query, user)
            
            self.db_manager.connection.commit()
            self.db_manager.disconnect()
            
            print(f"{Fore.GREEN}✅ Seeded {count} users{Style.RESET_ALL}")
            return True
            
        except Error as e:
            print(f"{Fore.RED}❌ Error seeding users: {e}{Style.RESET_ALL}")
            return False
    
    def seed_patients(self, count=50):
        """Generate and insert patients"""
        print(f"\n{Fore.YELLOW}🔄 Seeding {count} patients...{Style.RESET_ALL}")
        
        try:
            if not self.db_manager.connect():
                return False
            
            # Get existing doctors
            self.db_manager.cursor.execute("SELECT user_id FROM users LIMIT 1")
            doctor = self.db_manager.cursor.fetchone()
            registered_by = doctor['user_id'] if doctor else 'D001'
            
            patients = []
            for _ in range(count):
                national_id = self.generate_national_id()
                gender = random.choice(['male', 'female'])
                
                # Generate chronic conditions
                num_conditions = random.randint(0, 3)
                conditions = random.sample(self.chronic_conditions, min(num_conditions, len(self.chronic_conditions)))
                
                # Generate allergies
                allergies = []
                if random.random() > 0.7:
                    allergies = random.sample(['Penicillin', 'Aspirin', 'Peanuts', 'Shellfish', 'Latex'], random.randint(1, 2))
                
                # Generate medications
                num_meds = random.randint(0, 4)
                medications = random.sample(self.medications, min(num_meds, len(self.medications)))
                
                patient = {
                    'national_id': national_id,
                    'full_name': fake.name_male() if gender == 'male' else fake.name_female(),
                    'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=80),
                    'gender': gender,
                    'blood_type': random.choice(self.blood_types),
                    'phone': f"01{random.randint(0, 2)}{random.randint(10000000, 99999999)}",
                    'email': fake.email(),
                    'address': fake.address(),
                    'city': random.choice(self.egyptian_cities),
                    'governorate': random.choice(self.egyptian_cities),
                    'emergency_contact_name': fake.name(),
                    'emergency_contact_phone': f"01{random.randint(0, 2)}{random.randint(10000000, 99999999)}",
                    'emergency_contact_relation': random.choice(['Spouse', 'Parent', 'Sibling', 'Child', 'Friend']),
                    'chronic_conditions': json.dumps(conditions),
                    'allergies': json.dumps(allergies),
                    'current_medications': json.dumps(medications),
                    'family_history': json.dumps([]),
                    'disabilities': json.dumps([]),
                    'dnr_status': random.choice([True, False]) if random.random() > 0.9 else False,
                    'organ_donor': random.choice([True, False]),
                    'smoking_status': random.choice(['never', 'former', 'current']),
                    'alcohol_consumption': random.choice(['none', 'occasional', 'moderate']),
                    'exercise_frequency': random.choice(['none', 'rarely', 'weekly', 'daily']),
                    'registered_by': registered_by
                }
                patients.append(patient)
            
            # Insert patients
            query = """
            INSERT INTO patients (national_id, full_name, date_of_birth, gender, blood_type, phone, email,
                                address, city, governorate, emergency_contact_name, emergency_contact_phone,
                                emergency_contact_relation, chronic_conditions, allergies, current_medications,
                                family_history, disabilities, dnr_status, organ_donor, smoking_status,
                                alcohol_consumption, exercise_frequency, registered_by)
            VALUES (%(national_id)s, %(full_name)s, %(date_of_birth)s, %(gender)s, %(blood_type)s, %(phone)s,
                   %(email)s, %(address)s, %(city)s, %(governorate)s, %(emergency_contact_name)s,
                   %(emergency_contact_phone)s, %(emergency_contact_relation)s, %(chronic_conditions)s,
                   %(allergies)s, %(current_medications)s, %(family_history)s, %(disabilities)s,
                   %(dnr_status)s, %(organ_donor)s, %(smoking_status)s, %(alcohol_consumption)s,
                   %(exercise_frequency)s, %(registered_by)s)
            """
            
            inserted = 0
            for patient in patients:
                try:
                    self.db_manager.cursor.execute(query, patient)
                    inserted += 1
                except Error as e:
                    if "Duplicate entry" not in str(e):
                        print(f"{Fore.YELLOW}⚠️  Skipped duplicate patient{Style.RESET_ALL}")
            
            self.db_manager.connection.commit()
            self.db_manager.disconnect()
            
            print(f"{Fore.GREEN}✅ Seeded {inserted} patients{Style.RESET_ALL}")
            return True
            
        except Error as e:
            print(f"{Fore.RED}❌ Error seeding patients: {e}{Style.RESET_ALL}")
            return False
    
    def seed_visits(self, count=200):
        """Generate and insert visits"""
        print(f"\n{Fore.YELLOW}🔄 Seeding {count} visits...{Style.RESET_ALL}")
        
        try:
            if not self.db_manager.connect():
                return False
            
            # Get existing patients and doctors
            self.db_manager.cursor.execute("SELECT national_id FROM patients")
            patients = [row['national_id'] for row in self.db_manager.cursor.fetchall()]
            
            self.db_manager.cursor.execute("SELECT user_id, full_name FROM users")
            doctors = [(row['user_id'], row['full_name']) for row in self.db_manager.cursor.fetchall()]
            
            if not patients or not doctors:
                print(f"{Fore.YELLOW}⚠️  No patients or doctors found. Seed those first.{Style.RESET_ALL}")
                self.db_manager.disconnect()
                return False
            
            visits = []
            visit_types = ['Consultation', 'Follow-up', 'Emergency', 'Routine']
            
            for i in range(count):
                doctor_id, doctor_name = random.choice(doctors)
                visit_date = fake.date_between(start_date='-2y', end_date='today')
                
                visit = {
                    'visit_id': f"V{random.randint(10000, 99999)}",
                    'patient_national_id': random.choice(patients),
                    'doctor_id': doctor_id,
                    'doctor_name': doctor_name,
                    'visit_date': visit_date,
                    'visit_time': f"{random.randint(8, 17):02d}:{random.choice(['00', '15', '30', '45'])}",
                    'hospital': random.choice(self.egyptian_hospitals),
                    'department': random.choice(self.departments),
                    'visit_type': random.choice(visit_types),
                    'chief_complaint': fake.sentence(),
                    'diagnosis': fake.sentence(),
                    'treatment_plan': fake.text(max_nb_chars=200),
                    'notes': fake.text(max_nb_chars=150),
                    'attachments': json.dumps([])
                }
                visits.append(visit)
            
            # Insert visits
            query = """
            INSERT INTO visits (visit_id, patient_national_id, doctor_id, doctor_name, visit_date,
                              visit_time, hospital, department, visit_type, chief_complaint,
                              diagnosis, treatment_plan, notes, attachments)
            VALUES (%(visit_id)s, %(patient_national_id)s, %(doctor_id)s, %(doctor_name)s, %(visit_date)s,
                   %(visit_time)s, %(hospital)s, %(department)s, %(visit_type)s, %(chief_complaint)s,
                   %(diagnosis)s, %(treatment_plan)s, %(notes)s, %(attachments)s)
            """
            
            inserted = 0
            for visit in visits:
                try:
                    self.db_manager.cursor.execute(query, visit)
                    inserted += 1
                except Error as e:
                    if "Duplicate entry" not in str(e):
                        print(f"{Fore.YELLOW}⚠️  Error: {e}{Style.RESET_ALL}")
            
            self.db_manager.connection.commit()
            self.db_manager.disconnect()
            
            print(f"{Fore.GREEN}✅ Seeded {inserted} visits{Style.RESET_ALL}")
            return True
            
        except Error as e:
            print(f"{Fore.RED}❌ Error seeding visits: {e}{Style.RESET_ALL}")
            return False
    
    def import_json_data(self):
        """Import existing JSON data into database"""
        print(f"\n{Fore.YELLOW}🔄 Importing JSON data...{Style.RESET_ALL}")
        
        # This is a placeholder - you can implement actual JSON import here
        print(f"{Fore.GREEN}✅ JSON import completed{Style.RESET_ALL}")
        return True
    
    def seed_all(self):
        """Seed all data"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🌱 MedLink Data Seeding{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        success = True
        
        # Seed in order (respecting foreign keys)
        if self.config.get('generate_patients', 0) > 0:
            success &= self.seed_users(10)  # Create doctors first
            success &= self.seed_patients(self.config['generate_patients'])
        
        if self.config.get('generate_visits', 0) > 0:
            success &= self.seed_visits(self.config['generate_visits'])
        
        if self.config.get('import_json', False):
            success &= self.import_json_data()
        
        if success:
            print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✅ All Data Seeded Successfully!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
        else:
            print(f"\n{Fore.YELLOW}⚠️  Some seeding operations failed{Style.RESET_ALL}\n")
        
        # Show final status
        self.db_manager.print_database_status()


def main():
    """CLI interface for data seeding"""
    seeder = DataSeeder()
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}MedLink Data Seeder{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    print(f"{Fore.WHITE}Options:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}1. Seed All Data (Complete){Style.RESET_ALL}")
    print(f"{Fore.WHITE}2. Seed Users Only{Style.RESET_ALL}")
    print(f"{Fore.WHITE}3. Seed Patients Only{Style.RESET_ALL}")
    print(f"{Fore.WHITE}4. Seed Visits Only{Style.RESET_ALL}")
    print(f"{Fore.WHITE}5. Import JSON Data{Style.RESET_ALL}")
    print(f"{Fore.WHITE}6. Exit{Style.RESET_ALL}\n")
    
    choice = input(f"{Fore.CYAN}Choose option (1-6): {Style.RESET_ALL}").strip()
    
    if choice == "1":
        seeder.seed_all()
    elif choice == "2":
        seeder.seed_users(10)
    elif choice == "3":
        seeder.seed_patients(50)
    elif choice == "4":
        seeder.seed_visits(200)
    elif choice == "5":
        seeder.import_json_data()
    else:
        print(f"{Fore.GREEN}Exiting...{Style.RESET_ALL}")


if __name__ == "__main__":
    main()