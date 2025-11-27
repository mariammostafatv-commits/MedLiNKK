"""
Fingerprint authentication manager for R307 sensor
"""
import serial
from datetime import datetime
import struct
from typing import Optional, Tuple
from config.hardware_config import FINGERPRINT_CONFIG
from core.data_manager import data_manager
from utils.logger import log_hardware_event


class FingerprintManager:
    """Manages R307 fingerprint sensor operations"""

    # R307 Command Packets
    ADDR = 0xFFFFFFFF
    CMD_HANDSHAKE = 0x01
    CMD_GEN_IMG = 0x01
    CMD_IMG_2_TZ = 0x02
    CMD_MATCH = 0x03
    CMD_SEARCH = 0x04
    CMD_REG_MODEL = 0x05
    CMD_STORE = 0x06
    CMD_LOAD = 0x07
    CMD_DELETE = 0x0C
    CMD_EMPTY = 0x0D
    CMD_GET_COUNT = 0x1D

    def __init__(self):
        self.port = FINGERPRINT_CONFIG['port']
        self.baudrate = FINGERPRINT_CONFIG['baudrate']
        self.ser = None
        self.is_connected = False

    def connect(self) -> Tuple[bool, str]:
        """
        Connect to R307 fingerprint sensor

        Returns:
            (success: bool, message: str)
        """
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=FINGERPRINT_CONFIG['timeout']
            )

            # Send handshake
            if self._send_command(self.CMD_HANDSHAKE):
                self.is_connected = True
                return True, "Fingerprint sensor connected successfully"
            else:
                return False, "Handshake failed - sensor not responding"

        except serial.SerialException as e:
            return False, f"Connection error: {str(e)}"

    def disconnect(self):
        """Disconnect from sensor"""
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.is_connected = False

    def enroll_fingerprint(self, user_id: str, user_name: str) -> Tuple[bool, str, Optional[int]]:
        """
        Enroll new fingerprint for user

        Args:
            user_id: User ID
            user_name: User display name

        Returns:
            (success: bool, message: str, fingerprint_id: int or None)
        """
        if not self.is_connected:
            success, msg = self.connect()
            if not success:
                return False, msg, None

        try:
            # Find next available slot
            next_id = self._get_next_available_id()
            if next_id is None:
                return False, "No available fingerprint slots", None

            # Step 1: Capture first image
            print(f"Place {user_name}'s finger on sensor...")
            if not self._capture_image():
                return False, "Failed to capture first image", None

            if not self._generate_template(buffer=1):
                return False, "Failed to generate first template", None

            print("Remove finger and place again...")
            import time
            time.sleep(2)

            # Step 2: Capture second image
            if not self._capture_image():
                return False, "Failed to capture second image", None

            if not self._generate_template(buffer=2):
                return False, "Failed to generate second template", None

            # Step 3: Create model from both templates
            if not self._create_model():
                return False, "Templates do not match", None

            # Step 4: Store model
            if not self._store_template(next_id):
                return False, "Failed to store template", None

            # Step 5: Update database
            user = data_manager.find_item('users', 'users', 'user_id', user_id)
            if user:
                user['fingerprint_id'] = next_id
                user['fingerprint_enrolled'] = True
                user['fingerprint_enrollment_date'] = datetime.now().strftime(
                    "%Y-%m-%d")

                data_manager.update_item(
                    'users', 'users', user_id, 'user_id', user)

            # Log event
            log_hardware_event(
                event_type='fingerprint_enrollment',
                user_id=user_id,
                fingerprint_id=next_id,
                success=True
            )

            return True, f"Fingerprint enrolled successfully at position {next_id}", next_id

        except Exception as e:
            return False, f"Enrollment error: {str(e)}", None

    def authenticate_fingerprint(self) -> Tuple[bool, Optional[dict], str]:
        """
        Authenticate user by fingerprint scan

        Returns:
            (success: bool, user_data: dict or None, message: str)
        """
        if not self.is_connected:
            success, msg = self.connect()
            if not success:
                return False, None, msg

        try:
            print("Place finger on sensor...")

            # Capture image
            if not self._capture_image():
                return False, None, "Failed to capture fingerprint"

            # Generate template
            if not self._generate_template(buffer=1):
                return False, None, "Failed to generate template"

            # Search for match
            finger_id, confidence = self._search_fingerprint()

            if finger_id == -1:
                log_hardware_event(
                    event_type='fingerprint_login',
                    fingerprint_id=None,
                    success=False
                )
                return False, None, "Fingerprint not recognized"

            # Find user with this fingerprint ID
            users = data_manager.load_data('users')
            for user in users.get('users', []):
                if user.get('fingerprint_id') == finger_id:
                    # Log successful authentication
                    log_hardware_event(
                        event_type='fingerprint_login',
                        user_id=user['user_id'],
                        fingerprint_id=finger_id,
                        success=True,
                        confidence=confidence
                    )

                    # Update last login
                    user['last_fingerprint_login'] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S")
                    data_manager.update_item(
                        'users', 'users', user['user_id'], 'user_id', user)

                    return True, user, f"Welcome {user['full_name']}! (Confidence: {confidence}%)"

            return False, None, "Fingerprint found but user not in database"

        except Exception as e:
            return False, None, f"Authentication error: {str(e)}"

    def delete_fingerprint(self, user_id: str) -> Tuple[bool, str]:
        """
        Delete user's fingerprint from sensor

        Args:
            user_id: User ID

        Returns:
            (success: bool, message: str)
        """
        try:
            user = data_manager.find_item('users', 'users', 'user_id', user_id)
            if not user or not user.get('fingerprint_enrolled'):
                return False, "User has no enrolled fingerprint"

            finger_id = user.get('fingerprint_id')

            # Delete from sensor
            if not self._delete_template(finger_id):
                return False, "Failed to delete from sensor"

            # Update database
            user['fingerprint_id'] = None
            user['fingerprint_enrolled'] = False
            data_manager.update_item(
                'users', 'users', user_id, 'user_id', user)

            # Log event
            log_hardware_event(
                event_type='fingerprint_deletion',
                user_id=user_id,
                fingerprint_id=finger_id,
                success=True
            )

            return True, "Fingerprint deleted successfully"

        except Exception as e:
            return False, f"Deletion error: {str(e)}"

    # Private helper methods
    def _send_command(self, cmd: int, data: bytes = b'') -> bool:
        """Send command packet to sensor"""
        # Implementation details...
        pass

    def _capture_image(self) -> bool:
        """Capture fingerprint image"""
        # Implementation details...
        pass

    def _generate_template(self, buffer: int) -> bool:
        """Generate template from image"""
        # Implementation details...
        pass

    def _create_model(self) -> bool:
        """Create model from templates"""
        # Implementation details...
        pass

    def _store_template(self, position: int) -> bool:
        """Store template at position"""
        # Implementation details...
        pass

    def _search_fingerprint(self) -> Tuple[int, int]:
        """
        Search for fingerprint match
        Returns: (finger_id, confidence_score)
        """
        # Implementation details...
        pass

    def _delete_template(self, position: int) -> bool:
        """Delete template at position"""
        # Implementation details...
        pass

    def _get_next_available_id(self) -> Optional[int]:
        """Find next available fingerprint slot"""
        users = data_manager.load_data('users')
        used_ids = set()

        for user in users.get('users', []):
            if user.get('fingerprint_enrolled'):
                used_ids.add(user.get('fingerprint_id'))

        for i in range(1, FINGERPRINT_CONFIG['max_templates'] + 1):
            if i not in used_ids:
                return i

        return None


# Global instance
fingerprint_manager = FingerprintManager()
