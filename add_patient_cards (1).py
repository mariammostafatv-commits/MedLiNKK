"""
Add Patient NFC Cards - CORRECTED
Patients use national_id (no user_id)
"""

from core.database import get_db
from sqlalchemy import text
from datetime import datetime, timedelta

def add_patient_cards():
    """Add NFC cards for patients"""
    try:
        with get_db() as db:
            # Get all patients (use national_id, not user_id!)
            patients = db.execute(
                text("""
                    SELECT national_id, full_name
                    FROM patients
                    LIMIT 50
                """)
            ).fetchall()
            
            if not patients:
                print("❌ No patients found in database!")
                return
            
            print(f"✅ Found {len(patients)} patients\n")
            
            # Generate card UIDs starting from 0724975956
            base_uid = 724975956
            added_count = 0
            
            for i, patient in enumerate(patients):
                national_id, full_name = patient
                card_uid = str(base_uid + i)
                
                # Check if card already exists
                existing = db.execute(
                    text("SELECT card_uid FROM nfc_cards WHERE owner_id = :owner_id AND card_type = 'patient'"),
                    {"owner_id": national_id}
                ).fetchone()
                
                if existing:
                    print(f"⚠️  Card already exists for {full_name} (UID: {existing[0]})")
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
                        "owner_id": national_id,  # Use national_id for patients!
                        "owner_name": full_name,
                        "status": "active",
                        "is_active": 1,
                        "issue_date": issue_date,
                        "expiry_date": expiry_date
                    }
                )
                
                print(f"✅ Added card {card_uid} for {full_name} (ID: {national_id})")
                added_count += 1
            
            db.commit()
            
            # Show all cards
            print(f"\n{'='*80}")
            print("ALL NFC CARDS IN DATABASE:")
            print(f"{'='*80}")
            
            result = db.execute(
                text("""
                    SELECT card_uid, owner_name, card_type, owner_id, status 
                    FROM nfc_cards 
                    ORDER BY card_type, card_uid
                """)
            ).fetchall()
            
            print(f"\n{'Card UID':<15} {'Name':<30} {'Type':<10} {'Owner ID':<15} {'Status':<10}")
            print("-" * 90)
            for uid, name, ctype, owner_id, status in result:
                icon = "👨‍⚕️" if ctype == "doctor" else "👤"
                print(f"{uid:<15} {icon} {name:<28} {ctype:<10} {owner_id:<15} {status:<10}")
            
            print(f"\n{'='*80}")
            print(f"✅ Added {added_count} new patient cards")
            print(f"🎊 Total: {len(result)} cards in database")
            print(f"{'='*80}")
            print(f"\nYou can now scan patient cards!")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔧 Adding patient NFC cards...\n")
    add_patient_cards()
    print("\n✅ Done!")
