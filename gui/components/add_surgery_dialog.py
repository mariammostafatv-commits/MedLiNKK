"""
Add surgery dialog - Add surgery record to patient
Location: gui/components/add_surgery_dialog.py
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from core.surgery_manager import surgery_manager
from utils.date_utils import get_current_date, is_valid_date


class AddSurgeryDialog(ctk.CTkToplevel):
    """Dialog for adding new surgery record"""
    
    def __init__(self, parent, patient_data, doctor_data, on_success):
        super().__init__(parent)
        
        self.patient_data = patient_data
        self.doctor_data = doctor_data
        self.on_success = on_success
        
        # Configure window
        self.title("Add Surgery Record")
        self.geometry("700x750")
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
        """Create add surgery form"""
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header
        header = ctk.CTkFrame(main_frame, fg_color='transparent')
        header.pack(fill='x', pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header,
            text="🏥  Add Surgery Record",
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
        
        # Date
        date_label = ctk.CTkLabel(
            form_content,
            text="📅  Surgery Date *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        date_label.pack(anchor='w', pady=(0, 5))
        
        self.date_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="YYYY-MM-DD",
            font=FONTS['body'],
            height=40
        )
        self.date_entry.pack(fill='x', pady=(0, 15))
        self.date_entry.insert(0, get_current_date())
        
        # Procedure
        procedure_label = ctk.CTkLabel(
            form_content,
            text="⚕️  Procedure *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        procedure_label.pack(anchor='w', pady=(0, 5))
        
        self.procedure_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="e.g., Appendectomy, Knee Arthroscopy",
            font=FONTS['body'],
            height=40
        )
        self.procedure_entry.pack(fill='x', pady=(0, 15))
        
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
            placeholder_text="e.g., Cairo University Hospital",
            font=FONTS['body'],
            height=40
        )
        self.hospital_entry.pack(fill='x', pady=(0, 15))
        
        # Surgeon
        surgeon_label = ctk.CTkLabel(
            form_content,
            text="👨‍⚕️  Surgeon *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        surgeon_label.pack(anchor='w', pady=(0, 5))
        
        self.surgeon_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Surgeon's full name",
            font=FONTS['body'],
            height=40
        )
        self.surgeon_entry.pack(fill='x', pady=(0, 15))
        
        # Complications
        complications_label = ctk.CTkLabel(
            form_content,
            text="⚠️  Complications (if any)",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        complications_label.pack(anchor='w', pady=(0, 5))
        
        self.complications_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="None, or describe any complications",
            font=FONTS['body'],
            height=40
        )
        self.complications_entry.pack(fill='x', pady=(0, 15))
        self.complications_entry.insert(0, "None")
        
        # Recovery Time
        recovery_label = ctk.CTkLabel(
            form_content,
            text="⏱️  Recovery Time",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        recovery_label.pack(anchor='w', pady=(0, 5))
        
        self.recovery_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="e.g., 2 weeks, 1 month",
            font=FONTS['body'],
            height=40
        )
        self.recovery_entry.pack(fill='x', pady=(0, 15))
        
        # Additional Notes
        notes_label = ctk.CTkLabel(
            form_content,
            text="📝  Additional Notes",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        notes_label.pack(anchor='w', pady=(0, 5))
        
        self.notes_entry = ctk.CTkTextbox(
            form_content,
            font=FONTS['body'],
            height=80,
            wrap='word'
        )
        self.notes_entry.pack(fill='x', pady=(0, 15))
        
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
            text="Save Surgery",
            command=self.handle_save,
            font=FONTS['body_bold'],
            height=50,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        save_btn.pack(side='right', fill='x', expand=True, padx=(10, 0))
    
    def handle_save(self):
        """Save new surgery record"""
        # Get form data
        date = self.date_entry.get().strip()
        procedure = self.procedure_entry.get().strip()
        hospital = self.hospital_entry.get().strip()
        surgeon = self.surgeon_entry.get().strip()
        complications = self.complications_entry.get().strip()
        recovery_time = self.recovery_entry.get().strip()
        notes = self.notes_entry.get("1.0", "end-1c").strip()
        
        # Validate required fields
        if not all([date, procedure, hospital, surgeon]):
            messagebox.showerror("Validation Error", "Please fill all required fields (*)")
            return
        
        if not is_valid_date(date):
            messagebox.showerror("Invalid Date", "Please enter date in YYYY-MM-DD format")
            return
        
        # Create surgery data
        surgery_data = {
            'date': date,
            'procedure': procedure,
            'hospital': hospital,
            'surgeon': surgeon,
            'complications': complications if complications else None,
            'recovery_time': recovery_time if recovery_time else None,
            'notes': notes if notes else None
        }
        
        # Save surgery
        success, message = surgery_manager.add_surgery(
            self.patient_data.get('national_id'),
            surgery_data
        )
        
        if success:
            messagebox.showinfo("Success", "Surgery record added successfully!")
            self.on_success()
            self.destroy()
        else:
            messagebox.showerror("Error", f"Failed to save surgery: {message}")