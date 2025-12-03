"""
NFC Card Manager - Map card IDs to users
Location: core/card_manager.py
"""
import json
import os
from typing import Optional, Dict


class CardManager:
    """Manage NFC card to user mappings"""
    
    def __init__(self):
        self.cards_file = 'data/cards.json'
        self.cards = self.load_cards()
    
    def load_cards(self) -> Dict:
        """Load card mappings from file"""
        if os.path.exists(self.cards_file):
            try:
                with open(self.cards_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading cards: {e}")
                return self._create_default_cards()
        else:
            return self._create_default_cards()
    
    def _create_default_cards(self) -> Dict:
        """Create default card mappings"""
        default_cards = {
            "doctor_cards": {
                "0724975956": {
                    "username": "dr.ahmed",
                    "name": "Dr. Ahmed Mohamed",
                    "type": "doctor"
                },
                "0724975957": {
                    "username": "dr.mohamed",
                    "name": "Dr. Mohamed Hassan",
                    "type": "doctor"
                },
                "0724975958": {
                    "username": "dr.fatma",
                    "name": "Dr. Fatma Ali",
                    "type": "doctor"
                }
            },
            "patient_cards": {
                "0724975959": {
                    "national_id": "29501012345678",
                    "name": "Mohamed Ali Hassan",
                    "type": "patient"
                },
                "0724975960": {
                    "national_id": "28803151234567",
                    "name": "Sara Ahmed Ibrahim",
                    "type": "patient"
                },
                "0724975961": {
                    "national_id": "29201203456789",
                    "name": "Ahmed Hassan Mahmoud",
                    "type": "patient"
                }
            }
        }
        
        # Save default cards
        os.makedirs('data', exist_ok=True)
        with open(self.cards_file, 'w', encoding='utf-8') as f:
            json.dump(default_cards, f, indent=2, ensure_ascii=False)
        
        return default_cards
    
    def get_user_by_card(self, card_id: str) -> Optional[Dict]:
        """
        Get user info by card ID
        
        Returns:
            {
                'type': 'doctor' or 'patient',
                'username': '...' (for doctors),
                'national_id': '...' (for patients),
                'name': '...'
            }
        """
        card_id = card_id.strip()
        
        # Check doctor cards
        if card_id in self.cards.get('doctor_cards', {}):
            return self.cards['doctor_cards'][card_id]
        
        # Check patient cards
        if card_id in self.cards.get('patient_cards', {}):
            return self.cards['patient_cards'][card_id]
        
        return None
    
    def add_card(self, card_id: str, user_type: str, user_data: Dict) -> bool:
        """Add new card mapping"""
        try:
            card_id = card_id.strip()
            
            if user_type == 'doctor':
                if 'doctor_cards' not in self.cards:
                    self.cards['doctor_cards'] = {}
                self.cards['doctor_cards'][card_id] = {
                    **user_data,
                    'type': 'doctor'
                }
            elif user_type == 'patient':
                if 'patient_cards' not in self.cards:
                    self.cards['patient_cards'] = {}
                self.cards['patient_cards'][card_id] = {
                    **user_data,
                    'type': 'patient'
                }
            else:
                return False
            
            # Save to file
            with open(self.cards_file, 'w', encoding='utf-8') as f:
                json.dump(self.cards, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error adding card: {e}")
            return False
    
    def remove_card(self, card_id: str) -> bool:
        """Remove card mapping"""
        try:
            card_id = card_id.strip()
            
            # Check and remove from doctor cards
            if card_id in self.cards.get('doctor_cards', {}):
                del self.cards['doctor_cards'][card_id]
                with open(self.cards_file, 'w', encoding='utf-8') as f:
                    json.dump(self.cards, f, indent=2, ensure_ascii=False)
                return True
            
            # Check and remove from patient cards
            if card_id in self.cards.get('patient_cards', {}):
                del self.cards['patient_cards'][card_id]
                with open(self.cards_file, 'w', encoding='utf-8') as f:
                    json.dump(self.cards, f, indent=2, ensure_ascii=False)
                return True
            
            return False
        except Exception as e:
            print(f"Error removing card: {e}")
            return False
    
    def get_all_doctor_cards(self) -> Dict:
        """Get all doctor card mappings"""
        return self.cards.get('doctor_cards', {})
    
    def get_all_patient_cards(self) -> Dict:
        """Get all patient card mappings"""
        return self.cards.get('patient_cards', {})


# Global card manager instance
card_manager = CardManager()