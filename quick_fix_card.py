"""
Show ACTUAL table structure - no guessing!
"""

from core.database import get_db
from sqlalchemy import text

def show_table_structure():
    """Show actual columns in nfc_cards table"""
    try:
        with get_db() as db:
            # Method 1: DESCRIBE table
            print("=" * 80)
            print("ACTUAL COLUMNS IN nfc_cards TABLE:")
            print("=" * 80)
            result = db.execute(text("DESCRIBE nfc_cards")).fetchall()
            for row in result:
                print(f"  {row[0]:<20} {row[1]:<20} {row[2]:<5} {row[3]:<5}")
            
            # Method 2: Show first row
            print("\n" + "=" * 80)
            print("SAMPLE DATA (first row):")
            print("=" * 80)
            result = db.execute(text("SELECT * FROM nfc_cards LIMIT 1")).fetchone()
            if result:
                # Get column names
                columns = db.execute(text("SELECT * FROM nfc_cards LIMIT 0")).keys()
                for i, col in enumerate(columns):
                    print(f"  {col}: {result[i]}")
            else:
                print("  No data in table")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    show_table_structure()