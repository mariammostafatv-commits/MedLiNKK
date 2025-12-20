"""
Show ACTUAL patients table structure
"""

from core.database import get_db
from sqlalchemy import text

def show_patients_table():
    """Show actual columns in patients table"""
    try:
        with get_db() as db:
            # Show table structure
            print("=" * 80)
            print("ACTUAL COLUMNS IN patients TABLE:")
            print("=" * 80)
            result = db.execute(text("DESCRIBE patients")).fetchall()
            for row in result:
                print(f"  {row[0]:<25} {row[1]:<25} {row[2]:<5} {row[3]:<5}")
            
            # Show sample data
            print("\n" + "=" * 80)
            print("SAMPLE DATA (first 3 patients):")
            print("=" * 80)
            result = db.execute(text("SELECT * FROM patients LIMIT 3")).fetchall()
            
            if result:
                # Get column names
                columns = db.execute(text("SELECT * FROM patients LIMIT 0")).keys()
                
                for row_num, row in enumerate(result, 1):
                    print(f"\nPatient {row_num}:")
                    for i, col in enumerate(columns):
                        if row[i] is not None:
                            print(f"  {col}: {row[i]}")
            else:
                print("  No patients in table")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    show_patients_table()
