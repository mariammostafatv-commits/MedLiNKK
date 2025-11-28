"""
Add hospitalization dialog - Add hospitalization record to patient
Location: gui/components/add_hospitalization_dialog.py
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from core.hospitalization_manager import hospitalization_manager
from utils.date_utils import get_current_date, is_valid_date


class AddHospitalizationDialog(ctk.CTkToplevel):
    """Dialog for adding new hospitalization record"""
    
    def __init__(self, parent, patient_data, doctor_data, on_success):
        super().__init__(parent)
        
        self.patient_data = patient_data
        self.doctor_data = doctor_data
        self.on_success = on_success
        
        # Configure window
        self.title("Add Hospitalization Record")
        self.geometry("700x850")
        self.resizable(False, False)
        
        # Center on parent
        self.transient(parent)
        self.grab_set()
        
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        self.create_ui()
    
    def create_ui(self):
        """Create add hospitalization form"""
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header
        header = ctk.CTkFrame(main_frame, fg_color='transparent')
        header.pack(fill='x', pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header,
            text="🏥  Add Hospitalization Record",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(anchor='w')
        
        patient_label = ctk.CTkLabel(
            header,
            text=f"Patient: {self.patient_data.get('full_name', 'N/A')}",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        patient_label.pack(anchor='w', pady=(5, 0))
        
        # Scrollable form
        form_scroll = ctk.CTkScrollableFrame(
            main_frame,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg']
        )
        form_scroll.pack(fill='both', expand=True)
        
        form_content = ctk.CTkFrame(form_scroll, fg_color='transparent')
        form_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Dates Section
        dates_frame = ctk.CTkFrame(form_content, fg_color='transparent')
        dates_frame.pack(fill='x', pady=(0, 15))
        
        # Admission Date
        admission_container = ctk.CTkFrame(dates_frame, fg_color='transparent')
        admission_container.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        admission_label = ctk.CTkLabel(
            admission_container,
            text="📅  Admission Date *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        admission_label.pack(anchor='w', pady=(0, 5))
        
        self.admission_date_entry = ctk.CTkEntry(
            admission_container,
            placeholder_text="YYYY-MM-DD",
            font=FONTS['body'],
            height=40
        )
        self.admission_date_entry.pack(fill='x')
        self.admission_date_entry.insert(0, get_current_date())
        
        # Discharge Date
        discharge_container = ctk.CTkFrame(dates_frame, fg_color='transparent')
        discharge_container.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        discharge_label = ctk.CTkLabel(
            discharge_container,
            text="📅  Discharge Date *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        discharge_label.pack(anchor='w', pady=(0, 5))
        
        self.discharge_date_entry = ctk.CTkEntry(
            discharge_container,
            placeholder_text="YYYY-MM-DD",
            font=FONTS['body'],
            height=40
        )
        self.discharge_date_entry.pack(fill='x')
        
        # Reason for Admission
        reason_label = ctk.CTkLabel(
            form_content,
            text="🩺  Reason for Admission *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        reason_label.pack(anchor='w', pady=(0, 5))
        
        self.reason_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="e.g., Acute appendicitis, COVID-19",
            font=FONTS['body'],
            height=40
        )
        self.reason_entry.pack(fill='x', pady=(0, 15))
        
        # Hospital
        hospital_label = ctk.CTkLabel(
            form_content,
            text="🏥  Hospital *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        hospital_label.pack(anchor='w', pady=(0, 5))
        
        self.hospital_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Hospital name",
            font=FONTS['body'],
            height=40
        )
        self.hospital_entry.pack(fill='x', pady=(0, 15))
        
        # Department
        department_label = ctk.CTkLabel(
            form_content,
            text="🏢  Department",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        department_label.pack(anchor='w', pady=(0, 5))
        
        self.department_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="e.g., Internal Medicine, ICU",
            font=FONTS['body'],
            height=40
        )
        self.department_entry.pack(fill='x', pady=(0, 15))
        
        # Attending Doctor
        doctor_label = ctk.CTkLabel(
            form_content,
            text="👨‍⚕️  Attending Doctor",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        doctor_label.pack(anchor='w', pady=(0, 5))
        
        self.doctor_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Doctor's name",
            font=FONTS['body'],
            height=40
        )
        self.doctor_entry.pack(fill='x', pady=(0, 15))
        
        # Diagnosis
        diagnosis_label = ctk.CTkLabel(
            form_content,
            text="🔬  Diagnosis",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        diagnosis_label.pack(anchor='w', pady=(0, 5))
        
        self.diagnosis_entry = ctk.CTkTextbox(
            form_content,
            font=FONTS['body'],
            height=60,
            wrap='word'
        )
        self.diagnosis_entry.pack(fill='x', pady=(0, 15))
        
        # Treatment Summary
        treatment_label = ctk.CTkLabel(
            form_content,
            text="💊  Treatment Summary",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        treatment_label.pack(anchor='w', pady=(0, 5))
        
        self.treatment_entry = ctk.CTkTextbox(
            form_content,
            font=FONTS['body'],
            height=60,
            wrap='word'
        )
        self.treatment_entry.pack(fill='x', pady=(0, 15))
        
        # Outcome
        outcome_label = ctk.CTkLabel(
            form_content,
            text="📊  Outcome",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        outcome_label.pack(anchor='w', pady=(0, 5))
        
        self.outcome_entry = ctk.CTkOptionMenu(
            form_content,
            values=["Recovered", "Improved", "Stable", "Transferred", "Discharged against medical advice"],
            font=FONTS['body'],
            height=40
        )
        self.outcome_entry.pack(fill='x', pady=(0, 15))
        
        # Buttons
        btn_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        btn_frame.pack(fill='x', pady=(20, 0))
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.destroy,
            font=FONTS['body_bold'],
            height=50,
            fg_color='transparent',
            hover_color=COLORS['bg_light'],
            border_width=2,
            border_color=COLORS['danger'],
            text_color=COLORS['danger']
        )
        cancel_btn.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Save Hospitalization",
            command=self.handle_save,
            font=FONTS['body_bold'],
            height=50,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        save_btn.pack(side='right', fill='x', expand=True, padx=(10, 0))
    
    def handle_save(self):
        """Save new hospitalization record"""
        # Get form data
        admission_date = self.admission_date_entry.get().strip()
        discharge_date = self.discharge_date_entry.get().strip()
        reason = self.reason_entry.get().strip()
        hospital = self.hospital_entry.get().strip()
        department = self.department_entry.get().strip()
        doctor = self.doctor_entry.get().strip()
        diagnosis = self.diagnosis_entry.get("1.0", "end-1c").strip()
        treatment = self.treatment_entry.get("1.0", "end-1c").strip()
        outcome = self.outcome_entry.get()
        
        # Validate required fields
        if not all([admission_date, discharge_date, reason, hospital]):
            messagebox.showerror("Validation Error", "Please fill all required fields (*)")
            return
        
        if not is_valid_date(admission_date) or not is_valid_date(discharge_date):
            messagebox.showerror("Invalid Date", "Please enter dates in YYYY-MM-DD format")
            return
        
        # Check discharge is after admission
        if discharge_date < admission_date:
            messagebox.showerror("Invalid Dates", "Discharge date must be after admission date")
            return
        
        # Create hospitalization data
        hospitalization_data = {
            'admission_date': admission_date,
            'discharge_date': discharge_date,
            'reason': reason,
            'hospital': hospital,
            'department': department if department else None,
            'attending_doctor': doctor if doctor else None,
            'diagnosis': diagnosis if diagnosis else None,
            'treatment_summary': treatment if treatment else None,
            'outcome': outcome
        }
        
        # Save hospitalization
        success, message = hospitalization_manager.add_hospitalization(
            self.patient_data.get('national_id'),
            hospitalization_data
        )
        
        if success:
            messagebox.showinfo("Success", "Hospitalization record added successfully!")
            self.on_success()
            self.destroy()
        else:
            messagebox.showerror("Error", f"Failed to save hospitalization: {message}")