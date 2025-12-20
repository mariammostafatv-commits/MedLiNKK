"""
ENHANCED MEDICAL EMERGENCY CARD - Phase 12
Professional medical-grade emergency card with comprehensive information
Includes: DNR status, surgeries, disabilities, hospitalizations, family history

Location: utils/pdf_generator.py (REPLACE ENTIRE FILE)
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
from utils.qr_generator import generate_patient_qr_enhanced
import io


def generate_emergency_card(patient_data: dict, output_path: str) -> bool:
    """
    Generate professional medical-grade emergency card - ENHANCED
    
    NEW IN PHASE 12:
    - DNR status banner (if active)
    - Recent surgeries section
    - Disabilities and accessibility needs
    - Recent hospitalizations
    - Family history risk factors
    - Enhanced QR code with emergency data
    
    Design Features:
    - Large critical info (blood type, allergies)
    - Color-coded sections
    - Clear visual hierarchy
    - Professional medical aesthetic
    - Easy to read in emergency situations
    """
    try:
        pdf = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        
        # Professional medical colors
        EMERGENCY_RED = (0.85, 0.11, 0.14)      # Deep red
        DNR_PURPLE = (0.5, 0.0, 0.5)            # Purple for DNR
        CRITICAL_ORANGE = (1.0, 0.6, 0.0)       # Orange
        INFO_BLUE = (0.0, 0.45, 0.70)           # Medical blue
        SUCCESS_GREEN = (0.13, 0.55, 0.13)      # Green
        DARK_GRAY = (0.2, 0.2, 0.2)             # Almost black
        LIGHT_GRAY = (0.95, 0.95, 0.95)         # Very light gray
        WARNING_YELLOW = (1.0, 0.85, 0.0)       # Yellow for warnings
        
        y = height - 0.6*inch
        
        # ============================================
        # DNR STATUS BANNER - CRITICAL (Phase 12)
        # ============================================
        directives = patient_data.get('emergency_directives', {})
        dnr_status = directives.get('dnr_status', False) if directives else False
        
        if dnr_status:
            # VERY PROMINENT DNR BANNER
            pdf.setFillColorRGB(*DNR_PURPLE)
            pdf.rect(0, height - 0.9*inch, width, 0.9*inch, fill=True, stroke=False)
            
            pdf.setFillColorRGB(1, 1, 1)
            pdf.setFont("Helvetica-Bold", 32)
            pdf.drawCentredString(width/2, height - 0.55*inch, "⚠️ DNR - DO NOT RESUSCITATE ⚠️")
            
            # DNR date if available
            dnr_date = directives.get('dnr_date', '') if directives else ''
            if dnr_date:
                pdf.setFont("Helvetica", 12)
                pdf.drawCentredString(width/2, height - 0.75*inch, f"DNR Order Date: {dnr_date}")
            
            y = height - 1.1*inch
        else:
            # Standard emergency header
            pdf.setFillColorRGB(*EMERGENCY_RED)
            pdf.rect(0, height - 0.6*inch, width, 0.6*inch, fill=True, stroke=False)
            
            pdf.setFillColorRGB(1, 1, 1)
            pdf.setFont("Helvetica-Bold", 20)
            pdf.drawString(0.5*inch, height - 0.4*inch, "🚨 EMERGENCY MEDICAL CARD")
        
        # Generation date
        pdf.setFont("Helvetica", 10)
        pdf.setFillColorRGB(1, 1, 1)
        pdf.drawRightString(width - 0.5*inch, height - 0.4*inch, 
                           f"Generated: {datetime.now().strftime('%d %b %Y')}")
        
        y -= 0.2*inch
        
        # ============================================
        # PATIENT IDENTIFICATION
        # ============================================
        pdf.setFillColorRGB(*DARK_GRAY)
        pdf.setFont("Helvetica-Bold", 26)
        patient_name = patient_data.get('full_name', 'N/A').upper()
        pdf.drawString(0.5*inch, y, patient_name)
        
        y -= 0.35*inch
        
        # Basic info row
        pdf.setFont("Helvetica", 11)
        age = patient_data.get('age', 'N/A')
        gender = patient_data.get('gender', 'N/A')
        national_id = patient_data.get('national_id', 'N/A')
        
        pdf.drawString(0.5*inch, y, 
                      f"AGE: {age}  •  GENDER: {gender}  •  ID: {national_id}")
        
        y -= 0.5*inch
        
        # ============================================
        # CRITICAL SECTION 1: BLOOD TYPE
        # ============================================
        box_x = 0.5*inch
        box_width = 2.3*inch
        box_height = 1.3*inch
        
        # Blood type box - Red background
        pdf.setFillColorRGB(0.98, 0.85, 0.85)  # Light red
        pdf.setStrokeColorRGB(*EMERGENCY_RED)
        pdf.setLineWidth(3)
        pdf.roundRect(box_x, y - box_height, box_width, box_height, 
                     10, fill=True, stroke=True)
        
        # "BLOOD TYPE" label
        pdf.setFillColorRGB(*EMERGENCY_RED)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(box_x + 0.15*inch, y - 0.25*inch, "BLOOD TYPE")
        
        # Blood type value - HUGE
        pdf.setFont("Helvetica-Bold", 56)
        blood_type = patient_data.get('blood_type', '?')
        pdf.drawCentredString(box_x + box_width/2, y - 0.9*inch, blood_type)
        
        # ============================================
        # CRITICAL SECTION 2: ALLERGIES
        # ============================================
        allergies_x = 3*inch
        allergies_width = 4.5*inch
        
        allergies = patient_data.get('allergies', [])
        if allergies:
            # Allergies box - Orange background
            pdf.setFillColorRGB(1.0, 0.95, 0.85)  # Light orange
            pdf.setStrokeColorRGB(*CRITICAL_ORANGE)
            pdf.setLineWidth(3)
            pdf.roundRect(allergies_x, y - box_height, allergies_width, box_height,
                         10, fill=True, stroke=True)
            
            # "ALLERGIES" label
            pdf.setFillColorRGB(*CRITICAL_ORANGE)
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(allergies_x + 0.15*inch, y - 0.25*inch, "⚠️ ALLERGIES")
            
            # Allergies list
            pdf.setFont("Helvetica-Bold", 16)
            pdf.setFillColorRGB(0.8, 0.3, 0.0)
            
            if len(allergies) <= 3:
                for i, allergy in enumerate(allergies):
                    pdf.drawString(allergies_x + 0.15*inch, 
                                  y - 0.55*inch - (i * 0.25*inch), 
                                  f"• {allergy}")
            else:
                # Show first 3 + count
                for i in range(3):
                    pdf.drawString(allergies_x + 0.15*inch, 
                                  y - 0.55*inch - (i * 0.25*inch), 
                                  f"• {allergies[i]}")
                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(allergies_x + 0.15*inch, y - 1.05*inch,
                             f"+ {len(allergies)-3} more allergies")
        else:
            # No allergies box - Green
            pdf.setFillColorRGB(0.9, 0.98, 0.9)  # Light green
            pdf.setStrokeColorRGB(*SUCCESS_GREEN)
            pdf.setLineWidth(2)
            pdf.roundRect(allergies_x, y - box_height, allergies_width, box_height,
                         10, fill=True, stroke=True)
            
            pdf.setFillColorRGB(*SUCCESS_GREEN)
            pdf.setFont("Helvetica-Bold", 20)
            pdf.drawCentredString(allergies_x + allergies_width/2, y - 0.7*inch,
                                 "✓ NO KNOWN ALLERGIES")
        
        y -= box_height + 0.4*inch
        
        # ============================================
        # SECTION 3: DISABILITIES & ACCESSIBILITY (Phase 12)
        # ============================================
        disabilities_info = patient_data.get('disabilities_special_needs', {})
        has_disability = disabilities_info.get('has_disability', False) if disabilities_info else False
        
        if has_disability:
            disability_height = 0.9*inch
            pdf.setFillColorRGB(0.95, 0.95, 1.0)  # Light blue
            pdf.setStrokeColorRGB(*INFO_BLUE)
            pdf.setLineWidth(2)
            pdf.roundRect(0.5*inch, y - disability_height, 3.5*inch, disability_height,
                         8, fill=True, stroke=True)
            
            pdf.setFillColorRGB(*INFO_BLUE)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(0.65*inch, y - 0.22*inch, "♿ DISABILITIES & ACCESSIBILITY NEEDS")
            
            pdf.setFont("Helvetica", 10)
            pdf.setFillColorRGB(*DARK_GRAY)
            
            text_y = y - 0.45*inch
            
            # Disability type
            if disabilities_info.get('disability_type'):
                pdf.drawString(0.65*inch, text_y, f"Type: {disabilities_info['disability_type']}")
                text_y -= 0.18*inch
            
            # Mobility aids
            if disabilities_info.get('mobility_aids'):
                aids = disabilities_info['mobility_aids']
                if isinstance(aids, list) and aids:
                    pdf.drawString(0.65*inch, text_y, f"Aids: {', '.join(aids[:2])}")
                    text_y -= 0.18*inch
            
            # Communication needs
            if disabilities_info.get('communication_needs'):
                needs = disabilities_info['communication_needs']
                if isinstance(needs, list) and needs:
                    pdf.drawString(0.65*inch, text_y, f"Communication: {', '.join(needs[:2])}")
        
        # ============================================
        # SECTION 4: RECENT SURGERIES (Phase 12)
        # ============================================
        surgeries = patient_data.get('surgeries', [])
        recent_surgeries = sorted(surgeries, key=lambda x: x.get('date', ''), reverse=True)[:2]
        
        if recent_surgeries:
            surgery_height = 0.9*inch if len(recent_surgeries) == 1 else 1.3*inch
            surgery_x = 4.2*inch if has_disability else 0.5*inch
            surgery_width = 3.3*inch if has_disability else 7.0*inch
            
            pdf.setFillColorRGB(1.0, 0.95, 0.95)  # Light pink
            pdf.setStrokeColorRGB(*EMERGENCY_RED)
            pdf.setLineWidth(2)
            pdf.roundRect(surgery_x, y - surgery_height, surgery_width, surgery_height,
                         8, fill=True, stroke=True)
            
            pdf.setFillColorRGB(*EMERGENCY_RED)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(surgery_x + 0.15*inch, y - 0.22*inch, "🏥 RECENT SURGERIES")
            
            pdf.setFont("Helvetica", 9)
            pdf.setFillColorRGB(*DARK_GRAY)
            
            for i, surgery in enumerate(recent_surgeries):
                text_y = y - 0.45*inch - (i * 0.45*inch)
                procedure = surgery.get('procedure', 'Unknown')
                if len(procedure) > 35:
                    procedure = procedure[:32] + "..."
                date = surgery.get('date', 'N/A')
                
                pdf.setFont("Helvetica-Bold", 10)
                pdf.drawString(surgery_x + 0.15*inch, text_y, procedure)
                pdf.setFont("Helvetica", 9)
                pdf.drawString(surgery_x + 0.15*inch, text_y - 0.15*inch, 
                              f"Date: {date}")
                
                hospital = surgery.get('hospital', '')
                if hospital and len(hospital) > 30:
                    hospital = hospital[:27] + "..."
                if hospital:
                    pdf.drawString(surgery_x + 0.15*inch, text_y - 0.3*inch, 
                                  f"At: {hospital}")
        
        y -= max(disability_height if has_disability else 0, 
                 surgery_height if recent_surgeries else 0) + 0.4*inch
        
        # ============================================
        # SECTION 5: CHRONIC CONDITIONS
        # ============================================
        chronic = patient_data.get('chronic_diseases', [])
        if chronic:
            # Section header
            pdf.setFillColorRGB(*INFO_BLUE)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawString(0.5*inch, y, "CHRONIC CONDITIONS")
            
            y -= 0.05*inch
            pdf.setStrokeColorRGB(*INFO_BLUE)
            pdf.setLineWidth(2)
            pdf.line(0.5*inch, y, width - 0.5*inch, y)
            y -= 0.25*inch
            
            # Conditions in columns
            pdf.setFillColorRGB(*DARK_GRAY)
            pdf.setFont("Helvetica", 11)
            
            col1_x = 0.7*inch
            col2_x = 4.5*inch
            
            for i, condition in enumerate(chronic):
                if i < 4:  # First column
                    pdf.drawString(col1_x, y - (i * 0.25*inch), f"• {condition}")
                elif i < 8:  # Second column
                    pdf.drawString(col2_x, y - ((i-4) * 0.25*inch), f"• {condition}")
            
            if len(chronic) > 8:
                pdf.setFont("Helvetica-Oblique", 9)
                pdf.drawString(col1_x, y - 1.1*inch, f"+ {len(chronic)-8} more conditions")
            
            y -= max(1.2*inch, (min(len(chronic), 4) * 0.25*inch) + 0.3*inch)
        
        # ============================================
        # SECTION 6: FAMILY HISTORY RISK FACTORS (Phase 12)
        # ============================================
        family_history = patient_data.get('family_history', {})
        genetic_conditions = family_history.get('genetic_conditions', []) if family_history else []
        
        if genetic_conditions:
            risk_height = 0.6*inch
            pdf.setFillColorRGB(1.0, 0.98, 0.9)  # Light yellow
            pdf.setStrokeColorRGB(*WARNING_YELLOW)
            pdf.setLineWidth(2)
            pdf.roundRect(0.5*inch, y - risk_height, 3.5*inch, risk_height,
                         8, fill=True, stroke=True)
            
            pdf.setFillColorRGB(0.8, 0.6, 0.0)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(0.65*inch, y - 0.22*inch, "🧬 FAMILY HISTORY RISK FACTORS")
            
            pdf.setFont("Helvetica", 9)
            pdf.setFillColorRGB(*DARK_GRAY)
            
            # Show first 2 genetic conditions
            for i, condition in enumerate(genetic_conditions[:2]):
                if len(condition) > 40:
                    condition = condition[:37] + "..."
                pdf.drawString(0.65*inch, y - 0.42*inch - (i * 0.15*inch), f"• {condition}")
            
            if len(genetic_conditions) > 2:
                pdf.setFont("Helvetica-Oblique", 8)
                pdf.drawString(0.65*inch, y - 0.57*inch, f"+ {len(genetic_conditions)-2} more")
        
        # ============================================
        # SECTION 7: CURRENT MEDICATIONS
        # ============================================
        medications = patient_data.get('current_medications', [])
        if medications:
            med_x = 4.2*inch if genetic_conditions else 0.5*inch
            med_width = 3.3*inch if genetic_conditions else 7.0*inch
            
            # Section header
            pdf.setFillColorRGB(*INFO_BLUE)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(med_x, y, "CURRENT MEDICATIONS")
            
            y -= 0.05*inch
            pdf.setStrokeColorRGB(*INFO_BLUE)
            pdf.setLineWidth(1)
            pdf.line(med_x, y, med_x + med_width, y)
            y -= 0.2*inch
            
            # Medications table headers
            pdf.setFillColorRGB(*DARK_GRAY)
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawString(med_x + 0.2*inch, y, "MEDICATION")
            if genetic_conditions:
                pdf.drawString(med_x + 2.0*inch, y, "DOSAGE")
            else:
                pdf.drawString(med_x + 3.5*inch, y, "DOSAGE")
                pdf.drawString(med_x + 5.5*inch, y, "FREQUENCY")
            
            y -= 0.2*inch
            
            pdf.setFont("Helvetica", 9)
            for i, med in enumerate(medications[:5]):  # Show max 5
                if isinstance(med, dict):
                    med_name = med.get('name', 'Unknown')
                    dosage = med.get('dosage', '-')
                    frequency = med.get('frequency', '-')
                else:
                    med_name = str(med)
                    dosage = '-'
                    frequency = '-'
                
                # Truncate if too long
                if len(med_name) > 25:
                    med_name = med_name[:22] + "..."
                
                pdf.drawString(med_x + 0.2*inch, y, med_name)
                
                if genetic_conditions:
                    pdf.drawString(med_x + 2.0*inch, y, dosage)
                else:
                    pdf.drawString(med_x + 3.5*inch, y, dosage)
                    pdf.drawString(med_x + 5.5*inch, y, frequency)
                
                y -= 0.2*inch
            
            if len(medications) > 5:
                pdf.setFont("Helvetica-Oblique", 8)
                pdf.drawString(med_x + 0.2*inch, y - 0.1*inch, 
                              f"+ {len(medications)-5} more medications")
                y -= 0.2*inch
            
            y -= 0.3*inch
        
        # ============================================
        # SECTION 8: EMERGENCY CONTACT
        # ============================================
        emergency = patient_data.get('emergency_contact', {})
        if emergency:
            # Contact box - Blue background
            contact_height = 0.9*inch
            pdf.setFillColorRGB(0.9, 0.95, 1.0)  # Light blue
            pdf.setStrokeColorRGB(*INFO_BLUE)
            pdf.setLineWidth(2)
            pdf.roundRect(0.5*inch, y - contact_height, 4.5*inch, contact_height,
                         8, fill=True, stroke=True)
            
            # Header
            pdf.setFillColorRGB(*INFO_BLUE)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(0.65*inch, y - 0.25*inch, "EMERGENCY CONTACT")
            
            # Name and relation
            pdf.setFillColorRGB(*DARK_GRAY)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawString(0.65*inch, y - 0.5*inch, 
                          f"{emergency.get('name', 'N/A')} ({emergency.get('relation', 'N/A')})")
            
            # Phone - Large
            pdf.setFont("Helvetica-Bold", 16)
            pdf.setFillColorRGB(*INFO_BLUE)
            pdf.drawString(0.65*inch, y - 0.75*inch, 
                          f"📞 {emergency.get('phone', 'N/A')}")
        
        # ============================================
        # SECTION 9: ORGAN DONOR STATUS (Phase 12)
        # ============================================
        if directives:
            organ_donor = directives.get('organ_donor', False)
            
            if organ_donor:
                donor_height = 0.7*inch
                donor_x = 5.2*inch
                pdf.setFillColorRGB(0.9, 1.0, 0.9)  # Light green
                pdf.setStrokeColorRGB(*SUCCESS_GREEN)
                pdf.setLineWidth(2)
                pdf.roundRect(donor_x, y - donor_height, 2.8*inch, donor_height,
                             8, fill=True, stroke=True)
                
                pdf.setFillColorRGB(*SUCCESS_GREEN)
                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(donor_x + 0.15*inch, y - 0.25*inch, "💚 ORGAN DONOR")
                
                pdf.setFont("Helvetica", 10)
                pdf.setFillColorRGB(*DARK_GRAY)
                pdf.drawString(donor_x + 0.15*inch, y - 0.45*inch, "Registered organ donor")
                
                donor_card = directives.get('organ_donor_card_number', '')
                if donor_card:
                    pdf.setFont("Helvetica", 9)
                    pdf.drawString(donor_x + 0.15*inch, y - 0.6*inch, f"Card: {donor_card}")
        
        # ============================================
        # QR CODE - Enhanced with Emergency Data (Phase 12)
        # ============================================
        try:
            qr_img = generate_patient_qr_enhanced(patient_data)
            qr_buffer = io.BytesIO()
            qr_img.save(qr_buffer, format='PNG')
            qr_buffer.seek(0)
            
            qr_size = 1.4*inch
            qr_x = width - qr_size - 0.5*inch
            qr_y = 0.7*inch
            
            # QR box background
            pdf.setFillColorRGB(1, 1, 1)
            pdf.setStrokeColorRGB(0.7, 0.7, 0.7)
            pdf.setLineWidth(1)
            pdf.rect(qr_x - 0.05*inch, qr_y - 0.05*inch, 
                    qr_size + 0.1*inch, qr_size + 0.3*inch,
                    fill=True, stroke=True)
            
            pdf.drawImage(qr_buffer, qr_x, qr_y, 
                         width=qr_size, height=qr_size,
                         preserveAspectRatio=True, mask='auto')
            
            pdf.setFont("Helvetica", 7)
            pdf.setFillColorRGB(0.4, 0.4, 0.4)
            pdf.drawCentredString(qr_x + qr_size/2, qr_y - 0.15*inch, 
                                 "Scan for emergency data")
        except Exception as e:
            print(f"QR code error: {e}")
        
        # ============================================
        # FOOTER - Important Notice
        # ============================================
        footer_y = 0.5*inch
        
        # Footer bar
        pdf.setFillColorRGB(*LIGHT_GRAY)
        pdf.rect(0, footer_y - 0.15*inch, width, 0.35*inch, fill=True, stroke=False)
        
        # MedLink branding
        pdf.setFont("Helvetica-Bold", 9)
        pdf.setFillColorRGB(*INFO_BLUE)
        pdf.drawString(0.5*inch, footer_y + 0.05*inch, "MedLink")
        
        pdf.setFont("Helvetica", 8)
        pdf.setFillColorRGB(0.5, 0.5, 0.5)
        pdf.drawString(0.5*inch, footer_y - 0.1*inch, 
                      "Unified Medical Records System - Phase 12 Enhanced")
        
        # Keep card notice
        pdf.setFont("Helvetica-Bold", 8)
        pdf.setFillColorRGB(*EMERGENCY_RED)
        pdf.drawCentredString(width/2, footer_y, 
                             "⚠️  KEEP THIS CARD WITH YOU AT ALL TIMES")
        
        # Save PDF
        pdf.save()
        return True
        
    except Exception as e:
        print(f"Error generating emergency card: {e}")
        import traceback
        traceback.print_exc()
        return False