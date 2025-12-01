"""
Enhanced patient card - Shows patient info with medical badges
Location: gui/components/enhanced_patient_card.py
"""
import customtkinter as ctk
from gui.styles import *
from core.disability_manager import disability_manager
from utils.date_utils import calculate_age


class PatientCard(ctk.CTkFrame):
    """Enhanced patient card with medical status badges"""
    
    def __init__(self, parent, patient_data):
        super().__init__(
            parent,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg']
        )
        
        self.patient_data = patient_data
        self.create_ui()
    
    def create_ui(self):
        """Create enhanced patient card UI"""
        # Main content
        content = ctk.CTkFrame(self, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header with photo placeholder and basic info
        header = ctk.CTkFrame(content, fg_color='transparent')
        header.pack(fill='x', pady=(0, 15))
        
        # Photo placeholder
        photo_frame = ctk.CTkFrame(
            header,
            width=80,
            height=80,
            fg_color=COLORS['primary'],
            corner_radius=RADIUS['full']
        )
        photo_frame.pack(side='left', padx=(0, 15))
        photo_frame.pack_propagate(False)
        
        initials = self.get_initials()
        photo_label = ctk.CTkLabel(
            photo_frame,
            text=initials,
            font=('Segoe UI', 32, 'bold'),
            text_color='white'
        )
        photo_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Patient info
        info_frame = ctk.CTkFrame(header, fg_color='transparent')
        info_frame.pack(side='left', fill='both', expand=True)
        
        # Name
        name_label = ctk.CTkLabel(
            info_frame,
            text=self.patient_data.get('full_name', 'N/A'),
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        name_label.pack(anchor='w')
        
        # Age, Gender, Blood Type
        age = calculate_age(self.patient_data.get('date_of_birth', ''))
        gender = self.patient_data.get('gender', 'N/A')
        blood_type = self.patient_data.get('blood_type', 'N/A')
        
        demographics = f"{age} years • {gender} • Blood Type: {blood_type}"
        demo_label = ctk.CTkLabel(
            info_frame,
            text=demographics,
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        demo_label.pack(anchor='w', pady=(5, 0))
        
        # National ID
        national_id = self.patient_data.get('national_id', 'N/A')
        id_label = ctk.CTkLabel(
            info_frame,
            text=f"ID: {national_id}",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        id_label.pack(anchor='w', pady=(3, 0))
        
        # Badges Section
        self.create_badges(content)
        
        # Divider
        divider = ctk.CTkFrame(content, height=1, fg_color=COLORS['bg_light'])
        divider.pack(fill='x', pady=15)
        
        # Contact Information
        self.create_contact_info(content)
        
        # Medical Summary
        self.create_medical_summary(content)
    
    def create_badges(self, parent):
        """Create status badges"""
        badge_frame = ctk.CTkFrame(parent, fg_color='transparent')
        badge_frame.pack(fill='x', pady=(0, 10))
        
        # Check for disability
        disability_info = disability_manager.get_disability_info(
            self.patient_data.get('national_id')
        )
        
        if disability_info and disability_info.get('has_disability'):
            disability_badge = self.create_badge(
                badge_frame,
                "♿ DISABILITY",
                COLORS['warning']
            )
            disability_badge.pack(side='left', padx=(0, 10))
        
        # Check for DNR status (from emergency directives)
        emergency_directives = self.patient_data.get('emergency_directives', {})
        if emergency_directives.get('dnr_status'):
            dnr_badge = self.create_badge(
                badge_frame,
                "🚫 DNR",
                COLORS['danger']
            )
            dnr_badge.pack(side='left', padx=(0, 10))
        
        # Check for organ donor
        if emergency_directives.get('organ_donor'):
            donor_badge = self.create_badge(
                badge_frame,
                "❤️ ORGAN DONOR",
                COLORS['success']
            )
            donor_badge.pack(side='left', padx=(0, 10))
        
        # Check for allergies
        allergies = self.patient_data.get('allergies', [])
        if allergies and len(allergies) > 0:
            allergy_badge = self.create_badge(
                badge_frame,
                f"⚠️ ALLERGIES ({len(allergies)})",
                COLORS['danger']
            )
            allergy_badge.pack(side='left', padx=(0, 10))
        
        # Check for chronic conditions
        chronic_conditions = self.patient_data.get('chronic_conditions', [])
        if chronic_conditions and len(chronic_conditions) > 0:
            chronic_badge = self.create_badge(
                badge_frame,
                f"📋 CHRONIC ({len(chronic_conditions)})",
                COLORS['info']
            )
            chronic_badge.pack(side='left', padx=(0, 10))
    
    def create_badge(self, parent, text, color):
        """Create status badge"""
        badge = ctk.CTkFrame(
            parent,
            fg_color=color,
            corner_radius=RADIUS['sm'],
            height=28
        )
        
        badge_label = ctk.CTkLabel(
            badge,
            text=text,
            font=('Segoe UI', 11, 'bold'),
            text_color='white'
        )
        badge_label.pack(padx=12, pady=5)
        
        return badge
    
    def create_contact_info(self, parent):
        """Create contact information section"""
        contact_frame = ctk.CTkFrame(parent, fg_color='transparent')
        contact_frame.pack(fill='x', pady=(0, 15))
        
        # Phone
        phone = self.patient_data.get('phone', 'N/A')
        phone_row = self.create_info_row(contact_frame, "📱", "Phone", phone)
        phone_row.pack(fill='x', pady=3)
        
        # Email
        email = self.patient_data.get('email', 'N/A')
        email_row = self.create_info_row(contact_frame, "📧", "Email", email)
        email_row.pack(fill='x', pady=3)
        
        # Address
        address = self.patient_data.get('address', 'N/A')
        address_row = self.create_info_row(contact_frame, "📍", "Address", address)
        address_row.pack(fill='x', pady=3)
        
        # Emergency Contact
        emergency_contact = self.patient_data.get('emergency_contact', {})
        if emergency_contact:
            ec_name = emergency_contact.get('name', 'N/A')
            ec_phone = emergency_contact.get('phone', 'N/A')
            ec_text = f"{ec_name} - {ec_phone}"
            ec_row = self.create_info_row(contact_frame, "🚨", "Emergency", ec_text)
            ec_row.pack(fill='x', pady=3)
    
    def create_medical_summary(self, parent):
        """Create medical summary section"""
        summary_frame = ctk.CTkFrame(parent, fg_color='transparent')
        summary_frame.pack(fill='x')
        
        title = ctk.CTkLabel(
            summary_frame,
            text="Quick Medical Summary",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        title.pack(anchor='w', pady=(0, 10))
        
        # Allergies
        allergies = self.patient_data.get('allergies', [])
        if allergies:
            allergies_text = "⚠️ Allergies: " + ", ".join(allergies)
            allergies_label = ctk.CTkLabel(
                summary_frame,
                text=allergies_text,
                font=FONTS['small'],
                text_color=COLORS['danger'],
                wraplength=350,
                justify='left'
            )
            allergies_label.pack(anchor='w', pady=2)
        
        # Chronic Conditions
        chronic = self.patient_data.get('chronic_conditions', [])
        if chronic:
            chronic_text = "📋 Chronic: " + ", ".join(chronic)
            chronic_label = ctk.CTkLabel(
                summary_frame,
                text=chronic_text,
                font=FONTS['small'],
                text_color=COLORS['text_secondary'],
                wraplength=350,
                justify='left'
            )
            chronic_label.pack(anchor='w', pady=2)
        
        # Current Medications
        medications = self.patient_data.get('current_medications', [])
        if medications:
            med_text = "💊 Medications: " + ", ".join(medications[:3])
            if len(medications) > 3:
                med_text += f" (+{len(medications) - 3} more)"
            
            med_label = ctk.CTkLabel(
                summary_frame,
                text=med_text,
                font=FONTS['small'],
                text_color=COLORS['text_secondary'],
                wraplength=350,
                justify='left'
            )
            med_label.pack(anchor='w', pady=2)
    
    def create_info_row(self, parent, icon, label, value):
        """Create information row"""
        row = ctk.CTkFrame(parent, fg_color='transparent')
        
        # Icon and label
        left = ctk.CTkFrame(row, fg_color='transparent')
        left.pack(side='left', fill='x', expand=True)
        
        text = f"{icon} {label}:"
        label_widget = ctk.CTkLabel(
            left,
            text=text,
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        label_widget.pack(side='left')
        
        # Value
        value_label = ctk.CTkLabel(
            row,
            text=value,
            font=FONTS['small'],
            text_color=COLORS['text_primary']
        )
        value_label.pack(side='right')
        
        return row
    
    def get_initials(self):
        """Get patient initials"""
        name = self.patient_data.get('full_name', 'NA')
        parts = name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}".upper()
        elif len(parts) == 1:
            return parts[0][:2].upper()
        return "NA"