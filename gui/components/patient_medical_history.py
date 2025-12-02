"""
Patient medical history - View-only medical data for patients
Location: gui/components/patient_medical_history.py
"""
import customtkinter as ctk
from gui.styles import *
from core.surgery_manager import surgery_manager
from core.hospitalization_manager import hospitalization_manager
from core.vaccination_manager import vaccination_manager
from core.family_history_manager import family_history_manager
from core.disability_manager import disability_manager


class PatientMedicalHistory(ctk.CTkFrame):
    """View-only medical history for patients"""
    
    def __init__(self, parent, patient_data):
        super().__init__(parent, fg_color='transparent')
        
        self.patient_data = patient_data
        self.create_ui()
        self.load_data()
    
    def create_ui(self):
        """Create patient medical history UI"""
        # Header
        header = ctk.CTkFrame(self, fg_color='transparent')
        header.pack(fill='x', padx=20, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header,
            text="📋 My Medical History",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title.pack(anchor='w')
        
        subtitle = ctk.CTkLabel(
            header,
            text="Complete overview of your medical records",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        subtitle.pack(anchor='w', pady=(5, 0))
        
        # Scrollable content
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        self.scroll_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create sections
        self.create_basic_info_section()
        self.create_allergies_section()
        self.create_chronic_conditions_section()
        self.create_medications_section()
        self.create_surgeries_section()
        self.create_hospitalizations_section()
        self.create_vaccinations_section()
        self.create_family_history_section()
        self.create_disability_section()
    
    def create_basic_info_section(self):
        """Create basic patient information section"""
        section = self.create_section_card("👤 Basic Information")
        
        content = ctk.CTkFrame(section, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=(0, 15))
        
        # Blood Type
        blood_type = self.patient_data.get('blood_type', 'Unknown')
        self.create_info_row(content, "🩸 Blood Type", blood_type).pack(fill='x', pady=3)
        
        # Date of Birth
        dob = self.patient_data.get('date_of_birth', 'Unknown')
        self.create_info_row(content, "📅 Date of Birth", dob).pack(fill='x', pady=3)
        
        # Gender
        gender = self.patient_data.get('gender', 'Unknown')
        self.create_info_row(content, "⚧️ Gender", gender).pack(fill='x', pady=3)
        
        # Height & Weight
        height = self.patient_data.get('height', 'Not recorded')
        weight = self.patient_data.get('weight', 'Not recorded')
        vitals = f"{height} | {weight}"
        self.create_info_row(content, "📏 Height | Weight", vitals).pack(fill='x', pady=3)
    
    def create_allergies_section(self):
        """Create allergies section"""
        section = self.create_section_card("⚠️ Allergies")
        
        content = ctk.CTkFrame(section, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=(0, 15))
        
        allergies = self.patient_data.get('allergies', [])
        
        if not allergies:
            no_data = ctk.CTkLabel(
                content,
                text="No known allergies recorded",
                font=FONTS['body'],
                text_color=COLORS['success']
            )
            no_data.pack(pady=10)
        else:
            for allergy in allergies:
                allergy_card = ctk.CTkFrame(
                    content,
                    fg_color=COLORS['bg_light'],
                    corner_radius=RADIUS['sm']
                )
                allergy_card.pack(fill='x', pady=3)
                
                allergy_label = ctk.CTkLabel(
                    allergy_card,
                    text=f"⚠️ {allergy}",
                    font=FONTS['body'],
                    text_color=COLORS['danger']
                )
                allergy_label.pack(padx=15, pady=8, anchor='w')
    
    def create_chronic_conditions_section(self):
        """Create chronic conditions section"""
        section = self.create_section_card("📋 Chronic Conditions")
        
        content = ctk.CTkFrame(section, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=(0, 15))
        
        chronic = self.patient_data.get('chronic_conditions', [])
        
        if not chronic:
            no_data = ctk.CTkLabel(
                content,
                text="No chronic conditions recorded",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            no_data.pack(pady=10)
        else:
            for condition in chronic:
                condition_card = ctk.CTkFrame(
                    content,
                    fg_color=COLORS['bg_light'],
                    corner_radius=RADIUS['sm']
                )
                condition_card.pack(fill='x', pady=3)
                
                condition_label = ctk.CTkLabel(
                    condition_card,
                    text=f"📋 {condition}",
                    font=FONTS['body'],
                    text_color=COLORS['text_primary']
                )
                condition_label.pack(padx=15, pady=8, anchor='w')
    
    def create_medications_section(self):
        """Create current medications section"""
        section = self.create_section_card("💊 Current Medications")
        
        content = ctk.CTkFrame(section, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=(0, 15))
        
        medications = self.patient_data.get('current_medications', [])
   
        if medications:
            # Extract medication names from dictionaries
            if isinstance(medications[0], dict):
                med_names = [med.get('name', 'Unknown') for med in medications[:3]]
            else:
                med_names = medications[:3]
            
            med_text = "💊 Medications: " + ", ".join(med_names)
        if not medications:
            no_data = ctk.CTkLabel(
                content,
                text="No current medications recorded",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            no_data.pack(pady=10)
        else:
            for medication in medications:
                med_card = ctk.CTkFrame(
                    content,
                    fg_color=COLORS['bg_light'],
                    corner_radius=RADIUS['sm']
                )
                med_card.pack(fill='x', pady=3)
                
                med_label = ctk.CTkLabel(
                    med_card,
                    text=f"💊 {medication}",
                    font=FONTS['body'],
                    text_color=COLORS['text_primary']
                )
                med_label.pack(padx=15, pady=8, anchor='w')
    
    def create_surgeries_section(self):
        """Create surgeries section"""
        section = self.create_section_card("🏥 Surgery History")
        
        self.surgeries_content = ctk.CTkFrame(section, fg_color='transparent')
        self.surgeries_content.pack(fill='x', padx=20, pady=(0, 15))
    
    def create_hospitalizations_section(self):
        """Create hospitalizations section"""
        section = self.create_section_card("🏥 Hospitalization History")
        
        self.hosp_content = ctk.CTkFrame(section, fg_color='transparent')
        self.hosp_content.pack(fill='x', padx=20, pady=(0, 15))
    
    def create_vaccinations_section(self):
        """Create vaccinations section"""
        section = self.create_section_card("💉 Vaccination Records")
        
        self.vacc_content = ctk.CTkFrame(section, fg_color='transparent')
        self.vacc_content.pack(fill='x', padx=20, pady=(0, 15))
    
    def create_family_history_section(self):
        """Create family history section"""
        section = self.create_section_card("👨‍👩‍👧‍👦 Family Medical History")
        
        self.family_content = ctk.CTkFrame(section, fg_color='transparent')
        self.family_content.pack(fill='x', padx=20, pady=(0, 15))
    
    def create_disability_section(self):
        """Create disability section"""
        section = self.create_section_card("♿ Accessibility Information")
        
        self.disability_content = ctk.CTkFrame(section, fg_color='transparent')
        self.disability_content.pack(fill='x', padx=20, pady=(0, 15))
    
    def create_section_card(self, title):
        """Create section card with title"""
        card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg']
        )
        card.pack(fill='x', pady=(0, 15))
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=FONTS['subheading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(anchor='w', padx=20, pady=(15, 10))
        
        return card
    
    def create_info_row(self, parent, label, value):
        """Create information row"""
        row = ctk.CTkFrame(parent, fg_color='transparent')
        
        label_widget = ctk.CTkLabel(
            row,
            text=label,
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        label_widget.pack(side='left')
        
        value_label = ctk.CTkLabel(
            row,
            text=value,
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        value_label.pack(side='right')
        
        return row
    
    def load_data(self):
        """Load all medical data"""
        self.load_surgeries()
        self.load_hospitalizations()
        self.load_vaccinations()
        self.load_family_history()
        self.load_disability_info()
    
    def load_surgeries(self):
        """Load surgery data"""
        for widget in self.surgeries_content.winfo_children():
            widget.destroy()
        
        surgeries = surgery_manager.get_patient_surgeries(
            self.patient_data.get('national_id')
        )
        
        if not surgeries:
            no_data = ctk.CTkLabel(
                self.surgeries_content,
                text="No surgery records found",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            no_data.pack(pady=10)
            return
        
        for surgery in surgeries:
            card = ctk.CTkFrame(
                self.surgeries_content,
                fg_color=COLORS['bg_light'],
                corner_radius=RADIUS['md']
            )
            card.pack(fill='x', pady=5)
            
            content = ctk.CTkFrame(card, fg_color='transparent')
            content.pack(fill='x', padx=15, pady=12)
            
            # Header
            header = ctk.CTkLabel(
                content,
                text=f"📅 {surgery.get('date', 'N/A')} - {surgery.get('procedure', 'Unknown')}",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary']
            )
            header.pack(anchor='w')
            
            # Details
            details = f"🏥 {surgery.get('hospital', 'N/A')} | 👨‍⚕️ {surgery.get('surgeon', 'N/A')}"
            details_label = ctk.CTkLabel(
                content,
                text=details,
                font=FONTS['small'],
                text_color=COLORS['text_secondary']
            )
            details_label.pack(anchor='w', pady=(5, 0))
    
    def load_hospitalizations(self):
        """Load hospitalization data"""
        for widget in self.hosp_content.winfo_children():
            widget.destroy()
        
        hospitalizations = hospitalization_manager.get_patient_hospitalizations(
            self.patient_data.get('national_id')
        )
        
        if not hospitalizations:
            no_data = ctk.CTkLabel(
                self.hosp_content,
                text="No hospitalization records found",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            no_data.pack(pady=10)
            return
        
        for hosp in hospitalizations:
            card = ctk.CTkFrame(
                self.hosp_content,
                fg_color=COLORS['bg_light'],
                corner_radius=RADIUS['md']
            )
            card.pack(fill='x', pady=5)
            
            content = ctk.CTkFrame(card, fg_color='transparent')
            content.pack(fill='x', padx=15, pady=12)
            
            # Dates
            los = hospitalization_manager.calculate_length_of_stay(hosp)
            los_text = f" ({los} days)" if los else ""
            
            header = ctk.CTkLabel(
                content,
                text=f"📅 {hosp.get('admission_date', 'N/A')} → {hosp.get('discharge_date', 'N/A')}{los_text}",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary']
            )
            header.pack(anchor='w')
            
            # Reason
            reason = ctk.CTkLabel(
                content,
                text=f"🩺 {hosp.get('reason', 'N/A')}",
                font=FONTS['body'],
                text_color=COLORS['text_primary']
            )
            reason.pack(anchor='w', pady=(5, 0))
    
    def load_vaccinations(self):
        """Load vaccination data"""
        for widget in self.vacc_content.winfo_children():
            widget.destroy()
        
        vaccinations = vaccination_manager.get_patient_vaccinations(
            self.patient_data.get('national_id')
        )
        
        if not vaccinations:
            no_data = ctk.CTkLabel(
                self.vacc_content,
                text="No vaccination records found",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            no_data.pack(pady=10)
            return
        
        # Group by vaccine
        vaccine_groups = {}
        for vacc in vaccinations:
            name = vacc.get('vaccine_name', 'Unknown')
            if name not in vaccine_groups:
                vaccine_groups[name] = []
            vaccine_groups[name].append(vacc)
        
        for vaccine_name, doses in vaccine_groups.items():
            card = ctk.CTkFrame(
                self.vacc_content,
                fg_color=COLORS['bg_light'],
                corner_radius=RADIUS['md']
            )
            card.pack(fill='x', pady=5)
            
            content = ctk.CTkFrame(card, fg_color='transparent')
            content.pack(fill='x', padx=15, pady=12)
            
            # Vaccine name
            header = ctk.CTkLabel(
                content,
                text=f"💉 {vaccine_name} - {len(doses)} dose(s)",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary']
            )
            header.pack(anchor='w')
            
            # Latest dose
            latest = doses[0]
            latest_label = ctk.CTkLabel(
                content,
                text=f"Latest: {latest.get('date_administered', 'N/A')}",
                font=FONTS['small'],
                text_color=COLORS['text_secondary']
            )
            latest_label.pack(anchor='w', pady=(5, 0))
    
    def load_family_history(self):
        """Load family history data"""
        for widget in self.family_content.winfo_children():
            widget.destroy()
        
        family_history = family_history_manager.get_family_history(
            self.patient_data.get('national_id')
        )
        
        if not family_history:
            no_data = ctk.CTkLabel(
                self.family_content,
                text="No family medical history recorded",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            no_data.pack(pady=10)
            return
        
        # Risk summary
        risk_summary = family_history_manager.get_genetic_risk_summary(
            self.patient_data.get('national_id')
        )
        
        if risk_summary.get('risk_factors'):
            risk_text = "⚠️ Family Risk Factors: " + ", ".join(risk_summary['risk_factors'][:3])
            if len(risk_summary['risk_factors']) > 3:
                risk_text += f" (+{len(risk_summary['risk_factors']) - 3} more)"
            
            risk_label = ctk.CTkLabel(
                self.family_content,
                text=risk_text,
                font=FONTS['body'],
                text_color=COLORS['warning'],
                wraplength=600
            )
            risk_label.pack(anchor='w', pady=(0, 10))
    
    def load_disability_info(self):
        """Load disability information"""
        for widget in self.disability_content.winfo_children():
            widget.destroy()
        
        disability_info = disability_manager.get_disability_info(
            self.patient_data.get('national_id')
        )
        
        if not disability_info or not disability_info.get('has_disability'):
            no_data = ctk.CTkLabel(
                self.disability_content,
                text="No accessibility needs recorded",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            no_data.pack(pady=10)
            return
        
        summary = disability_manager.get_accessibility_summary(
            self.patient_data.get('national_id')
        )
        
        if summary.get('summary'):
            for item in summary['summary']:
                item_label = ctk.CTkLabel(
                    self.disability_content,
                    text=f"  • {item}",
                    font=FONTS['body'],
                    text_color=COLORS['text_primary']
                )
                item_label.pack(anchor='w', pady=2)