"""
ENHANCED QR Code Generation for Emergency Cards - Phase 12
Includes critical emergency data in QR code for faster emergency response

Location: utils/qr_generator.py (REPLACE ENTIRE FILE)
"""
import qrcode
from PIL import Image
import io
import json


def generate_qr_code(data: str, size: int = 200) -> Image.Image:
    """
    Generate QR code image
    
    Args:
        data: Data to encode in QR code
        size: Size of QR code image in pixels
    
    Returns:
        PIL Image object
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Resize to requested size
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    
    return img


def generate_patient_qr(national_id: str) -> Image.Image:
    """
    Generate QR code for patient National ID (Basic version)
    
    Args:
        national_id: Patient's National ID
    
    Returns:
        PIL Image with QR code
    """
    # Format: MEDLINK:ID:national_id
    data = f"MEDLINK:ID:{national_id}"
    return generate_qr_code(data, size=150)


def generate_patient_qr_enhanced(patient_data: dict) -> Image.Image:
    """
    Generate ENHANCED QR code with critical emergency data - Phase 12
    
    Includes:
    - Patient ID and basic info
    - Blood type
    - Critical allergies
    - DNR status
    - Chronic conditions
    - Emergency contact
    - Disability info
    
    Args:
        patient_data: Complete patient dictionary
    
    Returns:
        PIL Image with QR code containing emergency data
    """
    # Build emergency data package
    emergency_data = {
        'v': '2.0',  # Version 2.0 - Enhanced
        'id': patient_data.get('national_id', ''),
        'name': patient_data.get('full_name', ''),
        'age': patient_data.get('age', ''),
        'gender': patient_data.get('gender', ''),
        'blood': patient_data.get('blood_type', ''),
    }
    
    # Add allergies (critical!)
    allergies = patient_data.get('allergies', [])
    if allergies:
        # Limit to first 3 most critical
        emergency_data['allergies'] = allergies[:3]
    
    # Add DNR status (CRITICAL!)
    directives = patient_data.get('emergency_directives', {})
    if directives:
        dnr_status = directives.get('dnr_status', False)
        if dnr_status:
            emergency_data['dnr'] = True
            dnr_date = directives.get('dnr_date', '')
            if dnr_date:
                emergency_data['dnr_date'] = dnr_date
        
        # Organ donor status
        if directives.get('organ_donor', False):
            emergency_data['donor'] = True
    
    # Add top chronic conditions
    chronic = patient_data.get('chronic_diseases', [])
    if chronic:
        # Limit to first 3
        emergency_data['chronic'] = chronic[:3]
    
    # Add emergency contact
    emergency_contact = patient_data.get('emergency_contact', {})
    if emergency_contact:
        emergency_data['contact'] = {
            'name': emergency_contact.get('name', ''),
            'phone': emergency_contact.get('phone', ''),
            'relation': emergency_contact.get('relation', '')
        }
    
    # Add disability info (critical for care)
    disabilities_info = patient_data.get('disabilities_special_needs', {})
    if disabilities_info and disabilities_info.get('has_disability', False):
        emergency_data['disability'] = {
            'type': disabilities_info.get('disability_type', ''),
            'aids': disabilities_info.get('mobility_aids', [])[:2]  # First 2 aids
        }
        
        # Communication needs (critical!)
        comm_needs = disabilities_info.get('communication_needs', [])
        if comm_needs:
            emergency_data['disability']['comm'] = comm_needs[:2]
    
    # Add recent major surgery if any
    surgeries = patient_data.get('surgeries', [])
    if surgeries:
        # Get most recent surgery
        recent_surgery = sorted(surgeries, key=lambda x: x.get('date', ''), reverse=True)[0]
        emergency_data['recent_surgery'] = {
            'procedure': recent_surgery.get('procedure', '')[:30],  # Truncate
            'date': recent_surgery.get('date', '')
        }
    
    # Convert to compact JSON
    json_data = json.dumps(emergency_data, separators=(',', ':'))
    
    # Create QR code with emergency data
    # Format: MEDLINK:EMERGENCY:json_data
    qr_data = f"MEDLINK:EMERGENCY:{json_data}"
    
    return generate_qr_code(qr_data, size=150)


def qr_to_bytes(qr_image: Image.Image) -> bytes:
    """
    Convert QR code image to bytes
    
    Args:
        qr_image: PIL Image
    
    Returns:
        Image bytes
    """
    img_byte_arr = io.BytesIO()
    qr_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()


def decode_emergency_qr(qr_text: str) -> dict:
    """
    Decode emergency QR code data
    
    Usage: When scanning QR codes in emergency situations
    
    Args:
        qr_text: Text extracted from QR code
    
    Returns:
        Dictionary with patient emergency data
    """
    try:
        if qr_text.startswith("MEDLINK:EMERGENCY:"):
            json_part = qr_text.replace("MEDLINK:EMERGENCY:", "")
            return json.loads(json_part)
        elif qr_text.startswith("MEDLINK:ID:"):
            # Old format - just ID
            national_id = qr_text.replace("MEDLINK:ID:", "")
            return {'id': national_id, 'v': '1.0'}
        else:
            return {'error': 'Invalid QR code format'}
    except Exception as e:
        return {'error': str(e)}