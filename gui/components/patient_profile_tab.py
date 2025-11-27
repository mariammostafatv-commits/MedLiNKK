"""
Patient profile tab - View and edit own profile
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from core.patient_manager import patient_manager


class PatientProfileTab(ctk.CTkFrame):
    """Patient's own profile view with edit capability"""
    
    def __init__(self, parent, patient_data, user_data):
        super().__init__(parent, fg_color='transparent')
        
        self.patient_data = patient_data
        self.user_data = user_data
        self.edit_mode = False
        
        print(f"🔍 Creating PatientProfileTab for: {patient_data.get('full_name', 'Unknown')}")
        
        self.create_ui()
    
    def create_ui(self):
        """Create profile tab UI"""
        # Scrollable container
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header with edit button
        header = ctk.CTkFrame(scroll_frame, fg_color=COLORS['bg_medium'], height=80)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)
        
        header_content = ctk.CTkFrame(header, fg_color='transparent')
        header_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        title_label = ctk.CTkLabel(
            header_content,
            text="👤  My Profile",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(side='left')
        
        self.edit_btn = ctk.CTkButton(
            header_content,
            text="✏️  Edit Profile",
            command=self.toggle_edit_mode,
            font=FONTS['body_bold'],
            height=45,
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_hover']
        )
        self.edit_btn.pack(side='right')
        
        # Profile card
        profile_card = ctk.CTkFrame(
            scroll_frame,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg']
        )
        profile_card.pack(fill='x', pady=(0, 20))
        
        profile_content = ctk.CTkFrame(profile_card, fg_color='transparent')
        profile_content.pack(fill='x', padx=30, pady=30)
        
        # Patient icon and basic info
        info_header = ctk.CTkFrame(profile_content, fg_color='transparent')
        info_header.pack(fill='x', pady=(0, 20))
        
        icon_label = ctk.CTkLabel(
            info_header,
            text="👤",
            font=('Segoe UI', 64)
        )
        icon_label.pack(side='left', padx=(0, 20))
        
        name_frame = ctk.CTkFrame(info_header, fg_color='transparent')
        name_frame.pack(side='left', fill='x', expand=True)
        
        name_label = ctk.CTkLabel(
            name_frame,
            text=self.patient_data.get('full_name', 'N/A'),
            font=('Segoe UI', 28, 'bold'),
            text_color=COLORS['text_primary'],
            anchor='w'
        )
        name_label.pack(anchor='w')
        
        id_label = ctk.CTkLabel(
            name_frame,
            text=f"National ID: {self.patient_data.get('national_id', 'N/A')}",
            font=FONTS['body'],
            text_color=COLORS['text_secondary'],
            anchor='w'
        )
        id_label.pack(anchor='w')
        
        # Divider
        ctk.CTkFrame(
            profile_content,
            height=1,
            fg_color=COLORS['bg_hover']
        ).pack(fill='x', pady=20)
        
        # Basic Information Section
        self.create_section_title(profile_content, "📋  Basic Information")
        
        basic_grid = ctk.CTkFrame(profile_content, fg_color='transparent')
        basic_grid.pack(fill='x', pady=(0, 20))
        
        # Row 1
        row1 = ctk.CTkFrame(basic_grid, fg_color='transparent')
        row1.pack(fill='x', pady=(0, 15))
        
        self.create_info_field(row1, "Date of Birth", self.patient_data.get('date_of_birth', 'N/A'), side='left', editable=False)
        self.create_info_field(row1, "Age", f"{self.patient_data.get('age', 'N/A')} years", side='left', editable=False)
        self.create_info_field(row1, "Gender", self.patient_data.get('gender', 'N/A'), side='left', editable=False)
        
        # Row 2
        row2 = ctk.CTkFrame(basic_grid, fg_color='transparent')
        row2.pack(fill='x', pady=(0, 15))
        
        self.create_info_field(row2, "Blood Type", self.patient_data.get('blood_type', 'N/A'), side='left', editable=False)
        self.phone_field = self.create_info_field(row2, "Phone", self.patient_data.get('phone', 'N/A'), side='left', editable=True)
        
        # Email
        self.email_field = self.create_info_field(basic_grid, "Email", self.patient_data.get('email', 'N/A'), editable=True)
        
        # Address
        self.address_field = self.create_info_field(basic_grid, "Address", self.patient_data.get('address', 'N/A'), editable=True)
        
        # Emergency Contact Section
        self.create_section_title(profile_content, "🆘  Emergency Contact")
        
        emergency = self.patient_data.get('emergency_contact', {})
        
        ec_grid = ctk.CTkFrame(profile_content, fg_color='transparent')
        ec_grid.pack(fill='x', pady=(0, 20))
        
        self.ec_name_field = self.create_info_field(ec_grid, "Name", emergency.get('name', 'N/A'), editable=True)
        
        ec_row = ctk.CTkFrame(ec_grid, fg_color='transparent')
        ec_row.pack(fill='x', pady=(15, 0))
        
        self.ec_relation_field = self.create_info_field(ec_row, "Relation", emergency.get('relation', 'N/A'), side='left', editable=True)
        self.ec_phone_field = self.create_info_field(ec_row, "Phone", emergency.get('phone', 'N/A'), side='left', editable=True)
        
        # Medical Alerts Section
        self.create_section_title(profile_content, "⚠️  Medical Alerts")
        
        alerts_frame = ctk.CTkFrame(
            profile_content,
            fg_color=COLORS['bg_light'],
            corner_radius=RADIUS['md']
        )
        alerts_frame.pack(fill='x', pady=(0, 20))
        
        alerts_content = ctk.CTkFrame(alerts_frame, fg_color='transparent')
        alerts_content.pack(fill='x', padx=20, pady=20)
        
        # Allergies
        allergies = self.patient_data.get('allergies', [])
        allergies_text = ", ".join(allergies) if allergies else "None reported"
        
        allergy_label = ctk.CTkLabel(
            alerts_content,
            text=f"🚫  Allergies: {allergies_text}",
            font=FONTS['body_bold'],
            text_color=COLORS['warning'] if allergies else COLORS['text_secondary'],
            anchor='w'
        )
        allergy_label.pack(fill='x', pady=(0, 10))
        
        # Chronic diseases
        chronic = self.patient_data.get('chronic_diseases', [])
        chronic_text = ", ".join(chronic) if chronic else "None reported"
        
        chronic_label = ctk.CTkLabel(
            alerts_content,
            text=f"🏥  Chronic Conditions: {chronic_text}",
            font=FONTS['body'],
            text_color=COLORS['info'] if chronic else COLORS['text_secondary'],
            anchor='w'
        )
        chronic_label.pack(fill='x')
        
        # Current Medications
        self.create_section_title(profile_content, "💊  Current Medications")
        
        meds = self.patient_data.get('current_medications', [])
        
        if meds:
            for med in meds:
                med_card = ctk.CTkFrame(
                    profile_content,
                    fg_color=COLORS['bg_light'],
                    corner_radius=RADIUS['md']
                )
                med_card.pack(fill='x', pady=5)
                
                med_content = ctk.CTkFrame(med_card, fg_color='transparent')
                med_content.pack(fill='x', padx=15, pady=15)
                
                med_name = ctk.CTkLabel(
                    med_content,
                    text=med.get('name', 'N/A'),
                    font=FONTS['body_bold'],
                    text_color=COLORS['text_primary'],
                    anchor='w'
                )
                med_name.pack(anchor='w')
                
                med_details = f"{med.get('dosage', '')} - {med.get('frequency', '')}"
                med_detail_label = ctk.CTkLabel(
                    med_content,
                    text=med_details,
                    font=FONTS['small'],
                    text_color=COLORS['text_secondary'],
                    anchor='w'
                )
                med_detail_label.pack(anchor='w')
        else:
            no_meds = ctk.CTkLabel(
                profile_content,
                text="No current medications",
                font=FONTS['body'],
                text_color=COLORS['text_muted']
            )
            no_meds.pack(pady=10)
        
        # Insurance Information
        self.create_section_title(profile_content, "🏦  Insurance Information")
        
        insurance = self.patient_data.get('insurance', {})
        
        if insurance:
            ins_frame = ctk.CTkFrame(
                profile_content,
                fg_color=COLORS['bg_light'],
                corner_radius=RADIUS['md']
            )
            ins_frame.pack(fill='x')
            
            ins_content = ctk.CTkFrame(ins_frame, fg_color='transparent')
            ins_content.pack(fill='x', padx=20, pady=20)
            
            ins_provider = ctk.CTkLabel(
                ins_content,
                text=f"Provider: {insurance.get('provider', 'N/A')}",
                font=FONTS['body'],
                text_color=COLORS['text_primary'],
                anchor='w'
            )
            ins_provider.pack(anchor='w', pady=2)
            
            ins_policy = ctk.CTkLabel(
                ins_content,
                text=f"Policy Number: {insurance.get('policy_number', 'N/A')}",
                font=FONTS['body'],
                text_color=COLORS['text_secondary'],
                anchor='w'
            )
            ins_policy.pack(anchor='w', pady=2)
            
            ins_expiry = ctk.CTkLabel(
                ins_content,
                text=f"Valid Until: {insurance.get('expiry', 'N/A')}",
                font=FONTS['small'],
                text_color=COLORS['text_muted'],
                anchor='w'
            )
            ins_expiry.pack(anchor='w', pady=2)
        else:
            no_ins = ctk.CTkLabel(
                profile_content,
                text="No insurance information",
                font=FONTS['body'],
                text_color=COLORS['text_muted']
            )
            no_ins.pack(pady=10)
        
        # Save button (hidden initially)
        self.save_frame = ctk.CTkFrame(scroll_frame, fg_color='transparent')
        
        save_btn = ctk.CTkButton(
            self.save_frame,
            text="💾  Save Changes",
            command=self.save_changes,
            font=FONTS['body_bold'],
            height=50,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        save_btn.pack(fill='x')
        
        print("✅ PatientProfileTab created successfully")
    
    def create_section_title(self, parent, text):
        """Create section title"""
        title = ctk.CTkLabel(
            parent,
            text=text,
            font=FONTS['subheading'],
            text_color=COLORS['text_primary'],
            anchor='w'
        )
        title.pack(anchor='w', pady=(20, 10))
    
    def create_info_field(self, parent, label, value, side=None, editable=False):
        """Create info field with optional edit capability"""
        container = ctk.CTkFrame(parent, fg_color='transparent')
        
        if side:
            container.pack(side=side, fill='x', expand=True, padx=(0, 20))
        else:
            container.pack(fill='x', pady=(0, 15))
        
        label_widget = ctk.CTkLabel(
            container,
            text=label,
            font=FONTS['small'],
            text_color=COLORS['text_muted'],
            anchor='w'
        )
        label_widget.pack(anchor='w', pady=(0, 5))
        
        if editable:
            entry = ctk.CTkEntry(
                container,
                font=FONTS['body'],
                height=40,
                state='disabled'
            )
            entry.pack(fill='x')
            entry.insert(0, value)
            return entry
        else:
            value_widget = ctk.CTkLabel(
                container,
                text=value,
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary'],
                anchor='w'
            )
            value_widget.pack(anchor='w')
            return None
    
    def toggle_edit_mode(self):
        """Toggle between view and edit mode"""
        self.edit_mode = not self.edit_mode
        
        if self.edit_mode:
            # Enable editing
            self.edit_btn.configure(text="❌  Cancel", fg_color=COLORS['danger'])
            
            # Enable entry fields
            for field in [self.phone_field, self.email_field, self.address_field,
                         self.ec_name_field, self.ec_relation_field, self.ec_phone_field]:
                if field:
                    field.configure(state='normal')
            
            # Show save button
            self.save_frame.pack(fill='x', pady=20)
        else:
            # Disable editing
            self.edit_btn.configure(text="✏️  Edit Profile", fg_color=COLORS['primary'])
            
            # Disable entry fields
            for field in [self.phone_field, self.email_field, self.address_field,
                         self.ec_name_field, self.ec_relation_field, self.ec_phone_field]:
                if field:
                    field.configure(state='disabled')
            
            # Hide save button
            self.save_frame.pack_forget()
    
    def save_changes(self):
        """Save profile changes"""
        try:
            # Get updated values
            updated_data = self.patient_data.copy()
            
            updated_data['phone'] = self.phone_field.get() if self.phone_field else updated_data.get('phone')
            updated_data['email'] = self.email_field.get() if self.email_field else updated_data.get('email')
            updated_data['address'] = self.address_field.get() if self.address_field else updated_data.get('address')
            
            # Update emergency contact
            updated_data['emergency_contact'] = {
                'name': self.ec_name_field.get() if self.ec_name_field else '',
                'relation': self.ec_relation_field.get() if self.ec_relation_field else '',
                'phone': self.ec_phone_field.get() if self.ec_phone_field else ''
            }
            
            # Save to database
            success = patient_manager.update_patient(
                self.patient_data.get('national_id'),
                updated_data
            )
            
            if success:
                messagebox.showinfo("Success", "Profile updated successfully!")
                self.patient_data = updated_data
                self.toggle_edit_mode()
            else:
                messagebox.showerror("Error", "Failed to update profile")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {str(e)}")