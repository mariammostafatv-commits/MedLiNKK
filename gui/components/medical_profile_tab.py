"""
Medical profile tab - Display comprehensive medical data
Location: gui/components/medical_profile_tab.py

🔴 INSTRUCTIONS: REPLACE YOUR ENTIRE medical_profile_tab.py WITH THIS FILE
"""
import customtkinter as ctk
from gui.styles import *
from core.surgery_manager import surgery_manager
from core.hospitalization_manager import hospitalization_manager
from core.vaccination_manager import vaccination_manager
from core.family_history_manager import family_history_manager
from core.disability_manager import disability_manager
from gui.components.add_surgery_dialog import AddSurgeryDialog
from gui.components.add_hospitalization_dialog import AddHospitalizationDialog
from gui.components.add_vaccination_dialog import AddVaccinationDialog
from gui.components.family_history_dialog import FamilyHistoryDialog
from gui.components.disability_dialog import DisabilityDialog


class MedicalProfileTab(ctk.CTkFrame):
    """Medical profile tab showing comprehensive medical data"""

    def __init__(self, parent, patient_data, doctor_data):
        super().__init__(parent, fg_color='transparent')

        self.patient_data = patient_data
        self.doctor_data = doctor_data

        self.create_ui()
        self.load_data()

    def create_ui(self):
        """Create medical profile UI"""
        # Main container with scrollable area
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        self.scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header with action buttons
        self.create_header()

        # Surgery Section
        self.create_surgery_section()

        # Hospitalization Section
        self.create_hospitalization_section()

        # Vaccination Section
        self.create_vaccination_section()

        # Family History Section
        self.create_family_history_section()

        # Disability Section
        self.create_disability_section()

    def create_header(self):
        """Create header with action buttons"""
        header = ctk.CTkFrame(self.scroll_frame, fg_color='transparent')
        header.pack(fill='x', pady=(0, 20))

        title = ctk.CTkLabel(
            header,
            text="📋 Complete Medical Profile",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title.pack(side='left')

        # Action buttons
        btn_frame = ctk.CTkFrame(header, fg_color='transparent')
        btn_frame.pack(side='right')

        # Add Surgery
        surgery_btn = ctk.CTkButton(
            btn_frame,
            text="+ Surgery",
            command=self.open_add_surgery,
            font=FONTS['small_bold'],
            height=35,
            width=100,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        surgery_btn.pack(side='left', padx=5)

        # Add Hospitalization
        hosp_btn = ctk.CTkButton(
            btn_frame,
            text="+ Hospital",
            command=self.open_add_hospitalization,
            font=FONTS['small_bold'],
            height=35,
            width=100,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        hosp_btn.pack(side='left', padx=5)

        # Add Vaccination
        vacc_btn = ctk.CTkButton(
            btn_frame,
            text="+ Vaccine",
            command=self.open_add_vaccination,
            font=FONTS['small_bold'],
            height=35,
            width=100,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        vacc_btn.pack(side='left', padx=5)

        # Family History
        family_btn = ctk.CTkButton(
            btn_frame,
            text="👨‍👩‍👧‍👦 Family",
            command=self.open_family_history,
            font=FONTS['small_bold'],
            height=35,
            width=100,
            fg_color=COLORS['info'],
            hover_color='#0284c7'
        )
        family_btn.pack(side='left', padx=5)

        # Disability
        disability_btn = ctk.CTkButton(
            btn_frame,
            text="♿ Disability",
            command=self.open_disability,
            font=FONTS['small_bold'],
            height=35,
            width=100,
            fg_color=COLORS['info'],
            hover_color='#0284c7'
        )
        disability_btn.pack(side='left', padx=5)

    def create_surgery_section(self):
        """Create surgery history section"""
        section = self.create_section_card("🏥 Surgery History")

        # Surgery table frame
        self.surgery_frame = ctk.CTkFrame(section, fg_color='transparent')
        self.surgery_frame.pack(
            fill='both', expand=True, padx=15, pady=(0, 15))

    def create_hospitalization_section(self):
        """Create hospitalization section"""
        section = self.create_section_card("🏥 Hospitalization History")

        # Hospitalization table frame
        self.hosp_frame = ctk.CTkFrame(section, fg_color='transparent')
        self.hosp_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def create_vaccination_section(self):
        """Create vaccination section"""
        section = self.create_section_card("💉 Vaccination Records")

        # Vaccination table frame
        self.vacc_frame = ctk.CTkFrame(section, fg_color='transparent')
        self.vacc_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def create_family_history_section(self):
        """Create family history section"""
        section = self.create_section_card("👨‍👩‍👧‍👦 Family Medical History")

        # Family history content frame
        self.family_frame = ctk.CTkFrame(section, fg_color='transparent')
        self.family_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def create_disability_section(self):
        """Create disability section"""
        section = self.create_section_card("♿ Disability & Special Needs")

        # Disability content frame
        self.disability_frame = ctk.CTkFrame(section, fg_color='transparent')
        self.disability_frame.pack(
            fill='both', expand=True, padx=15, pady=(0, 15))

    def create_section_card(self, title):
        """Create section card with title"""
        card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg']
        )
        card.pack(fill='x', pady=(0, 15))

        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=FONTS['subheading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(anchor='w', padx=15, pady=(15, 10))

        return card

    def load_data(self):
        """Load all medical data"""
        self.load_surgeries()
        self.load_hospitalizations()
        self.load_vaccinations()
        self.load_family_history()
        self.load_disability_info()

    def load_surgeries(self):
        """Load and display surgery history"""
        # Clear existing
        for widget in self.surgery_frame.winfo_children():
            widget.destroy()

        surgeries = surgery_manager.get_patient_surgeries(
            self.patient_data.get('national_id')
        )

        if not surgeries:
            no_data = ctk.CTkLabel(
                self.surgery_frame,
                text="No surgery records found",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            no_data.pack(pady=20)
            return

        # Display each surgery
        for surgery in surgeries:
            self.create_surgery_card(surgery)

    def create_surgery_card(self, surgery):
        """Create card for single surgery"""
        card = ctk.CTkFrame(
            self.surgery_frame,
            fg_color=COLORS['bg_light'],
            corner_radius=RADIUS['md']
        )
        card.pack(fill='x', pady=5)

        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='x', padx=15, pady=12)

        # Date and procedure
        header = ctk.CTkLabel(
            content,
            text=f"📅 {surgery.get('date', 'N/A')} - {surgery.get('procedure', 'Unknown')}",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        header.pack(anchor='w')

        # Details
        details = f"🏥 {surgery.get('hospital', 'N/A')} | 👨‍⚕️ {surgery.get('surgeon', 'N/A')}"
        if surgery.get('complications') and surgery['complications'] != 'None':
            details += f" | ⚠️ {surgery['complications']}"

        details_label = ctk.CTkLabel(
            content,
            text=details,
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        details_label.pack(anchor='w', pady=(5, 0))

        # Recovery time and notes
        if surgery.get('recovery_time'):
            recovery_label = ctk.CTkLabel(
                content,
                text=f"⏱️ Recovery: {surgery['recovery_time']}",
                font=FONTS['small'],
                text_color=COLORS['text_secondary']
            )
            recovery_label.pack(anchor='w', pady=(3, 0))

        if surgery.get('notes'):
            notes_label = ctk.CTkLabel(
                content,
                text=f"📝 {surgery['notes']}",
                font=FONTS['small'],
                text_color=COLORS['text_secondary'],
                wraplength=600
            )
            notes_label.pack(anchor='w', pady=(3, 0))

    def load_hospitalizations(self):
        """Load and display hospitalization history"""
        # Clear existing
        for widget in self.hosp_frame.winfo_children():
            widget.destroy()

        hospitalizations = hospitalization_manager.get_patient_hospitalizations(
            self.patient_data.get('national_id')
        )

        if not hospitalizations:
            no_data = ctk.CTkLabel(
                self.hosp_frame,
                text="No hospitalization records found",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            no_data.pack(pady=20)
            return

        # Display each hospitalization
        for hosp in hospitalizations:
            self.create_hospitalization_card(hosp)

    def create_hospitalization_card(self, hosp):
        """Create card for single hospitalization"""
        card = ctk.CTkFrame(
            self.hosp_frame,
            fg_color=COLORS['bg_light'],
            corner_radius=RADIUS['md']
        )
        card.pack(fill='x', pady=5)

        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='x', padx=15, pady=12)

        # Calculate length of stay
        los = hospitalization_manager.calculate_length_of_stay(hosp)
        los_text = f" ({los} days)" if los else ""

        # Dates and reason
        header = ctk.CTkLabel(
            content,
            text=f"📅 {hosp.get('admission_date', 'N/A')} → {hosp.get('discharge_date', 'N/A')}{los_text}",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        header.pack(anchor='w')

        reason = ctk.CTkLabel(
            content,
            text=f"🩺 Reason: {hosp.get('reason', 'N/A')}",
            font=FONTS['body'],
            text_color=COLORS['text_primary']
        )
        reason.pack(anchor='w', pady=(5, 0))

        # Hospital and department
        location = f"🏥 {hosp.get('hospital', 'N/A')}"
        if hosp.get('department'):
            location += f" - {hosp['department']}"

        location_label = ctk.CTkLabel(
            content,
            text=location,
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        location_label.pack(anchor='w', pady=(3, 0))

        # Doctor
        if hosp.get('attending_doctor'):
            doctor_label = ctk.CTkLabel(
                content,
                text=f"👨‍⚕️ {hosp['attending_doctor']}",
                font=FONTS['small'],
                text_color=COLORS['text_secondary']
            )
            doctor_label.pack(anchor='w', pady=(2, 0))

        # Outcome
        if hosp.get('outcome'):
            outcome_label = ctk.CTkLabel(
                content,
                text=f"✅ {hosp['outcome']}",
                font=FONTS['small'],
                text_color=COLORS['success']
            )
            outcome_label.pack(anchor='w', pady=(2, 0))

    def load_vaccinations(self):
        """Load and display vaccinations"""
        # Clear existing
        for widget in self.vacc_frame.winfo_children():
            widget.destroy()

        vaccinations = vaccination_manager.get_patient_vaccinations(
            self.patient_data.get('national_id')
        )

        if not vaccinations:
            no_data = ctk.CTkLabel(
                self.vacc_frame,
                text="No vaccination records found",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            no_data.pack(pady=20)
            return

        # Group by vaccine
        vaccine_groups = {}
        for vax in vaccinations:
            name = vax.get('vaccine_name', 'Unknown')
            if name not in vaccine_groups:
                vaccine_groups[name] = []
            vaccine_groups[name].append(vax)

        # Display each vaccine group
        for vaccine_name, doses in vaccine_groups.items():
            self.create_vaccination_card(vaccine_name, doses)

    def create_vaccination_card(self, vaccine_name, doses):
        """Create card for vaccine with all doses"""
        card = ctk.CTkFrame(
            self.vacc_frame,
            fg_color=COLORS['bg_light'],
            corner_radius=RADIUS['md']
        )
        card.pack(fill='x', pady=5)

        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='x', padx=15, pady=12)

        # Header
        header = ctk.CTkLabel(
            content,
            text=f"💉 {vaccine_name} ({len(doses)} dose{'s' if len(doses) > 1 else ''})",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        header.pack(anchor='w')

        # Display each dose
        for i, dose in enumerate(doses, 1):
            dose_text = f"  Dose {i}: {dose.get('date_administered', 'N/A')}"
            if dose.get('location'):
                dose_text += f" at {dose['location']}"

            dose_label = ctk.CTkLabel(
                content,
                text=dose_text,
                font=FONTS['small'],
                text_color=COLORS['text_secondary']
            )
            dose_label.pack(anchor='w', pady=(3, 0))

    def load_family_history(self):
        """Load and display family history"""
        # Clear existing
        for widget in self.family_frame.winfo_children():
            widget.destroy()

        family_history = family_history_manager.get_family_history(
            self.patient_data.get('national_id')
        )

        if not family_history:
            no_data = ctk.CTkLabel(
                self.family_frame,
                text="No family medical history recorded",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            no_data.pack(pady=20)
            return

        # Father
        if 'father' in family_history:
            father = family_history['father']
            father_text = "👨 Father: "
            if father.get('alive'):
                father_text += f"Alive, Age {father.get('age', '?')}"
            else:
                father_text += "Deceased"

            father_label = ctk.CTkLabel(
                self.family_frame,
                text=father_text,
                font=FONTS['body'],
                text_color=COLORS['text_primary']
            )
            father_label.pack(anchor='w', pady=(0, 5))

            if father.get('medical_conditions'):
                conds = ', '.join(father['medical_conditions'])
                cond_label = ctk.CTkLabel(
                    self.family_frame,
                    text=f"  Conditions: {conds}",
                    font=FONTS['small'],
                    text_color=COLORS['text_secondary']
                )
                cond_label.pack(anchor='w', pady=(0, 10))

        # Mother
        if 'mother' in family_history:
            mother = family_history['mother']
            mother_text = "👩 Mother: "
            if mother.get('alive'):
                mother_text += f"Alive, Age {mother.get('age', '?')}"
            else:
                mother_text += "Deceased"

            mother_label = ctk.CTkLabel(
                self.family_frame,
                text=mother_text,
                font=FONTS['body'],
                text_color=COLORS['text_primary']
            )
            mother_label.pack(anchor='w', pady=(0, 5))

            if mother.get('medical_conditions'):
                conds = ', '.join(mother['medical_conditions'])
                cond_label = ctk.CTkLabel(
                    self.family_frame,
                    text=f"  Conditions: {conds}",
                    font=FONTS['small'],
                    text_color=COLORS['text_secondary']
                )
                cond_label.pack(anchor='w', pady=(0, 10))

        # Genetic conditions
        if family_history.get('genetic_conditions'):
            gen_label = ctk.CTkLabel(
                self.family_frame,
                text=f"🧬 Genetic: {', '.join(family_history['genetic_conditions'])}",
                font=FONTS['small'],
                text_color=COLORS['warning']
            )
            gen_label.pack(anchor='w', pady=(10, 0))

    def load_disability_info(self):
        """Load and display disability info"""
        # Clear existing
        for widget in self.disability_frame.winfo_children():
            widget.destroy()

        disability_info = disability_manager.get_disability_info(
            self.patient_data.get('national_id')
        )

        if not disability_info or not disability_info.get('has_disability'):
            no_data = ctk.CTkLabel(
                self.disability_frame,
                text="No disability or special needs recorded",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            no_data.pack(pady=20)
            return

        # Disability type
        if disability_info.get('disability_type'):
            type_label = ctk.CTkLabel(
                self.disability_frame,
                text=f"♿ Type: {disability_info['disability_type']}",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary']
            )
            type_label.pack(anchor='w', pady=(0, 10))

        # Mobility aids
        if disability_info.get('mobility_aids'):
            aids_label = ctk.CTkLabel(
                self.disability_frame,
                text=f"🦽 Mobility aids: {', '.join(disability_info['mobility_aids'])}",
                font=FONTS['small'],
                text_color=COLORS['text_secondary']
            )
            aids_label.pack(anchor='w', pady=2)

        # Impairments
        if disability_info.get('hearing_impairment'):
            ctk.CTkLabel(
                self.disability_frame,
                text="👂 Hearing impairment",
                font=FONTS['small'],
                text_color=COLORS['text_secondary']
            ).pack(anchor='w', pady=2)

        if disability_info.get('visual_impairment'):
            ctk.CTkLabel(
                self.disability_frame,
                text="👁️ Visual impairment",
                font=FONTS['small'],
                text_color=COLORS['text_secondary']
            ).pack(anchor='w', pady=2)

        # Notes
        if disability_info.get('notes'):
            notes_label = ctk.CTkLabel(
                self.disability_frame,
                text=f"\n📝 {disability_info['notes']}",
                font=FONTS['small'],
                text_color=COLORS['text_secondary'],
                wraplength=600
            )
            notes_label.pack(anchor='w', pady=(10, 0))

    # Dialog openers
    def open_add_surgery(self):
        """Open add surgery dialog"""
        dialog = AddSurgeryDialog(
            self,
            self.patient_data,
            self.doctor_data,
            self.load_surgeries
        )

    def open_add_hospitalization(self):
        """Open add hospitalization dialog"""
        dialog = AddHospitalizationDialog(
            self,
            self.patient_data,
            self.doctor_data,
            self.load_hospitalizations
        )

    def open_add_vaccination(self):
        """Open add vaccination dialog"""
        dialog = AddVaccinationDialog(
            self,
            self.patient_data,
            self.doctor_data,
            self.load_vaccinations
        )

    def open_family_history(self):
        """Open family history dialog"""
        dialog = FamilyHistoryDialog(
            self,
            self.patient_data,
            self.load_family_history
        )

    def open_disability(self):
        """Open disability dialog"""
        dialog = DisabilityDialog(
            self,
            self.patient_data,
            self.load_disability_info
        )
