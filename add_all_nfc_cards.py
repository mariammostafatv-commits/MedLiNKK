"""
Add ALL NFC Cards - Doctors AND Patients
One script to add cards for everyone!
"""

from core.database import get_db
from sqlalchemy import text
from datetime import datetime, timedelta

def add_all_cards():
    """Add NFC cards for all doctors and patients"""
    try:
        with get_db() as db:
            print("=" * 80)
            print("ADDING NFC CARDS FOR DOCTORS")
            print("=" * 80)
            
            # Get all doctors (users with role='doctor')
            doctors = db.execute(
                text("""
                    SELECT user_id, full_name, username
                    FROM users 
                    WHERE role = 'doctor'
                    LIMIT 20
                """)
            ).fetchall()
            
            print(f"✅ Found {len(doctors)} doctors\n")
            
            # Add doctor cards starting from 0724184100
            doctor_base_uid = 724184100
            doctor_count = 0
            
            for i, doctor in enumerate(doctors):
                user_id, full_name, username = doctor
                card_uid = str(doctor_base_uid + i)
                
                # Check if card already exists
                existing = db.execute(
                    text("SELECT card_uid FROM nfc_cards WHERE owner_id = :owner_id"),
                    {"owner_id": str(user_id)}
                ).fetchone()
                
                if existing:
                    print(f"⚠️  Card exists: {full_name} (UID: {existing[0]})")
                    continue
                
                # Add NFC card
                issue_date = datetime.now().date()
                expiry_date = (datetime.now() + timedelta(days=365*5)).date()
                
                db.execute(
                    text("""
                        INSERT INTO nfc_cards 
                        (card_uid, card_type, owner_id, owner_name, status, is_active, 
                         issue_date, expiry_date, use_count)
                        VALUES 
                        (:card_uid, :card_type, :owner_id, :owner_name, :status, :is_active,
                         :issue_date, :expiry_date, 0)
                    """),
                    {
                        "card_uid": card_uid,
                        "card_type": "doctor",
                        "owner_id": str(user_id),
                        "owner_name": full_name,
                        "status": "active",
                        "is_active": 1,
                        "issue_date": issue_date,
                        "expiry_date": expiry_date
                    }
                )
                
                print(f"✅ Doctor card {card_uid} - {full_name}")
                doctor_count += 1
            
            print(f"\n{'='*80}")
            print("ADDING NFC CARDS FOR PATIENTS")
            print(f"{'='*80}")
            
            # Get all patients
            patients = db.execute(
                text("""
                    SELECT p.national_id, p.full_name, u.user_id 
                    FROM patients p
                    JOIN users u ON p.user_id = u.user_id
                    LIMIT 50
                """)
            ).fetchall()
            
            print(f"✅ Found {len(patients)} patients\n")
            
            # Add patient cards starting from 0724975956
            patient_base_uid = 724975956
            patient_count = 0
            
            for i, patient in enumerate(patients):
                national_id, full_name, user_id = patient
                card_uid = str(patient_base_uid + i)
                
                # Check if card already exists
                existing = db.execute(
                    text("SELECT card_uid FROM nfc_cards WHERE owner_id = :owner_id"),
                    {"owner_id": str(user_id)}
                ).fetchone()
                
                if existing:
                    print(f"⚠️  Card exists: {full_name} (UID: {existing[0]})")
                    continue
                
                # Add NFC card
                issue_date = datetime.now().date()
                expiry_date = (datetime.now() + timedelta(days=365*5)).date()
                
                db.execute(
                    text("""
                        INSERT INTO nfc_cards 
                        (card_uid, card_type, owner_id, owner_name, status, is_active, 
                         issue_date, expiry_date, use_count)
                        VALUES 
                        (:card_uid, :card_type, :owner_id, :owner_name, :status, :is_active,
                         :issue_date, :expiry_date, 0)
                    """),
                    {
                        "card_uid": card_uid,
                        "card_type": "patient",
                        "owner_id": str(user_id),
                        "owner_name": full_name,
                        "status": "active",
                        "is_active": 1,
                        "issue_date": issue_date,
                        "expiry_date": expiry_date
                    }
                )
                
                print(f"✅ Patient card {card_uid} - {full_name}")
                patient_count += 1
            
            db.commit()
            
            # Show summary
            print(f"\n{'='*80}")
            print("SUMMARY - ALL NFC CARDS")
            print(f"{'='*80}")
            
            result = db.execute(
                text("""
                    SELECT card_uid, owner_name, card_type, status 
                    FROM nfc_cards 
                    ORDER BY card_type, card_uid
                """)
            ).fetchall()
            
            print(f"\n{'Card UID':<15} {'Name':<35} {'Type':<10} {'Status':<10}")
            print("-" * 80)
            
            for uid, name, ctype, status in result:
                icon = "👨‍⚕️" if ctype == "doctor" else "👤"
                print(f"{uid:<15} {icon} {name:<33} {ctype:<10} {status:<10}")
            
            print(f"\n{'='*80}")
            print(f"✅ Added {doctor_count} doctor cards")
            print(f"✅ Added {patient_count} patient cards")
            print(f"🎊 Total: {len(result)} cards in database")
            print(f"{'='*80}")
            
            print(f"\n🎉 SUCCESS! All NFC cards ready!")
            print(f"\nDoctor cards: 0724184100 - 0724184{100 + len(doctors) - 1}")
            print(f"Patient cards: 0724975956 - 0724975{956 + len(patients) - 1}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\n🔧 ADDING ALL NFC CARDS (DOCTORS + PATIENTS)\n")
    add_all_cards()
    print("\n✅ Done! Test with: python main.py\n")
