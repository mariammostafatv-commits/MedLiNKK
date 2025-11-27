"""
NFC card manager for R20C reader
"""
import serial
from typing import Optional, Tuple
from config.hardware_config import NFC_CONFIG
from core.data_manager import data_manager
from core.patient_manager import patient_manager
from utils.logger import log_hardware_event
from datetime import datetime


class NFCManager:
    """Manages R20C NFC card reader operations"""
    
    def __init__(self):
        self.port = NFC_CONFIG['port']
        self.baudrate = NFC_CONFIG['baudrate']
        self.ser = None
        self.is_connected = False
    
    def connect(self) -> Tuple[bool, str]:
        """
        Connect to R20C NFC reader
        
        Returns:
            (success: bool, message: str)
        """
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=NFC_CONFIG['timeout']
            )
            
            self.is_connected = True
            return True, "NFC reader connected successfully"
            
        except serial.SerialException as e:
            return False, f"Connection error: {str(e)}"
    
    def disconnect(self):
        """Disconnect from reader"""
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.is_connected = False
    
    def read_card_uid(self, timeout: int = 30) -> Tuple[bool, Optional[str], str]:
        """
        Read UID from NFC card/tag
        
        Args:
            timeout: Seconds to wait for card tap
            
        Returns:
            (success: bool, uid: str or None, message: str)
        """
        if not self.is_connected:
            success, msg = self.connect()
            if not success:
                return False, None, msg
        
        try:
            import time
            start_time = time.time()
            
            print(f"Waiting for NFC card... ({timeout}s timeout)")
            
            while time.time() - start_time < timeout:
                if self.ser.in_waiting > 0:
                    data = self.ser.readline()
                    
                    if data:
                        # Parse UID (format depends on R20C configuration)
                        uid = data.decode('utf-8').strip()
                        
                        # Validate UID format
                        if self._is_valid_uid(uid):
                            print(f"✅ Card detected: {uid}")
                            return True, uid, "Card read successfully"
                
                time.sleep(0.1)
            
            return False, None, "Timeout - No card detected"
            
        except Exception as e:
            return False, None, f"Read error: {str(e)}"
    
    def assign_card_to_patient(self, national_id: str, card_type: str = "Mifare Classic 1K") -> Tuple[bool, str]:
        """
        Assign NFC card to patient
        
        Args:
            national_id: Patient's National ID
            card_type: Type of NFC card
            
        Returns:
            (success: bool, message: str)
        """
        try:
            # Read card UID
            success, uid, msg = self.read_card_uid(timeout=30)
            
            if not success:
                return False, msg
            
            # Check if card already assigned
            existing = self._find_patient_by_card(uid)
            if existing:
                return False, f"Card already assigned to {existing.get('full_name')}"
            
            # Get patient
            patient = patient_manager.get_patient_by_id(national_id)
            if not patient:
                return False, "Patient not found"
            
            # Update patient record
            patient['nfc_card_uid'] = uid
            patient['nfc_card_assigned'] = True
            patient['nfc_card_assignment_date'] = datetime.now().strftime("%Y-%m-%d")
            patient['nfc_card_type'] = card_type
            patient['nfc_card_status'] = 'active'
            
            patient_manager.update_patient(national_id, patient)
            
            # Log event
            log_hardware_event(
                event_type='nfc_card_assignment',
                patient_national_id=national_id,
                card_uid=uid,
                success=True
            )
            
            return True, f"Card {uid} assigned successfully to {patient.get('full_name')}"
            
        except Exception as e:
            return False, f"Assignment error: {str(e)}"
    
    def get_patient_from_card(self, timeout: int = 10) -> Tuple[bool, Optional[dict], str]:
        """
        Read card and return patient data
        
        Args:
            timeout: Seconds to wait for card
            
        Returns:
            (success: bool, patient_data: dict or None, message: str)
        """
        try:
            # Read card
            success, uid, msg = self.read_card_uid(timeout)
            
            if not success:
                return False, None, msg
            
            # Find patient
            patient = self._find_patient_by_card(uid)
            
            if not patient:
                log_hardware_event(
                    event_type='nfc_card_scan',
                    card_uid=uid,
                    success=False,
                    error='Card not assigned'
                )
                return False, None, "Card not assigned to any patient"
            
            # Log successful access
            log_hardware_event(
                event_type='nfc_card_scan',
                patient_national_id=patient.get('national_id'),
                card_uid=uid,
                success=True
            )
            
            return True, patient, f"Patient: {patient.get('full_name')}"
            
        except Exception as e:
            return False, None, f"Error: {str(e)}"
    
    def unassign_card(self, national_id: str) -> Tuple[bool, str]:
        """
        Remove card assignment from patient
        
        Args:
            national_id: Patient's National ID
            
        Returns:
            (success: bool, message: str)
        """
        try:
            patient = patient_manager.get_patient_by_id(national_id)
            if not patient:
                return False, "Patient not found"
            
            if not patient.get('nfc_card_assigned'):
                return False, "Patient has no assigned card"
            
            old_uid = patient.get('nfc_card_uid')
            
            # Update patient record
            patient['nfc_card_uid'] = None
            patient['nfc_card_assigned'] = False
            patient['nfc_card_status'] = 'unassigned'
            
            patient_manager.update_patient(national_id, patient)
            
            # Log event
            log_hardware_event(
                event_type='nfc_card_unassignment',
                patient_national_id=national_id,
                card_uid=old_uid,
                success=True
            )
            
            return True, "Card unassigned successfully"
            
        except Exception as e:
            return False, f"Unassignment error: {str(e)}"
    
    def mark_card_lost(self, national_id: str) -> Tuple[bool, str]:
        """Mark card as lost (for security)"""
        try:
            patient = patient_manager.get_patient_by_id(national_id)
            if patient and patient.get('nfc_card_assigned'):
                patient['nfc_card_status'] = 'lost'
                patient_manager.update_patient(national_id, patient)
                
                log_hardware_event(
                    event_type='nfc_card_lost',
                    patient_national_id=national_id,
                    card_uid=patient.get('nfc_card_uid'),
                    success=True
                )
                
                return True, "Card marked as lost"
            return False, "No assigned card found"
        except Exception as e:
            return False, str(e)
    
    # Private helpers
    def _is_valid_uid(self, uid: str) -> bool:
        """Validate UID format"""
        # UID should be hexadecimal, 8-20 characters
        if not uid:
            return False
        
        try:
            int(uid, 16)
            return 4 <= len(uid) <= 20
        except ValueError:
            return False
    
    def _find_patient_by_card(self, uid: str) -> Optional[dict]:
        """Find patient with given card UID"""
        patients = patient_manager.get_all_patients()
        
        for patient in patients:
            if patient.get('nfc_card_uid') == uid and patient.get('nfc_card_status') == 'active':
                return patient
        
        return None


# Global instance
nfc_manager = NFCManager()