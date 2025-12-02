
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from core.vaccination_manager import vaccination_manager
from utils.date_utils import get_current_date, is_valid_date


class AddVaccinationDialog(ctk.CTkToplevel):
    """Dialog for adding new vaccination record - FIXED VERSION"""
    
    def __init__(self, parent, patient_data, doctor_data, on_success):
        super().__init__(parent)
        
        self.patient_data = patient_data
        self.doctor_data = doctor_data
        self.on_success = on_success
        
        # Configure window
        self.title("Add Vaccination Record")
        self.geometry("600x700")
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
        
        # ✅ FIX: Handle window close button (X)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # ✅ FIX: Bind ESC key to close
        self.bind("<Escape>", lambda e: self.on_closing())
        
        self.create_ui()
    
    def create_ui(self):
        """Create add vaccination form"""
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header
        header = ctk.CTkFrame(main_frame, fg_color='transparent')
        header.pack(fill='x', pady=(0, 20))
        
        icon_label = ctk.CTkLabel(
            header,
            text="💉",
            font=('Segoe UI', 48)
        )
        icon_label.pack()
        
        title_label = ctk.CTkLabel(
            header,
            text="Add Vaccination Record",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(pady=(10, 0))
        
        patient_label = ctk.CTkLabel(
            header,
            text=f"Patient: {self.patient_data.get('full_name', 'N/A')}",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        patient_label.pack(pady=(5, 0))
        
        # Scrollable form card
        form_scroll = ctk.CTkScrollableFrame(
            main_frame,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg'],
            height=400
        )
        form_scroll.pack(fill='both', expand=True, pady=(0, 20))
        
        form_content = ctk.CTkFrame(form_scroll, fg_color='transparent')
        form_content.pack(fill='both', expand=True, padx=25, pady=25)
        
        # Vaccine Name
        vaccine_label = ctk.CTkLabel(
            form_content,
            text="💉  Vaccine Name *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        vaccine_label.pack(anchor='w', pady=(0, 5))
        
        self.vaccine_entry = ctk.CTkOptionMenu(
            form_content,
            values=[
                "COVID-19 (Pfizer-BioNTech)",
                "COVID-19 (Moderna)",
                "COVID-19 (AstraZeneca)",
                "COVID-19 (Sinovac)",
                "COVID-19 (Sinopharm)",
                "Influenza (Flu Shot)",
                "Hepatitis B",
                "Hepatitis A",
                "MMR (Measles, Mumps, Rubella)",
                "Tetanus/Diphtheria (Td)",
                "Tetanus/Diphtheria/Pertussis (Tdap)",
                "Polio (IPV)",
                "Pneumococcal",
                "HPV (Human Papillomavirus)",
                "Meningococcal",
                "Varicella (Chickenpox)",
                "Rotavirus",
                "Other"
            ],
            font=FONTS['body'],
            height=40,
            fg_color=COLORS['bg_light'],
            button_color=COLORS['primary']
        )
        self.vaccine_entry.pack(fill='x', pady=(0, 15))
        
        # Date Administered
        date_label = ctk.CTkLabel(
            form_content,
            text="📅  Date Administered *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        date_label.pack(anchor='w', pady=(0, 5))
        
        date_frame = ctk.CTkFrame(form_content, fg_color='transparent')
        date_frame.pack(fill='x', pady=(0, 15))
        
        self.date_entry = ctk.CTkEntry(
            date_frame,
            placeholder_text="YYYY-MM-DD",
            font=FONTS['body'],
            height=40,
            width=200
        )
        self.date_entry.pack(side='left', fill='x', expand=True)
        self.date_entry.insert(0, get_current_date())
        
        today_btn = ctk.CTkButton(
            date_frame,
            text="Today",
            command=lambda: self.date_entry.delete(0, 'end') or self.date_entry.insert(0, get_current_date()),
            width=80,
            height=40,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        today_btn.pack(side='left', padx=(10, 0))
        
        # Dose Number
        dose_label = ctk.CTkLabel(
            form_content,
            text="🔢  Dose Number",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        dose_label.pack(anchor='w', pady=(0, 5))
        
        self.dose_entry = ctk.CTkOptionMenu(
            form_content,
            values=["1st Dose", "2nd Dose", "3rd Dose", "Booster", "Annual"],
            font=FONTS['body'],
            height=40,
            fg_color=COLORS['bg_light'],
            button_color=COLORS['primary']
        )
        self.dose_entry.pack(fill='x', pady=(0, 15))
        
        # Location
        location_label = ctk.CTkLabel(
            form_content,
            text="📍  Vaccination Location *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        location_label.pack(anchor='w', pady=(0, 5))
        
        self.location_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="e.g., Cairo Vaccination Center, Ministry of Health Clinic",
            font=FONTS['body'],
            height=40
        )
        self.location_entry.pack(fill='x', pady=(0, 15))
        
        # Batch Number
        batch_label = ctk.CTkLabel(
            form_content,
            text="🏷️  Batch/Lot Number",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        batch_label.pack(anchor='w', pady=(0, 5))
        
        self.batch_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Optional - for tracking purposes",
            font=FONTS['body'],
            height=40
        )
        self.batch_entry.pack(fill='x', pady=(0, 15))
        
        # Next Dose Due
        next_dose_label = ctk.CTkLabel(
            form_content,
            text="📅  Next Dose Due Date",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        next_dose_label.pack(anchor='w', pady=(0, 5))
        
        self.next_dose_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="YYYY-MM-DD (Leave empty if not applicable)",
            font=FONTS['body'],
            height=40
        )
        self.next_dose_entry.pack(fill='x', pady=(0, 5))
        
        # Help text
        help_text = ctk.CTkLabel(
            form_content,
            text="💡 Tip: Leave 'Next Dose Due' empty for single-dose vaccines",
            font=FONTS['small'],
            text_color=COLORS['text_muted']
        )
        help_text.pack(anchor='w')
        
        # Buttons
        btn_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        btn_frame.pack(fill='x')
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="✖  Cancel",
            command=self.on_closing,  # ✅ FIX: Use on_closing instead of destroy
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
            text="✓  Save Vaccination",
            command=self.handle_save,
            font=FONTS['body_bold'],
            height=50,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        save_btn.pack(side='right', fill='x', expand=True, padx=(10, 0))
    
    def on_closing(self):
        """Handle dialog close - with confirmation if form has data"""
        # Check if form has any data entered
        has_data = (
            self.date_entry.get() != get_current_date() or
            self.location_entry.get().strip() != "" or
            self.batch_entry.get().strip() != "" or
            self.next_dose_entry.get().strip() != ""
        )
        
        if has_data:
            # Ask for confirmation
            result = messagebox.askyesno(
                "Discard Changes?",
                "You have unsaved changes. Close anyway?",
                parent=self
            )
            if not result:
                return  # Don't close
        
        # Close the dialog properly
        self.grab_release()
        self.destroy()
    
    def handle_save(self):
        """Save new vaccination record"""
        # Get form data
        vaccine_name = self.vaccine_entry.get()
        date_administered = self.date_entry.get().strip()
        dose_number = self.dose_entry.get()
        location = self.location_entry.get().strip()
        batch_number = self.batch_entry.get().strip()
        next_dose_due = self.next_dose_entry.get().strip()
        
        # Validate required fields
        if not all([vaccine_name, date_administered, location]):
            messagebox.showerror(
                "Missing Information", 
                "Please fill in:\n• Vaccine Name\n• Date Administered\n• Location",
                parent=self
            )
            return
        
        # Validate date format
        if not is_valid_date(date_administered):
            messagebox.showerror(
                "Invalid Date", 
                "Date must be in YYYY-MM-DD format\nExample: 2024-03-15",
                parent=self
            )
            self.date_entry.focus()
            return
        
        # Validate next dose date if provided
        if next_dose_due and not is_valid_date(next_dose_due):
            messagebox.showerror(
                "Invalid Date", 
                "Next dose date must be in YYYY-MM-DD format\nExample: 2024-06-15",
                parent=self
            )
            self.next_dose_entry.focus()
            return
        
        # Create vaccination data
        vaccination_data = {
            'vaccine_name': vaccine_name,
            'date_administered': date_administered,
            'dose_number': dose_number,
            'location': location,
            'batch_number': batch_number if batch_number else None,
            'next_dose_due': next_dose_due if next_dose_due else None
        }
        
        # Save vaccination
        try:
            success, message = vaccination_manager.add_vaccination(
                self.patient_data.get('national_id'),
                vaccination_data
            )
            
            if success:
                messagebox.showinfo(
                    "Success", 
                    "✓ Vaccination record saved successfully!",
                    parent=self
                )
                # Refresh the parent view
                if self.on_success:
                    self.on_success()
                # Close dialog
                self.grab_release()
                self.destroy()
            else:
                messagebox.showerror(
                    "Save Failed", 
                    f"Could not save vaccination:\n{message}",
                    parent=self
                )
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"An error occurred:\n{str(e)}",
                parent=self
            )


