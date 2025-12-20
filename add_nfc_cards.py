"""
Add NFC Cards - Table is EMPTY!
This adds Dr. Ahmed Hassan's card to the database
"""

from core.database import get_db
from sqlalchemy import text
from datetime import datetime, timedelta

def add_doctor_cards():
    """Add NFC cards for doctors"""
    try:
        with get_db() as db:
            # First, check if Dr. Ahmed Hassan exists
            user = db.execute(
                text("SELECT user_id, full_name FROM users WHERE username = 'dr.ahmed.hassan'")
            ).fetchone()
            
            if not user:
                print("❌ Dr. Ahmed Hassan not found in users table!")
                print("   Please create user account first")
                return
            
            user_id = user[0]
            full_name = user[1]
            
            print(f"✅ Found user: {full_name} (ID: {user_id})")
            
            # Add NFC card for this doctor
            print(f"\n🔧 Adding NFC card: 0724184100")
            
            issue_date = datetime.now().date()
            expiry_date = (datetime.now() + timedelta(days=365*5)).date()  # 5 years validity
            
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
                    "card_uid": "0724184100",
                    "card_type": "doctor",
                    "owner_id": str(user_id),
                    "owner_name": full_name,
                    "status": "active",
                    "is_active": 1,
                    "issue_date": issue_date,
                    "expiry_date": expiry_date
                }
            )
            db.commit()
            
            print(f"✅ Card added successfully!")
            
            # Verify
            print(f"\n📋 Verification:")
            result = db.execute(
                text("SELECT card_uid, owner_id, owner_name, card_type, status FROM nfc_cards")
            ).fetchall()
            
            for uid, oid, name, ctype, status in result:
                print(f"   {uid} - {name} ({ctype}, status: {status})")
            
            print(f"\n🎊 SUCCESS! You can now scan card: 0724184100")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔧 Adding NFC cards to database...\n")
    add_doctor_cards()
    print("\n✅ Done! Test with: python main.py")
