"""
Disability dialog - Update disability and special needs
Location: gui/components/disability_dialog.py
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from core.disability_manager import disability_manager


class DisabilityDialog(ctk.CTkToplevel):
    """Dialog for updating disability and special needs information"""
    
    def __init__(self, parent, patient_data, on_success):
        super().__init__(parent)
        
        self.patient_data = patient_data
        self.on_success = on_success
        
        # Load existing disability info
        self.disability_info = disability_manager.get_disability_info(
            patient_data.get('national_id')
        ) or {}
        
        # Configure window
        self.title("Disability & Special Needs")
        self.geometry("750x800")
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
        """Create disability information form"""
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header
        header = ctk.CTkFrame(main_frame, fg_color='transparent')
        header.pack(fill='x', pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header,
            text="♿  Disability & Special Needs",
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
        
        # Has Disability Checkbox
        self.has_disability = ctk.CTkCheckBox(
            form_content,
            text="Patient has a disability or special needs",
            font=FONTS['body_bold'],
            onvalue=True,
            offvalue=False,
            command=self.toggle_disability_fields
        )
        self.has_disability.pack(anchor='w', pady=(0, 20))
        if self.disability_info.get('has_disability'):
            self.has_disability.select()
        
        # Disability fields container
        self.disability_fields = ctk.CTkFrame(form_content, fg_color='transparent')
        self.disability_fields.pack(fill='both', expand=True)
        
        # Disability Type
        type_label = ctk.CTkLabel(
            self.disability_fields,
            text="🏷️  Disability Type",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        type_label.pack(anchor='w', pady=(0, 5))
        
        self.disability_type = ctk.CTkEntry(
            self.disability_fields,
            placeholder_text="e.g., Physical, Visual, Hearing, Cognitive",
            font=FONTS['body'],
            height=40
        )
        self.disability_type.pack(fill='x', pady=(0, 15))
        if self.disability_info.get('disability_type'):
            self.disability_type.insert(0, self.disability_info['disability_type'])
        
        # Mobility Aids
        mobility_label = ctk.CTkLabel(
            self.disability_fields,
            text="🦽  Mobility Aids Used",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        mobility_label.pack(anchor='w', pady=(0, 5))
        
        self.mobility_aids = ctk.CTkEntry(
            self.disability_fields,
            placeholder_text="e.g., Wheelchair, Walker, Cane (comma-separated)",
            font=FONTS['body'],
            height=40
        )
        self.mobility_aids.pack(fill='x', pady=(0, 15))
        if self.disability_info.get('mobility_aids'):
            self.mobility_aids.insert(0, ', '.join(self.disability_info['mobility_aids']))
        
        # Impairment Checkboxes
        impairment_frame = ctk.CTkFrame(
            self.disability_fields,
            fg_color=COLORS['bg_light'],
            corner_radius=RADIUS['md']
        )
        impairment_frame.pack(fill='x', pady=(0, 15))
        
        impairment_content = ctk.CTkFrame(impairment_frame, fg_color='transparent')
        impairment_content.pack(fill='x', padx=15, pady=15)
        
        impairment_title = ctk.CTkLabel(
            impairment_content,
            text="Impairment Types:",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        impairment_title.pack(anchor='w', pady=(0, 10))
        
        self.hearing_impairment = ctk.CTkCheckBox(
            impairment_content,
            text="Hearing Impairment",
            font=FONTS['body']
        )
        self.hearing_impairment.pack(anchor='w', pady=3)
        if self.disability_info.get('hearing_impairment'):
            self.hearing_impairment.select()
        
        self.visual_impairment = ctk.CTkCheckBox(
            impairment_content,
            text="Visual Impairment",
            font=FONTS['body']
        )
        self.visual_impairment.pack(anchor='w', pady=3)
        if self.disability_info.get('visual_impairment'):
            self.visual_impairment.select()
        
        self.cognitive_impairment = ctk.CTkCheckBox(
            impairment_content,
            text="Cognitive Impairment",
            font=FONTS['body']
        )
        self.cognitive_impairment.pack(anchor='w', pady=3)
        if self.disability_info.get('cognitive_impairment'):
            self.cognitive_impairment.select()
        
        # Communication Needs
        comm_label = ctk.CTkLabel(
            self.disability_fields,
            text="💬  Communication Needs",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        comm_label.pack(anchor='w', pady=(0, 5))
        
        self.communication_needs = ctk.CTkEntry(
            self.disability_fields,
            placeholder_text="e.g., Sign Language Interpreter, Large Print (comma-separated)",
            font=FONTS['body'],
            height=40
        )
        self.communication_needs.pack(fill='x', pady=(0, 15))
        if self.disability_info.get('communication_needs'):
            self.communication_needs.insert(0, ', '.join(self.disability_info['communication_needs']))
        
        # Accessibility Requirements
        access_label = ctk.CTkLabel(
            self.disability_fields,
            text="🚪  Accessibility Requirements",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        access_label.pack(anchor='w', pady=(0, 5))
        
        self.accessibility_requirements = ctk.CTkEntry(
            self.disability_fields,
            placeholder_text="e.g., Wheelchair Access, Elevator, Accessible Restroom (comma-separated)",
            font=FONTS['body'],
            height=40
        )
        self.accessibility_requirements.pack(fill='x', pady=(0, 15))
        if self.disability_info.get('accessibility_requirements'):
            self.accessibility_requirements.insert(0, ', '.join(self.disability_info['accessibility_requirements']))
        
        # Additional Notes
        notes_label = ctk.CTkLabel(
            self.disability_fields,
            text="📝  Additional Notes",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        notes_label.pack(anchor='w', pady=(0, 5))
        
        self.notes = ctk.CTkTextbox(
            self.disability_fields,
            font=FONTS['body'],
            height=80,
            wrap='word'
        )
        self.notes.pack(fill='x')
        if self.disability_info.get('notes'):
            self.notes.insert("1.0", self.disability_info['notes'])
        
        # Toggle initial state
        self.toggle_disability_fields()
        
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
            text="Save Information",
            command=self.handle_save,
            font=FONTS['body_bold'],
            height=50,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        save_btn.pack(side='right', fill='x', expand=True, padx=(10, 0))
    
    def toggle_disability_fields(self):
        """Enable/disable disability fields based on checkbox"""
        state = 'normal' if self.has_disability.get() else 'disabled'
        
        # Toggle all input fields
        for widget in self.disability_fields.winfo_children():
            if isinstance(widget, (ctk.CTkEntry, ctk.CTkTextbox)):
                widget.configure(state=state)
            elif isinstance(widget, ctk.CTkCheckBox):
                widget.configure(state=state)
            elif isinstance(widget, ctk.CTkFrame):
                # Handle nested frames (like impairment checkboxes)
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkFrame):
                        for subchild in child.winfo_children():
                            if isinstance(subchild, (ctk.CTkCheckBox, ctk.CTkEntry)):
                                subchild.configure(state=state)
    
    def handle_save(self):
        """Save disability information"""
        try:
            # Build disability data
            disability_data = {
                'has_disability': self.has_disability.get()
            }
            
            if self.has_disability.get():
                # Disability type
                disability_type = self.disability_type.get().strip()
                if disability_type:
                    disability_data['disability_type'] = disability_type
                
                # Mobility aids
                mobility_text = self.mobility_aids.get().strip()
                if mobility_text:
                    disability_data['mobility_aids'] = [m.strip() for m in mobility_text.split(',') if m.strip()]
                
                # Impairments
                disability_data['hearing_impairment'] = self.hearing_impairment.get()
                disability_data['visual_impairment'] = self.visual_impairment.get()
                disability_data['cognitive_impairment'] = self.cognitive_impairment.get()
                
                # Communication needs
                comm_text = self.communication_needs.get().strip()
                if comm_text:
                    disability_data['communication_needs'] = [c.strip() for c in comm_text.split(',') if c.strip()]
                
                # Accessibility requirements
                access_text = self.accessibility_requirements.get().strip()
                if access_text:
                    disability_data['accessibility_requirements'] = [a.strip() for a in access_text.split(',') if a.strip()]
                
                # Notes
                notes_text = self.notes.get("1.0", "end-1c").strip()
                if notes_text:
                    disability_data['notes'] = notes_text
            
            # Save
            success, message = disability_manager.update_disability_info(
                self.patient_data.get('national_id'),
                disability_data
            )
            
            if success:
                messagebox.showinfo("Success", "Disability information updated successfully!")
                self.on_success()
                self.destroy()
            else:
                messagebox.showerror("Error", f"Failed to save disability information: {message}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save disability information: {str(e)}")