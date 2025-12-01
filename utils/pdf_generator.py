"""
Enhanced PDF generation for emergency cards with Phase 8 comprehensive data
Includes: surgeries, hospitalizations, disabilities, DNR status, organ donor, vaccinations
Location: utils/pdf_generator_enhanced.py
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from utils.qr_generator import generate_patient_qr, qr_to_bytes
import io


def generate_emergency_card_enhanced(patient_data: dict, output_path: str) -> bool:
    """
    Generate comprehensive emergency card PDF with Phase 8 data

    Args:
        patient_data: Complete patient information dictionary
        output_path: Path to save PDF

    Returns:
        Success boolean
    """
    try:
        # Create PDF
        pdf = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter

        # ========================================
        # HEADER - Red Emergency Banner
        # ========================================
        pdf.setFillColorRGB(0.93, 0.26, 0.26)  # Red
        pdf.rect(0, height - 2*inch, width, 2*inch, fill=True, stroke=False)

        # Title
        pdf.setFillColorRGB(1, 1, 1)  # White text
        pdf.setFont("Helvetica-Bold", 32)
        pdf.drawCentredString(width/2, height - 1*inch, "🆘 EMERGENCY CARD")

        pdf.setFont("Helvetica", 14)
        pdf.drawCentredString(width/2, height - 1.5*inch,
                              "Medical Records System - Comprehensive Profile")

        # ========================================
        # PATIENT NAME - Large and Bold
        # ========================================
        y_position = height - 2.5*inch

        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 24)
        pdf.drawString(1*inch, y_position,
                       patient_data.get('full_name', 'N/A'))

        y_position -= 0.4*inch

        # ========================================
        # CRITICAL INFORMATION BOX
        # ========================================
        pdf.setFillColorRGB(1, 0.95, 0.95)  # Light red background
        pdf.roundRect(1*inch, y_position - 2.2*inch, width -
                      2*inch, 2.3*inch, 0.15*inch, fill=True)

        pdf.setFillColorRGB(0, 0, 0)

        # Blood Type - LARGE
        pdf.setFont("Helvetica-Bold", 18)
        blood_type = patient_data.get('blood_type', 'Unknown')
        pdf.drawString(1.2*inch, y_position - 0.3*inch, "🩸 Blood Type:")

        pdf.setFillColorRGB(0.8, 0, 0)  # Red text
        pdf.setFont("Helvetica-Bold", 32)
        pdf.drawString(3.5*inch, y_position - 0.45*inch, blood_type)

        pdf.setFillColorRGB(0, 0, 0)
        y_position -= 0.8*inch

        # Age and Gender
        pdf.setFont("Helvetica", 12)
        age = patient_data.get('age', 'N/A')
        gender = patient_data.get('gender', 'N/A')
        pdf.drawString(1.2*inch, y_position,
                       f"Age: {age} | Gender: {gender}")

        y_position -= 0.25*inch

        # National ID
        pdf.drawString(1.2*inch, y_position,
                       f"National ID: {patient_data.get('national_id', 'N/A')}")

        y_position -= 0.4*inch

        # ========================================
        # ALLERGIES - Highlighted
        # ========================================
        allergies = patient_data.get('allergies', [])
        if allergies:
            pdf.setFont("Helvetica-Bold", 14)
            pdf.setFillColorRGB(0.8, 0, 0)  # Red
            pdf.drawString(1.2*inch, y_position, "⚠️  ALLERGIES:")

            pdf.setFont("Helvetica-Bold", 12)
            pdf.setFillColorRGB(0.6, 0, 0)
            allergies_text = ", ".join(allergies)
            pdf.drawString(1.2*inch, y_position - 0.25*inch, allergies_text)

            y_position -= 0.6*inch
        else:
            pdf.setFont("Helvetica", 11)
            pdf.drawString(1.2*inch, y_position, "⚠️  No known allergies")
            y_position -= 0.35*inch

        # ========================================
        # CHRONIC DISEASES
        # ========================================
        chronic = patient_data.get('chronic_diseases', [])
        if chronic:
            pdf.setFont("Helvetica-Bold", 12)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(1.2*inch, y_position, "🏥 Chronic Conditions:")

            pdf.setFont("Helvetica", 11)
            pdf.drawString(1.2*inch, y_position - 0.25*inch,
                           ", ".join(chronic))

            y_position -= 0.5*inch

        y_position -= 0.2*inch

        # ========================================
        # PHASE 8: EMERGENCY DIRECTIVES
        # ========================================
        directives = patient_data.get('emergency_directives', {})

        # DNR Status
        if directives.get('dnr_status'):
            pdf.setFillColorRGB(1, 0.9, 0.9)  # Very light red
            pdf.roundRect(1*inch, y_position - 0.55*inch, 3 *
                          inch, 0.6*inch, 0.1*inch, fill=True)

            pdf.setFillColorRGB(0.8, 0, 0)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(1.2*inch, y_position - 0.25*inch,
                           "⛔ DNR (DO NOT RESUSCITATE)")

            dnr_date = directives.get('dnr_date', 'Date not specified')
            pdf.setFont("Helvetica", 9)
            pdf.drawString(1.2*inch, y_position - 0.45 *
                           inch, f"Date: {dnr_date}")

            y_position -= 0.75*inch

        # Organ Donor Status
        if directives.get('organ_donor'):
            pdf.setFillColorRGB(0.9, 1, 0.9)  # Light green
            pdf.roundRect(1*inch, y_position - 0.45*inch, 2.5 *
                          inch, 0.5*inch, 0.1*inch, fill=True)

            pdf.setFillColorRGB(0, 0.5, 0)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(1.2*inch, y_position - 0.3*inch, "💚 ORGAN DONOR")

            y_position -= 0.65*inch

        # Religious Preferences
        religious = directives.get('religious_preferences', {})
        if religious.get('religion') or religious.get('special_considerations'):
            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(1*inch, y_position, "🕌 Religious Considerations:")

            pdf.setFont("Helvetica", 10)
            if religious.get('religion'):
                pdf.drawString(1.2*inch, y_position - 0.25*inch,
                               f"Religion: {religious['religion']}")

            if religious.get('special_considerations'):
                considerations = religious['special_considerations']
                if len(considerations) > 60:
                    considerations = considerations[:57] + "..."
                pdf.drawString(1.2*inch, y_position -
                               0.45*inch, considerations)
                y_position -= 0.65*inch
            else:
                y_position -= 0.4*inch

        # ========================================
        # PHASE 8: DISABILITIES / SPECIAL NEEDS
        # ========================================
        disability_info = patient_data.get('disabilities_special_needs', {})

        if disability_info.get('has_disability'):
            pdf.setFillColorRGB(0.95, 0.95, 1)  # Light blue
            pdf.roundRect(1*inch, y_position - 0.9*inch, width -
                          2*inch, 1*inch, 0.1*inch, fill=True)

            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(1.2*inch, y_position - 0.25*inch,
                           "♿ Disability / Special Needs:")

            pdf.setFont("Helvetica", 10)

            if disability_info.get('disability_type'):
                pdf.drawString(1.2*inch, y_position - 0.45*inch,
                               f"Type: {disability_info['disability_type']}")

            # Communication needs
            if disability_info.get('communication_needs'):
                needs_text = ", ".join(
                    disability_info['communication_needs'][:3])
                pdf.drawString(1.2*inch, y_position - 0.65*inch,
                               f"Communication: {needs_text}")

            # Accessibility requirements
            if disability_info.get('accessibility_requirements'):
                access_text = ", ".join(
                    disability_info['accessibility_requirements'][:3])
                pdf.drawString(1.2*inch, y_position - 0.85*inch,
                               f"Accessibility: {access_text}")

            y_position -= 1.1*inch

        # ========================================
        # CURRENT MEDICATIONS
        # ========================================
        medications = patient_data.get('current_medications', [])
        if medications:
            pdf.setFillColorRGB(0.95, 0.98, 1)  # Very light blue
            pdf.roundRect(1*inch, y_position - (0.3*inch + len(medications[:4]) * 0.25*inch),
                          width - 2*inch, 0.4*inch +
                          len(medications[:4]) * 0.25*inch,
                          0.1*inch, fill=True)

            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(1.2*inch, y_position - 0.2 *
                           inch, "💊 Current Medications:")

            pdf.setFont("Helvetica", 9)
            for i, med in enumerate(medications[:4]):  # Show max 4
                med_text = f"{med.get('name', 'N/A')} - {med.get(
                    'dosage', '')} {med.get('frequency', '')}"
                pdf.drawString(1.2*inch, y_position -
                               (0.4 + i * 0.25)*inch, med_text)

            y_position -= (0.5 + len(medications[:4]) * 0.25)*inch

        # ========================================
        # PHASE 8: RECENT SURGERIES
        # ========================================
        surgeries = patient_data.get('surgeries', [])
        if surgeries:
            # Show most recent surgery
            recent_surgery = sorted(
                surgeries, key=lambda x: x.get('date', ''), reverse=True)[0]

            pdf.setFillColorRGB(1, 0.98, 0.95)  # Light orange
            pdf.roundRect(1*inch, y_position - 0.7*inch, width -
                          2*inch, 0.8*inch, 0.1*inch, fill=True)

            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(1.2*inch, y_position - 0.2 *
                           inch, "🏥 Recent Surgery:")

            pdf.setFont("Helvetica", 10)
            pdf.drawString(1.2*inch, y_position - 0.4*inch,
                           f"{recent_surgery.get('procedure', 'N/A')} - {recent_surgery.get('date', 'N/A')}")
            pdf.drawString(1.2*inch, y_position - 0.6*inch,
                           f"Hospital: {recent_surgery.get('hospital', 'N/A')}")

            y_position -= 0.9*inch

        # ========================================
        # PHASE 8: RECENT HOSPITALIZATION
        # ========================================
        hospitalizations = patient_data.get('hospitalizations', [])
        if hospitalizations:
            # Show most recent hospitalization
            recent_hosp = sorted(hospitalizations, key=lambda x: x.get(
                'admission_date', ''), reverse=True)[0]

            pdf.setFillColorRGB(0.98, 0.95, 1)  # Light purple
            pdf.roundRect(1*inch, y_position - 0.7*inch, width -
                          2*inch, 0.8*inch, 0.1*inch, fill=True)

            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(1.2*inch, y_position - 0.2*inch,
                           "🏥 Recent Hospitalization:")

            pdf.setFont("Helvetica", 10)
            pdf.drawString(1.2*inch, y_position - 0.4*inch,
                           f"{recent_hosp.get('reason', 'N/A')}")
            pdf.drawString(1.2*inch, y_position - 0.6*inch,
                           f"{recent_hosp.get('admission_date', 'N/A')} to {recent_hosp.get('discharge_date', 'N/A')}")

            y_position -= 0.9*inch

        # ========================================
        # EMERGENCY CONTACT
        # ========================================
        emergency = patient_data.get('emergency_contact', {})
        if emergency:
            pdf.setFillColorRGB(0.95, 0.98, 1)
            pdf.roundRect(1*inch, y_position - 0.9*inch, width -
                          2*inch, 1*inch, 0.1*inch, fill=True)

            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(1.2*inch, y_position - 0.2 *
                           inch, "📞 Emergency Contact:")

            pdf.setFont("Helvetica", 11)
            pdf.drawString(1.2*inch, y_position - 0.45*inch,
                           f"{emergency.get('name', 'N/A')} ({emergency.get('relation', 'N/A')})")
            pdf.drawString(1.2*inch, y_position - 0.7*inch,
                           f"Phone: {emergency.get('phone', 'N/A')}")

            y_position -= 1.2*inch

        # ========================================
        # QR CODE
        # ========================================
        try:
            qr_img = generate_patient_qr(patient_data.get('national_id', ''))
            qr_bytes = qr_to_bytes(qr_img)

            # Draw QR code
            pdf.drawImage(RLImage(io.BytesIO(qr_bytes), width=1.5*inch, height=1.5*inch),
                          width - 2.5*inch, 0.8*inch, width=1.5*inch, height=1.5*inch,
                          preserveAspectRatio=True, mask='auto')

            pdf.setFont("Helvetica", 8)
            pdf.setFillColorRGB(0.5, 0.5, 0.5)
            pdf.drawCentredString(width - 1.75*inch, 0.5 *
                                  inch, "Scan for full records")
        except Exception as e:
            print(f"QR code generation error: {e}")

        # ========================================
        # FOOTER
        # ========================================
        pdf.setFont("Helvetica", 8)
        pdf.setFillColorRGB(0.5, 0.5, 0.5)
        pdf.drawString(
            1*inch, 0.5*inch, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        pdf.drawCentredString(
            width/2, 0.3*inch, "MedLink - Unified Medical Records System")

        # Instructions at bottom
        pdf.setFont("Helvetica-Bold", 9)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(1*inch, 0.15*inch,
                       "⚠️ KEEP THIS CARD WITH YOU AT ALL TIMES - Updated with comprehensive medical profile")

        # Save PDF
        pdf.save()
        return True

    except Exception as e:
        print(f"Error generating enhanced emergency card: {e}")
        import traceback
        traceback.print_exc()
        return False


# Keep original function for backward compatibility
def generate_emergency_card(patient_data: dict, output_path: str) -> bool:
    """
    Wrapper function - calls enhanced version
    Maintains backward compatibility
    """
    return generate_emergency_card_enhanced(patient_data, output_path)
