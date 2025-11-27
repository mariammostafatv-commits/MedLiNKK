"""
Hardware event logging system
"""
from datetime import datetime
from pathlib import Path
from core.data_manager import data_manager
import socket


def log_hardware_event(
    event_type: str,
    user_id: str = None,
    patient_national_id: str = None,
    fingerprint_id: int = None,
    card_uid: str = None,
    success: bool = True,
    error: str = None,
    **kwargs
) -> bool:
    """
    Log hardware access event

    Args:
        event_type: Type of event (fingerprint_login, nfc_card_scan, etc.)
        user_id: User ID if applicable
        patient_national_id: Patient ID if applicable
        fingerprint_id: Fingerprint template ID
        card_uid: NFC card UID
        success: Whether operation succeeded
        error: Error message if failed
        **kwargs: Additional event data

    Returns:
        Success boolean
    """
    try:
        # Create event record
        event = {
            'event_id': generate_event_id(),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'event_type': event_type,
            'success': success
        }

        # Add optional fields
        if user_id:
            event['user_id'] = user_id
        if patient_national_id:
            event['patient_national_id'] = patient_national_id
        if fingerprint_id:
            event['fingerprint_id'] = fingerprint_id
        if card_uid:
            event['card_uid'] = card_uid
        if error:
            event['error'] = error

        # Add system information
        event['ip_address'] = get_local_ip()
        event['device_name'] = socket.gethostname()

        # Add extra kwargs
        event.update(kwargs)

        # Save to audit log
        log_data = data_manager.load_data('hardware_audit_log')
        if 'hardware_events' not in log_data:
            log_data['hardware_events'] = []

        log_data['hardware_events'].append(event)

        # Keep only last 10,000 events (prevent unlimited growth)
        if len(log_data['hardware_events']) > 10000:
            log_data['hardware_events'] = log_data['hardware_events'][-10000:]

        return data_manager.save_data('hardware_audit_log', log_data)

    except Exception as e:
        print(f"Failed to log hardware event: {e}")
        return False


def generate_event_id() -> str:
    """Generate unique event ID"""
    import uuid
    return f"HW{uuid.uuid4().hex[:8].upper()}"


def get_local_ip() -> str:
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def get_hardware_audit_log(
    event_type: str = None,
    user_id: str = None,
    patient_national_id: str = None,
    start_date: str = None,
    end_date: str = None,
    limit: int = 100
) -> list:
    """
    Query hardware audit log

    Args:
        event_type: Filter by event type
        user_id: Filter by user
        patient_national_id: Filter by patient
        start_date: Filter by start date
        end_date: Filter by end date
        limit: Max results

    Returns:
        List of events
    """
    log_data = data_manager.load_data('hardware_audit_log')
    events = log_data.get('hardware_events', [])

    # Apply filters
    filtered = events

    if event_type:
        filtered = [e for e in filtered if e.get('event_type') == event_type]

    if user_id:
        filtered = [e for e in filtered if e.get('user_id') == user_id]

    if patient_national_id:
        filtered = [e for e in filtered if e.get(
            'patient_national_id') == patient_national_id]

    if start_date:
        filtered = [e for e in filtered if e.get(
            'timestamp', '') >= start_date]

    if end_date:
        filtered = [e for e in filtered if e.get('timestamp', '') <= end_date]

    # Sort by timestamp (newest first)
    filtered.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

    return filtered[:limit]
