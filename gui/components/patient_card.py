"""
Patient Card Component - FIXED VERSION
Displays patient information in a card format
Location: gui/components/patient_card.py
"""
import customtkinter as ctk
from gui.styles import *


class PatientCard(ctk.CTkFrame):
    def __init__(self, parent, patient_data, on_emergency=None):
        """
        Initialize patient card
        
        Args:
            parent: Parent widget
            patient_data: Dictionary containing patient information
            on_emergency: Optional callback function for emergency button
        """
        super().__init__(parent, fg_color=COLORS['bg_medium'], corner_radius=RADIUS['lg'])
        
        self.patient_data = patient_data
        self.on_emergency = on_emergency  # Store callback
        
        self.create_ui()
    
    def create_ui(self):
        """Create the patient card UI"""
        # Main container with padding
        container = ctk.CTkFrame(self, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(container)
        
        # Basic info section
        self.create_basic_info(container)
        
        # Medical summary section
        self.create_medical_summary(container)
        
        # Emergency button (if callback provided)
        # if self.on_emergency:
        #     self.create_emergency_button(container)
    
    def create_header(self, parent):
        """Create patient header with photo and name"""
        header = ctk.CTkFrame(parent, fg_color='transparent')
        header.pack(fill='x', pady=(0, 15))
        
        # Photo placeholder
        photo_frame = ctk.CTkFrame(
            header,
            width=80,
            height=80,
            fg_color=COLORS['primary'],
            corner_radius=40  # Fixed: Use number instead of RADIUS['full']
        )
        photo_frame.pack(side='left', padx=(0, 15))
        photo_frame.pack_propagate(False)
        
        # Initials in photo
        initials = self.get_initials(self.patient_data.get('full_name', 'N/A'))
        initials_label = ctk.CTkLabel(
            photo_frame,
            text=initials,
            font=('Segoe UI', 28, 'bold'),
            text_color='white'
        )
        initials_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Name and ID
        info_frame = ctk.CTkFrame(header, fg_color='transparent')
        info_frame.pack(side='left', fill='both', expand=True)
        
        # Patient name
        name_label = ctk.CTkLabel(
            info_frame,
            text=self.patient_data.get('full_name', 'Unknown Patient'),
            font=FONTS['heading'],
            text_color=COLORS['text_primary'],
            anchor='w'
        )
        name_label.pack(anchor='w')
        
        # National ID
        id_label = ctk.CTkLabel(
            info_frame,
            text=f"📋 ID: {self.patient_data.get('national_id', 'N/A')}",
            font=FONTS['body'],
            text_color=COLORS['text_secondary'],
            anchor='w'
        )
        id_label.pack(anchor='w', pady=(2, 0))
    
    def create_basic_info(self, parent):
        """Create basic patient information grid"""
        info_frame = ctk.CTkFrame(parent, fg_color=COLORS['bg_light'], corner_radius=RADIUS['md'])
        info_frame.pack(fill='x', pady=(0, 15))
        
        # Info grid
        grid = ctk.CTkFrame(info_frame, fg_color='transparent')
        grid.pack(fill='x', padx=15, pady=15)
        
        # Configure grid
        grid.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Info items
        info_items = [
            ("🩸 Blood Type", self.patient_data.get('blood_type', 'N/A')),
            ("🎂 Age", f"{self.patient_data.get('age', 'N/A')} years"),
            ("⚧ Gender", self.patient_data.get('gender', 'N/A')),
            ("📞 Phone", self.patient_data.get('phone', 'N/A'))
        ]
        
        for i, (label, value) in enumerate(info_items):
            self.create_info_item(grid, label, value, i // 2, i % 2 * 2)
    
    def create_info_item(self, parent, label, value, row, col):
        """Create a single info item"""
        # Label
        label_widget = ctk.CTkLabel(
            parent,
            text=label,
            font=FONTS['small'],
            text_color=COLORS['text_secondary'],
            anchor='w'
        )
        label_widget.grid(row=row, column=col, sticky='w', padx=(0, 10), pady=5)
        
        # Value
        value_widget = ctk.CTkLabel(
            parent,
            text=str(value),
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary'],
            anchor='w'
        )
        value_widget.grid(row=row, column=col+1, sticky='w', pady=5)
    
    def create_medical_summary(self, parent):
        """Create medical summary section"""
        content = ctk.CTkFrame(parent, fg_color='transparent')
        content.pack(fill='x')
        
        # Allergies
        allergies = self.patient_data.get('allergies', [])
        if allergies:
            allergy_frame = ctk.CTkFrame(content, fg_color=COLORS['danger'], corner_radius=RADIUS['md'])
            allergy_frame.pack(fill='x', pady=(0, 8))
            
            allergy_text = "⚠️  ALLERGIES: " + ", ".join(allergies[:3])
            if len(allergies) > 3:
                allergy_text += f" (+{len(allergies)-3} more)"
            
            allergy_label = ctk.CTkLabel(
                allergy_frame,
                text=allergy_text,
                font=FONTS['body_bold'],
                text_color='white'
            )
            allergy_label.pack(padx=15, pady=10)
        
        # Chronic diseases
        chronic = self.patient_data.get('chronic_diseases', [])
        if chronic:
            chronic_text = "🏥 Chronic: " + ", ".join(chronic[:3])
            if len(chronic) > 3:
                chronic_text += f" (+{len(chronic)-3} more)"
            
            chronic_label = ctk.CTkLabel(
                content,
                text=chronic_text,
                font=FONTS['body'],
                text_color=COLORS['text_secondary'],
                anchor='w'
            )
            chronic_label.pack(anchor='w', pady=2)
        
        # Current medications - FIXED: Handle dictionaries
        medications = self.patient_data.get('current_medications', [])
        if medications:
            # Extract medication names from dictionaries
            if isinstance(medications[0], dict):
                # Medications are dictionaries with 'name' key
                med_names = [med.get('name', 'Unknown') for med in medications[:3]]
            else:
                # Medications are already strings
                med_names = medications[:3]
            
            med_text = "💊 Medications: " + ", ".join(med_names)
            if len(medications) > 3:
                med_text += f" (+{len(medications)-3} more)"
            
            med_label = ctk.CTkLabel(
                content,
                text=med_text,
                font=FONTS['body'],
                text_color=COLORS['text_secondary'],
                anchor='w'
            )
            med_label.pack(anchor='w', pady=2)
    
    def create_emergency_button(self, parent):
        """Create emergency card button"""
        button_frame = ctk.CTkFrame(parent, fg_color='transparent')
        button_frame.pack(fill='x', pady=(15, 0))
        
        emergency_btn = ctk.CTkButton(
            button_frame,
            text="🆘 View Emergency Card",
            command=self.on_emergency,
            font=FONTS['body_bold'],
            fg_color=COLORS['danger'],
            hover_color='#dc2626',
            height=40,
            corner_radius=RADIUS['md']
        )
        emergency_btn.pack(fill='x')
    
    def get_initials(self, full_name):
        """Get initials from full name"""
        try:
            if not full_name or full_name == 'N/A':
                return "?"
            
            parts = full_name.split()
            if len(parts) >= 2:
                return (parts[0][0] + parts[1][0]).upper()
            elif len(parts) == 1:
                return parts[0][0].upper()
            else:
                return "?"
        except:
            return "?"


# For backwards compatibility
class EnhancedPatientCard(PatientCard):
    """Alias for backwards compatibility"""
    pass