"""
Migrate NFC cards from JSON to database
Location: database/migrations/migrate_cards.py
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_db_context
from database.models import NFCCard


def migrate_cards(json_file_path: str = 'data/cards.json'):
    """
    Migrate NFC cards from JSON file to database
    
    Args:
        json_file_path: Path to cards.json file
    
    Returns:
        (success: bool, message: str, count: int)
    """
    print("\n" + "="*60)
    print("💳 MIGRATING NFC CARDS")
    print("="*60)
    
    try:
        # Load JSON data
        print(f"📖 Reading from: {json_file_path}")
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get doctor and patient cards
        doctor_cards = data.get('doctor_cards', {})
        patient_cards = data.get('patient_cards', {})
        
        total_cards = len(doctor_cards) + len(patient_cards)
        print(f"✅ Found {len(doctor_cards)} doctor cards")
        print(f"✅ Found {len(patient_cards)} patient cards")
        print(f"✅ Total: {total_cards} cards")
        
        if total_cards == 0:
            return True, "No cards to migrate", 0
        
        # Migrate to database
        migrated_count = 0
        skipped_count = 0
        
        # Track all card UIDs to detect duplicates BEFORE adding to database
        seen_uids = set()
        
        with get_db_context() as db:
            # Migrate doctor cards
            for card_uid, card_data in doctor_cards.items():
                # Check if card already exists in database
                existing = db.query(NFCCard).filter_by(card_uid=card_uid).first()
                if existing:
                    print(f"  ⏭️  Skipping {card_uid} (already exists in database)")
                    skipped_count += 1
                    continue
                
                # Check for duplicate within this migration batch
                if card_uid in seen_uids:
                    print(f"  ⚠️  Skipping {card_uid} → {card_data.get('name')} (DUPLICATE CARD UID!)")
                    skipped_count += 1
                    continue
                
                # Mark as seen
                seen_uids.add(card_uid)
                
                # Create NFC card object
                nfc_card = NFCCard(
                    card_uid=card_uid,
                    card_type='doctor',
                    username=card_data.get('username'),
                    national_id=None,
                    holder_name=card_data.get('name'),
                    status='active',
                    created_at=datetime.now(),
                    last_used=None
                )
                
                db.add(nfc_card)
                print(f"  ✅ Doctor card: {card_uid} → {nfc_card.holder_name}")
                migrated_count += 1
            
            # Migrate patient cards
            for card_uid, card_data in patient_cards.items():
                # Check if card already exists in database
                existing = db.query(NFCCard).filter_by(card_uid=card_uid).first()
                if existing:
                    print(f"  ⏭️  Skipping {card_uid} (already exists in database)")
                    skipped_count += 1
                    continue
                
                # Check for duplicate within this migration batch
                if card_uid in seen_uids:
                    print(f"  ⚠️  Skipping {card_uid} → {card_data.get('name')} (DUPLICATE CARD UID!)")
                    skipped_count += 1
                    continue
                
                # Mark as seen
                seen_uids.add(card_uid)
                
                # Create NFC card object
                nfc_card = NFCCard(
                    card_uid=card_uid,
                    card_type='patient',
                    username=None,
                    national_id=card_data.get('national_id'),
                    holder_name=card_data.get('name'),
                    status='active',
                    created_at=datetime.now(),
                    last_used=None
                )
                
                db.add(nfc_card)
                print(f"  ✅ Patient card: {card_uid} → {nfc_card.holder_name}")
                migrated_count += 1
        
        print(f"\n✅ Migration complete!")
        print(f"   Migrated: {migrated_count}")
        print(f"   Skipped: {skipped_count}")
        
        return True, f"Successfully migrated {migrated_count} NFC cards", migrated_count
        
    except FileNotFoundError:
        error_msg = f"❌ File not found: {json_file_path}"
        print(error_msg)
        return False, error_msg, 0
    
    except Exception as e:
        error_msg = f"❌ Error during migration: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return False, error_msg, 0


if __name__ == "__main__":
    # Run standalone
    success, message, count = migrate_cards()
    sys.exit(0 if success else 1)