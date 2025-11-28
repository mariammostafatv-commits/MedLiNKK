"""
Family history dialog - Update family medical history
Location: gui/components/family_history_dialog.py
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from core.family_history_manager import family_history_manager


class FamilyHistoryDialog(ctk.CTkToplevel):
    """Dialog for updating family medical history"""
    
    def __init__(self, parent, patient_data, on_success):
        super().__init__(parent)
        
        self.patient_data = patient_data
        self.on_success = on_success
        
        # Load existing family history
        self.family_history = family_history_manager.get_family_history(
            patient_data.get('national_id')
        ) or {}
        
        # Configure window
        self.title("Family Medical History")
        self.geometry("800x850")
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
        """Create family history form"""
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header
        header = ctk.CTkFrame(main_frame, fg_color='transparent')
        header.pack(fill='x', pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header,
            text="👨‍👩‍👧‍👦  Family Medical History",
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
        form_content.pack(fill='both', expand=True, padx=25, pady=25)
        
        # FATHER SECTION
        father_frame = self.create_section(form_content, "👨  Father's Medical History")
        father_content = ctk.CTkFrame(father_frame, fg_color='transparent')
        father_content.pack(fill='x', padx=20, pady=15)
        
        father_data = self.family_history.get('father', {})
        
        # Father alive checkbox
        self.father_alive = ctk.CTkCheckBox(
            father_content,
            text="Father is alive",
            font=FONTS['body'],
            onvalue=True,
            offvalue=False,
            command=self.toggle_father_fields
        )
        self.father_alive.pack(anchor='w', pady=(0, 10))
        if father_data.get('alive', True):
            self.father_alive.select()
        
        # Age at death
        self.father_death_age = ctk.CTkEntry(
            father_content,
            placeholder_text="Age at death (if deceased)",
            font=FONTS['body'],
            height=40
        )
        self.father_death_age.pack(fill='x', pady=(0, 10))
        if father_data.get('age_at_death'):
            self.father_death_age.insert(0, str(father_data['age_at_death']))
        
        # Cause of death
        self.father_cause = ctk.CTkEntry(
            father_content,
            placeholder_text="Cause of death (if deceased)",
            font=FONTS['body'],
            height=40
        )
        self.father_cause.pack(fill='x', pady=(0, 10))
        if father_data.get('cause_of_death'):
            self.father_cause.insert(0, father_data['cause_of_death'])
        
        # Medical conditions
        conditions_label = ctk.CTkLabel(
            father_content,
            text="Medical Conditions (comma-separated):",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        conditions_label.pack(anchor='w', pady=(0, 5))
        
        self.father_conditions = ctk.CTkEntry(
            father_content,
            placeholder_text="e.g., Diabetes, Hypertension, Heart Disease",
            font=FONTS['body'],
            height=40
        )
        self.father_conditions.pack(fill='x')
        if father_data.get('medical_conditions'):
            self.father_conditions.insert(0, ', '.join(father_data['medical_conditions']))
        
        self.toggle_father_fields()
        
        # MOTHER SECTION
        mother_frame = self.create_section(form_content, "👩  Mother's Medical History")
        mother_content = ctk.CTkFrame(mother_frame, fg_color='transparent')
        mother_content.pack(fill='x', padx=20, pady=15)
        
        mother_data = self.family_history.get('mother', {})
        
        # Mother alive checkbox
        self.mother_alive = ctk.CTkCheckBox(
            mother_content,
            text="Mother is alive",
            font=FONTS['body'],
            onvalue=True,
            offvalue=False,
            command=self.toggle_mother_fields
        )
        self.mother_alive.pack(anchor='w', pady=(0, 10))
        if mother_data.get('alive', True):
            self.mother_alive.select()
        
        # Age
        self.mother_age = ctk.CTkEntry(
            mother_content,
            placeholder_text="Current age (if alive)",
            font=FONTS['body'],
            height=40
        )
        self.mother_age.pack(fill='x', pady=(0, 10))
        if mother_data.get('age'):
            self.mother_age.insert(0, str(mother_data['age']))
        
        # Medical conditions
        conditions_label = ctk.CTkLabel(
            mother_content,
            text="Medical Conditions (comma-separated):",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        conditions_label.pack(anchor='w', pady=(0, 5))
        
        self.mother_conditions = ctk.CTkEntry(
            mother_content,
            placeholder_text="e.g., Diabetes, Osteoporosis, Thyroid Issues",
            font=FONTS['body'],
            height=40
        )
        self.mother_conditions.pack(fill='x')
        if mother_data.get('medical_conditions'):
            self.mother_conditions.insert(0, ', '.join(mother_data['medical_conditions']))
        
        self.toggle_mother_fields()
        
        # GENETIC CONDITIONS
        genetic_frame = self.create_section(form_content, "🧬  Known Genetic Conditions")
        genetic_content = ctk.CTkFrame(genetic_frame, fg_color='transparent')
        genetic_content.pack(fill='x', padx=20, pady=15)
        
        genetic_label = ctk.CTkLabel(
            genetic_content,
            text="List any known genetic/hereditary conditions in the family:",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        genetic_label.pack(anchor='w', pady=(0, 5))
        
        self.genetic_conditions = ctk.CTkTextbox(
            genetic_content,
            font=FONTS['body'],
            height=60,
            wrap='word'
        )
        self.genetic_conditions.pack(fill='x')
        if self.family_history.get('genetic_conditions'):
            self.genetic_conditions.insert("1.0", ', '.join(self.family_history['genetic_conditions']))
        
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
            text="Save Family History",
            command=self.handle_save,
            font=FONTS['body_bold'],
            height=50,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        save_btn.pack(side='right', fill='x', expand=True, padx=(10, 0))
    
    def create_section(self, parent, title):
        """Create section with title"""
        section = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_light'],
            corner_radius=RADIUS['md']
        )
        section.pack(fill='x', pady=(0, 15))
        
        title_label = ctk.CTkLabel(
            section,
            text=title,
            font=FONTS['subheading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(anchor='w', padx=20, pady=(15, 0))
        
        return section
    
    def toggle_father_fields(self):
        """Enable/disable father fields based on alive status"""
        if self.father_alive.get():
            self.father_death_age.configure(state='disabled')
            self.father_cause.configure(state='disabled')
        else:
            self.father_death_age.configure(state='normal')
            self.father_cause.configure(state='normal')
    
    def toggle_mother_fields(self):
        """Enable/disable mother fields based on alive status"""
        if self.mother_alive.get():
            self.mother_age.configure(state='normal')
        else:
            self.mother_age.configure(state='disabled')
    
    def handle_save(self):
        """Save family medical history"""
        try:
            # Build family history data
            family_history_data = {}
            
            # Father data
            father_conditions = [c.strip() for c in self.father_conditions.get().split(',') if c.strip()]
            
            family_history_data['father'] = {
                'alive': self.father_alive.get()
            }
            
            if not self.father_alive.get():
                age_at_death = self.father_death_age.get().strip()
                if age_at_death:
                    try:
                        family_history_data['father']['age_at_death'] = int(age_at_death)
                    except ValueError:
                        messagebox.showerror("Invalid Input", "Father's age at death must be a number")
                        return
                
                cause = self.father_cause.get().strip()
                if cause:
                    family_history_data['father']['cause_of_death'] = cause
            
            if father_conditions:
                family_history_data['father']['medical_conditions'] = father_conditions
            
            # Mother data
            mother_conditions = [c.strip() for c in self.mother_conditions.get().split(',') if c.strip()]
            
            family_history_data['mother'] = {
                'alive': self.mother_alive.get()
            }
            
            if self.mother_alive.get():
                age = self.mother_age.get().strip()
                if age:
                    try:
                        family_history_data['mother']['age'] = int(age)
                    except ValueError:
                        messagebox.showerror("Invalid Input", "Mother's age must be a number")
                        return
            
            if mother_conditions:
                family_history_data['mother']['medical_conditions'] = mother_conditions
            
            # Genetic conditions
            genetic_text = self.genetic_conditions.get("1.0", "end-1c").strip()
            if genetic_text:
                family_history_data['genetic_conditions'] = [c.strip() for c in genetic_text.split(',') if c.strip()]
            
            # Save
            success, message = family_history_manager.update_family_history(
                self.patient_data.get('national_id'),
                family_history_data
            )
            
            if success:
                messagebox.showinfo("Success", "Family medical history updated successfully!")
                self.on_success()
                self.destroy()
            else:
                messagebox.showerror("Error", f"Failed to save family history: {message}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save family history: {str(e)}")