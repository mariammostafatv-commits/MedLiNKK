"""
ONE-COMMAND FIX - Update Dr. Ahmed Hassan's card UID
Uses correct column names: username (not user_id)
"""

from core.database import get_db
from sqlalchemy import text

def fix_card():
    """Update Dr. Ahmed Hassan's card UID"""
    try:
        with get_db() as db:
            # Show before
            print("\n📋 BEFORE:")
            result = db.execute(
                text("SELECT card_uid, username, full_name FROM nfc_cards WHERE username = 'dr.ahmed.hassan'")
            ).fetchone()
            if result:
                print(f"   {result[0]} - {result[2]} ({result[1]})")
            else:
                print("   Dr. Ahmed Hassan not found! Showing all cards:")
                results = db.execute(text("SELECT card_uid, username, full_name FROM nfc_cards LIMIT 5")).fetchall()
                for uid, username, name in results:
                    print(f"   {uid} - {name} ({username})")
                return
            
            # Update
            print("\n🔧 Updating card UID...")
            db.execute(
                text("UPDATE nfc_cards SET card_uid = '0724184100' WHERE username = 'dr.ahmed.hassan'")
            )
            db.commit()
            
            # Show after
            print("\n✅ AFTER:")
            result = db.execute(
                text("SELECT card_uid, username, full_name FROM nfc_cards WHERE username = 'dr.ahmed.hassan'")
            ).fetchone()
            if result:
                print(f"   {result[0]} - {result[2]} ({result[1]})")
            
            print("\n🎊 SUCCESS! Now scan card: 0724184100")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔧 Fixing Dr. Ahmed Hassan's card UID...\n")
    fix_card()
    print("\n✅ Done! Test with: python main.py")
