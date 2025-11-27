"""
Hardware configuration for MedLink
"""

# Fingerprint Sensor (R307) Configuration
FINGERPRINT_CONFIG = {
    'enabled': True,
    'port': 'COM3',                    # Adjust based on system
    'baudrate': 57600,
    'address': 0xFFFFFFFF,
    'password': 0x00000000,
    'max_templates': 1000,
    'timeout': 5                       # seconds
}

# NFC Reader (R20C) Configuration
NFC_CONFIG = {
    'enabled': True,
    'port': 'COM4',                    # Adjust based on system
    'baudrate': 9600,
    'mode': 'serial',                  # 'serial' or 'keyboard'
    'timeout': 2
}

# Security Settings
HARDWARE_SECURITY = {
    'require_fingerprint_for_sensitive_actions': True,
    'nfc_scan_timeout': 30,            # seconds to wait for card tap
    'fingerprint_max_attempts': 3,
    'log_all_hardware_access': True,
    'encrypt_hardware_logs': True
}
