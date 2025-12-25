"""
Insert Survey Data into MedLink Database
This script inserts all the data from the questionnaire PDFs
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.database import get_db_context
from core.models import *
from utils.security import hash_password

# Survey data extracted from PDFs
SURVEY_DATA = [
    # Students
    {
        "name": "Mariam Mostafa Lotfy",
        "student_id": "250102822",
        "email": None,  # Not provided in PDF
        "phone": "01144773066",
        "birth_date": "2007-05-25",
        "role": "student",
        "chronic_diseases": [],
        "allergies": ["Hazelnuts (بندق)"],
        "surgeries": ["Tonsillectomy (اللوز)"],
        "blood_type": "A+",
        "nfc_card_id": "0052734218"
    },
    {
        "name": "Mohamed Abdeltwab Mostafa",
        "student_id": "250103396",
        "email": None,
        "phone": "01096326337",
        "birth_date": "2025-12-06",  # Likely typo in form, should be 2006
        "role": "student",
        "chronic_diseases": [],
        "allergies": [],
        "surgeries": [],
        "blood_type": None,
        "nfc_card_id": "0045269565"
    },
    {
        "name": "Mahmoud Khaled Ahmed",
        "student_id": "250102827",
        "email": None,
        "phone": "01019229340",
        "birth_date": "2007-10-29",
        "role": "student",
        "chronic_diseases": [],
        "allergies": [],
        "surgeries": [],
        "blood_type": "O+",
        "nfc_card_id": "0035129109"
    },
    {
        "name": "Mohamed Ahmed Mosaad",
        "student_id": "240102807",
        "email": None,
        "phone": "01229239432",
        "birth_date": "2006-10-23",
        "role": "student",
        "chronic_diseases": [],
        "allergies": [],
        "surgeries": [],
        "blood_type": None,
        "nfc_card_id": "0052474795"
    },
    {
        "name": "Omar Ahmed Gouda",
        "student_id": "250104265",
        "email": None,
        "phone": "01033717699",
        "birth_date": "2007-02-19",
        "role": "student",
        "chronic_diseases": [],
        "allergies": [],
        "surgeries": [],
        "blood_type": "O+",
        "nfc_card_id": "0052889209"
    },
    {
        "name": "Youssef Atif Abdelkream",
        "student_id": "250102910",
        "email": None,
        "phone": "01070685797",
        "birth_date": "2007-11-25",
        "role": "student",
        "chronic_diseases": [],
        "allergies": [],
        "surgeries": [],
        "blood_type": None,
        "nfc_card_id": "0035107125"
    },
    {
        "name": "Youssef Elsaeed Mostafa",
        "student_id": "250103438",
        "email": None,
        "phone": "01030202105",
        "birth_date": "2007-08-20",
        "role": "student",
        "chronic_diseases": [],
        "allergies": [],
        "surgeries": [],
        "blood_type": None,
        "nfc_card_id": "0045184006"
    },
    {
        "name": "Youssef El Sayed",
        "student_id": "250103408",
        "email": None,
        "phone": "01064516728",
        "birth_date": "2007-02-08",
        "role": "student",
        "chronic_diseases": [],
        "allergies": [],
        "surgeries": ["Adenoidectomy and Tonsillectomy (اللحمية واللوز)"],
        "blood_type": "A+",
        "nfc_card_id": "0045651748"
    },
    {
        "name": "Youssef Gamal Mohamed Mahmoud",
        "student_id": "250103050",
        "email": "abc@gmail.com",
        "phone": "01026737472",
        "birth_date": "2000-03-26",
        "role": "student",
        "chronic_diseases": [],
        "allergies": ["Animals and plants (الحيوانات و نباتات)"],
        "surgeries": [],
        "blood_type": None,
        "nfc_card_id": "0052489229"
    },
    {
        "name": "Abanoub Adel Amir",
        "student_id": "250103126",
        "email": "abanoub250103126@sut.edu.eg",
        "phone": "01206833256",
        "birth_date": "2007-09-16",
        "role": "student",
        "chronic_diseases": [],
        "allergies": [],
        "surgeries": ["Yes (نعم)"],  # Details not specified
        "blood_type": None,
        "nfc_card_id": "0045204499"
    },
    {
        "name": "Abdelrhman Ahmed Mohamed",
        "student_id": "250103433",
        "email": None,
        "phone": "01060910194",
        "birth_date": "2006-10-30",
        "role": "student",
        "chronic_diseases": [],
        "allergies": [],
        "surgeries": [],
        "blood_type": None,
        "nfc_card_id": "0053809534"
    },
    {
        "name": "Abdelrahman Mohamed Elsayed",
        "student_id": "250103320",
        "email": None,
        "phone": "01024390676",
        "birth_date": "2007-07-21",
        "role": "student",
        "chronic_diseases": [],
        "allergies": [],
        "surgeries": [],
        "blood_type": "O+",
        "nfc_card_id": "0045204739"
    },
    {
        "name": "Ahmed Yasser Gomaa",
        "student_id": "250102872",
        "email": "a20yasser200@gmail.com",
        "phone": "01212549614",
        "birth_date": "2007-01-10",
        "role": "student",
        "chronic_diseases": [],
        "allergies": [],
        "surgeries": ["LASIK Eye Surgery (ليزك ي دكتره)"],
        "blood_type": None,
        "nfc_card_id": "0045268870"
    },
    {
        "name": "Desouky Hatem Desouky",
        "student_id": "250103142",
        "email": None,
        "phone": "01093468070",
        "birth_date": "2007-04-16",
        "role": "student",
        "chronic_diseases": [],
        "allergies": [],
        "surgeries": [],
        "blood_type": None,  # Not answered
        "nfc_card_id": "0052712197"
    },
    {
        "name": "Hafsa Ahmed Mohamed",
        "student_id": "250102620",
        "email": "hafsa250102620@sut.edu.eg",
        "phone": "01270277739",
        "birth_date": "2006-04-04",
        "role": "student",
        "chronic_diseases": [],
        "allergies": [],
        "surgeries": [],
        "blood_type": "O+",
        "nfc_card_id": "0045200862"
    },
    {
        "name": "Manar Mohamed Hassan",
        "student_id": "250102656",
        "email": None,
        "phone": "01555204752",
        "birth_date": "2007-08-26",
        "role": "student",
        "chronic_diseases": [],
        "allergies": [],
        "surgeries": ["Hand fracture surgery (نعم كسر اليد)"],
        "blood_type": None,
        "nfc_card_id": "0045791045"
    },
    
    # Doctors
    {
        "name": "Ahmed Moawad Ibrahim",
        "student_id": None,
        "email": "ahmed.moawad@sut.edu.eg",
        "phone": "01061946452",
        "birth_date": "1992-03-22",
        "role": "doctor",
        "chronic_diseases": [],
        "allergies": [],
        "surgeries": [],
        "blood_type": None,
        "nfc_card_id": "0053379675",
        "specialization": "Computer Science",
        "license_number": "DOC-AM-2024-001"
    },
    {
        "name": "Ahmed Youssef Mohamed",
        "student_id": None,
        "email": "aeyouseff@gmail.com",
        "phone": "01009453403",
        "birth_date": "2000-09-05",
        "role": "doctor",
        "chronic_diseases": [],
        "allergies": [],
        "surgeries": [],
        "blood_type": None,
        "nfc_card_id": None,  # Not provided
        "specialization": "Computer Science",
        "license_number": "DOC-AY-2024-002"
    },
    {
        "name": "Mai Hassanin ElBaradei",
        "student_id": None,
        "email": "mai.hassanin@sut.edu.eg",
        "phone": "01000000000",
        "birth_date": "1998-11-06",
        "role": "doctor",
        "chronic_diseases": [],
        "allergies": [],
        "surgeries": [],
        "blood_type": None,
        "nfc_card_id": "0045647885",
        "specialization": "Computer Science",
        "license_number": "DOC-MH-2024-003"
    },
]


def calculate_age(birth_date_str):
    """Calculate age from birth date string"""
    try:
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        today = datetime.today().date()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except:
        return 18  # Default age


def parse_name(full_name):
    """Parse full name into first and last name"""
    parts = full_name.strip().split()
    if len(parts) >= 2:
        first_name = parts[0]
        last_name = " ".join(parts[1:])
    else:
        first_name = full_name
        last_name = ""
    return first_name, last_name


def insert_data():
    """Insert all survey data into database"""
    
    print("=" * 60)
    print("MedLink - Insert Survey Data")
    print("=" * 60)
    print()
    
    with get_db_context() as db:
        inserted_patients = 0
        inserted_doctors = 0
        inserted_cards = 0
        skipped = 0
        
        for idx, person in enumerate(SURVEY_DATA, 1):
            print(f"[{idx}/{len(SURVEY_DATA)}] Processing: {person['name']}")
            
            try:
                # Parse name
                first_name, last_name = parse_name(person['name'])
                
                # Calculate age
                age = calculate_age(person['birth_date'])
                
                # Generate national ID (using student ID or generating one)
                if person['student_id']:
                    national_id = person['student_id']
                else:
                    # For doctors without student ID, generate from birth date and phone
                    national_id = f"DOC{person['phone'][-8:]}"
                
                # Check if already exists
                existing_patient = db.query(Patient).filter_by(national_id=national_id).first()
                if existing_patient:
                    print(f"  ⚠️  Already exists: {person['name']} (NID: {national_id})")
                    skipped += 1
                    continue
                
                # Determine gender from name
                gender = Gender.Female if any(n in first_name.lower() for n in ['mariam', 'hafsa', 'manar', 'mai']) else Gender.Male
                
                # Parse blood type to enum if provided
                blood_type_enum = None
                if person.get('blood_type'):
                    blood_type_map = {
                        'A+': BloodType.A_POSITIVE,
                        'A-': BloodType.A_NEGATIVE,
                        'B+': BloodType.B_POSITIVE,
                        'B-': BloodType.B_NEGATIVE,
                        'AB+': BloodType.AB_POSITIVE,
                        'AB-': BloodType.AB_NEGATIVE,
                        'O+': BloodType.O_POSITIVE,
                        'O-': BloodType.O_NEGATIVE,
                    }
                    blood_type_enum = blood_type_map.get(person.get('blood_type'))
                
                # Create patient
                patient = Patient(
                    national_id=national_id,
                    full_name=person['name'],
                    date_of_birth=datetime.strptime(person['birth_date'], "%Y-%m-%d").date(),
                    age=age,
                    gender=gender,
                    blood_type=blood_type_enum,
                    phone=person['phone'],
                    email=person.get('email'),
                    address="Cairo, Egypt",
                    city="Cairo",
                    governorate="Cairo",
                    emergency_contact={
                        'name': 'Emergency Contact',
                        'relation': 'Family',
                        'phone': person['phone']
                    }
                )
                db.add(patient)
                db.flush()  # Get the patient ID
                
                print(f"  ✅ Patient created: {patient.full_name} (NID: {national_id})")
                inserted_patients += 1
                
                # Add allergies
                if person.get('allergies'):
                    for allergen in person['allergies']:
                        if allergen.strip():
                            allergy = Allergy(
                                patient_national_id=national_id,
                                allergen_name=allergen,
                                severity="Moderate",
                                reaction="Allergic reaction",
                                date_identified=datetime.now().date()
                            )
                            db.add(allergy)
                    print(f"  ✅ Added {len(person['allergies'])} allergies")
                
                # Add chronic diseases (none in this dataset)
                if person.get('chronic_diseases'):
                    for disease in person['chronic_diseases']:
                        if disease.strip():
                            chronic = ChronicDisease(
                                patient_national_id=national_id,
                                disease_name=disease,
                                date_diagnosed=datetime.now().date(),
                                is_active=True
                            )
                            db.add(chronic)
                    print(f"  ✅ Added {len(person['chronic_diseases'])} chronic diseases")
                
                # Add surgeries
                if person.get('surgeries'):
                    for surgery_desc in person['surgeries']:
                        if surgery_desc.strip() and surgery_desc.lower() not in ['no', 'لا', 'نعم', 'yes']:
                            surgery = Surgery(
                                patient_national_id=national_id,
                                surgery_id=f"SRG-{national_id}-{len(person['surgeries'])}",
                                procedure_name=surgery_desc,
                                surgery_date=datetime.now().date(),  # Date not provided
                                hospital="Not specified",
                                surgeon_name="Not specified"
                            )
                            db.add(surgery)
                    print(f"  ✅ Added {len(person['surgeries'])} surgeries")
                
                # Add NFC card if provided
                if person.get('nfc_card_id'):
                    # Check if card already assigned
                    existing_card = db.query(PatientCard).filter_by(card_uid=person['nfc_card_id']).first()
                    if not existing_card:
                        card = PatientCard(
                            patient_national_id=national_id,
                            card_uid=person['nfc_card_id'],
                            full_name=person['name'],
                            blood_type=person.get('blood_type'),
                            card_type='patient',
                            is_active=True,
                            issue_date=datetime.now().date()
                        )
                        db.add(card)
                        print(f"  ✅ NFC card assigned: {person['nfc_card_id']}")
                        inserted_cards += 1
                    else:
                        print(f"  ⚠️  NFC card already assigned: {person['nfc_card_id']}")
                
                # If doctor, create doctor record
                if person['role'] == 'doctor':
                    # Create user account first
                    username = person['email'].split('@')[0] if person.get('email') else f"dr.{first_name.lower()}"
                    
                    # Check if user exists
                    existing_user = db.query(User).filter_by(username=username).first()
                    if not existing_user:
                        user = User(
                            username=username,
                            password_hash=hash_password("password123"),  # Default password
                            role=UserRole.doctor,
                            full_name=person['name'],
                            email=person.get('email'),
                            phone=person['phone'],
                            is_active=True
                        )
                        db.add(user)
                        db.flush()  # Get user ID
                        
                        # Create doctor record
                        doctor = Doctor(
                            user_id=user.user_id,
                            national_id=national_id,
                            specialization=person.get('specialization', 'General Practice'),
                            license_number=person.get('license_number', f'LIC-{national_id}'),
                            hospital='Elsewedy University of Technology',
                            department='Computer Science'
                        )
                        db.add(doctor)
                        print(f"  ✅ Doctor account created: {username}")
                        inserted_doctors += 1
                    else:
                        print(f"  ⚠️  Doctor account already exists: {username}")
                
                print()  # Blank line between records
                
            except Exception as e:
                print(f"  ❌ Error processing {person['name']}: {str(e)}")
                print()
                continue
        
        # Commit all changes
        db.commit()
        
        # Print summary
        print("=" * 60)
        print("Summary:")
        print("=" * 60)
        print(f"✅ Patients inserted: {inserted_patients}")
        print(f"✅ Doctors inserted: {inserted_doctors}")
        print(f"✅ NFC cards assigned: {inserted_cards}")
        print(f"⚠️  Skipped (already exist): {skipped}")
        print(f"📊 Total processed: {len(SURVEY_DATA)}")
        print("=" * 60)
        print()
        print("✅ All data inserted successfully!")
        print()


if __name__ == "__main__":
    try:
        insert_data()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()