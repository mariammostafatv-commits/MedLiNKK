"""
Doctor dashboard - Main interface for doctors
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.components import add_hospitalization_dialog, add_surgery_dialog, add_vaccination_dialog, disability_dialog, family_history_dialog
from gui.components.add_hospitalization_dialog import AddHospitalizationDialog
from gui.components.add_vaccination_dialog import AddVaccinationDialog
from gui.components.family_history_dialog import FamilyHistoryDialog
from gui.components.disability_dialog import DisabilityDialog
from gui.styles import *
from gui.components.sidebar import Sidebar
from gui.components.patient_card import PatientCard
from core.patient_manager import patient_manager
from core.search_engine import search_engine


class DoctorDashboard(ctk.CTkToplevel):
    """Main doctor dashboard window"""

    def __init__(self, parent, user_data):
        super().__init__(parent)

        self.parent = parent
        self.user_data = user_data
        self.current_patient = None

        # Configure window FIRST
        self.title("MedLink - Doctor Portal")
        self.geometry("1400x800")
        self.minsize(1200, 700)

        # Setup theme
        setup_theme()

        # Force window to show
        self.deiconify()
        self.lift()
        self.focus_force()

        # Small delay then create UI
        self.after(100, self.create_ui)

        # Center window after UI is created
        self.after(200, self.center_window)

    def center_window(self):
        """Center window on screen"""
        try:
            self.update_idletasks()
            width = self.winfo_width()
            height = self.winfo_height()
            x = (self.winfo_screenwidth() // 2) - (width // 2)
            y = (self.winfo_screenheight() // 2) - (height // 2)
            self.geometry(f'{width}x{height}+{x}+{y}')
        except Exception as e:
            print(f"Center window error: {e}")

    def create_ui(self):
        """Create dashboard interface"""
        try:
            print("Creating dashboard UI...")  # Debug

            # Main container
            main_container = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
            main_container.pack(fill='both', expand=True)

            print("Main container created")  # Debug

            # Sidebar
            try:
                self.sidebar = Sidebar(
                    main_container,
                    self.user_data,
                    self.handle_logout
                )
                self.sidebar.pack(side='left', fill='y')
                print("Sidebar created")  # Debug
            except Exception as e:
                print(f"Sidebar error: {e}")
                # Continue without sidebar

            # Main content area
            content_area = ctk.CTkFrame(
                main_container,
                fg_color=COLORS['bg_dark']
            )
            content_area.pack(side='right', fill='both', expand=True)

            print("Content area created")  # Debug

            # Top bar with search
            top_bar = ctk.CTkFrame(
                content_area,
                fg_color=COLORS['bg_medium'],
                height=80
            )
            top_bar.pack(fill='x', padx=20, pady=20)
            top_bar.pack_propagate(False)

            top_content = ctk.CTkFrame(top_bar, fg_color='transparent')
            top_content.pack(fill='both', expand=True, padx=20, pady=15)

            # Search section
            search_label = ctk.CTkLabel(
                top_content,
                text="🔍  Search Patient",
                font=FONTS['subheading'],
                text_color=COLORS['text_primary']
            )
            search_label.pack(side='left', padx=(0, 20))

            # Search entry
            self.search_entry = ctk.CTkEntry(
                top_content,
                placeholder_text="Enter National ID (14 digits)",
                font=FONTS['body'],
                height=45,
                width=400,
                corner_radius=RADIUS['md'],
                border_width=2
            )
            self.search_entry.pack(side='left', padx=(0, 15))
            self.search_entry.bind('<Return>', lambda e: self.handle_search())

            # Search button
            search_btn = ctk.CTkButton(
                top_content,
                text="Search",
                command=self.handle_search,
                font=FONTS['body_bold'],
                height=45,
                width=120,
                corner_radius=RADIUS['md'],
                fg_color=COLORS['primary'],
                hover_color=COLORS['primary_hover']
            )
            search_btn.pack(side='left')

            print("Search bar created")  # Debug

            # Content area with tabs
            self.content_frame = ctk.CTkFrame(
                content_area,
                fg_color='transparent'
            )
            self.content_frame.pack(
                fill='both', expand=True, padx=20, pady=(0, 20))

            print("Content frame created")  # Debug

            # Show welcome screen initially
            self.show_welcome_screen()

            print("✅ Dashboard UI created successfully!")  # Debug

            # Force update
            self.update()

        except Exception as e:
            print(f"❌ Error creating dashboard UI: {e}")
            import traceback
            traceback.print_exc()

            # Show error in window
            error_label = ctk.CTkLabel(
                self,
                text=f"Error loading dashboard:\n{str(e)}",
                font=FONTS['body'],
                text_color=COLORS['danger']
            )
            error_label.pack(expand=True)

    def show_welcome_screen(self):
        """Show welcome screen with quick stats"""
        try:
            print("Showing welcome screen...")  # Debug

            # Clear content
            for widget in self.content_frame.winfo_children():
                widget.destroy()

            welcome_container = ctk.CTkFrame(
                self.content_frame,
                fg_color='transparent'
            )
            welcome_container.pack(fill='both', expand=True)

            # Welcome message
            welcome_frame = ctk.CTkFrame(
                welcome_container,
                fg_color=COLORS['bg_medium'],
                corner_radius=RADIUS['lg'],
                height=200
            )
            welcome_frame.pack(fill='x', pady=(0, 20))
            welcome_frame.pack_propagate(False)

            welcome_content = ctk.CTkFrame(
                welcome_frame, fg_color='transparent')
            welcome_content.place(relx=0.5, rely=0.5, anchor='center')

            greeting = ctk.CTkLabel(
                welcome_content,
                text=f"Welcome back, {self.user_data.get('full_name', 'Doctor')}! 👋",
                font=('Segoe UI', 28, 'bold'),
                text_color=COLORS['text_primary']
            )
            greeting.pack()

            subtitle = ctk.CTkLabel(
                welcome_content,
                text=f"{self.user_data.get('specialization', 'Medical')} Department | {self.user_data.get('hospital', 'Hospital')}",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            subtitle.pack(pady=(10, 0))

            # Quick stats
            stats_container = ctk.CTkFrame(
                welcome_container,
                fg_color='transparent'
            )
            stats_container.pack(fill='both', expand=True)

            # Get stats
            try:
                all_patients = patient_manager.get_all_patients()
                total_patients = len(all_patients)
            except:
                total_patients = 0

            # Stats cards
            stats = [
                ("👥", "Total Patients", str(
                    total_patients), COLORS['primary']),
                ("📅", "Today's Appointments", "0", COLORS['secondary']),
                ("🆘", "Emergency Cases", "0", COLORS['danger']),
                ("📊", "Pending Reports", "0", COLORS['warning'])
            ]

            row_frame = ctk.CTkFrame(stats_container, fg_color='transparent')
            row_frame.pack(fill='x', pady=10)

            for icon, label, value, color in stats:
                self.create_stat_card(row_frame, icon, label, value, color)

            # Quick actions
            actions_frame = ctk.CTkFrame(
                welcome_container,
                fg_color=COLORS['bg_medium'],
                corner_radius=RADIUS['lg']
            )
            actions_frame.pack(fill='x', pady=20)

            actions_content = ctk.CTkFrame(
                actions_frame, fg_color='transparent')
            actions_content.pack(fill='x', padx=30, pady=30)

            actions_title = ctk.CTkLabel(
                actions_content,
                text="Quick Actions",
                font=FONTS['heading'],
                text_color=COLORS['text_primary']
            )
            actions_title.pack(anchor='w', pady=(0, 15))

            buttons_frame = ctk.CTkFrame(
                actions_content, fg_color='transparent')
            buttons_frame.pack(fill='x')

            action_buttons = [
                ("👤 Add New Patient", self.add_patient),
                ("📋 Add Visit Record", self.add_visit),
                ("🆘 Emergency Protocol", self.emergency_mode),
                ("📊 View Statistics", self.view_stats)
            ]

            for text, command in action_buttons:
                btn = ctk.CTkButton(
                    buttons_frame,
                    text=text,
                    command=command,
                    font=FONTS['body'],
                    height=50,
                    corner_radius=RADIUS['md'],
                    fg_color=COLORS['bg_light'],
                    hover_color=COLORS['bg_hover'],
                    anchor='w'
                )
                btn.pack(fill='x', pady=5)

            print("✅ Welcome screen created")  # Debug

        except Exception as e:
            print(f"❌ Error in welcome screen: {e}")
            import traceback
            traceback.print_exc()

    def create_stat_card(self, parent, icon, label, value, color):
        """Create statistics card"""
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg']
        )
        card.pack(side='left', fill='both', expand=True, padx=10)

        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=25, pady=25)

        icon_label = ctk.CTkLabel(
            content,
            text=icon,
            font=('Segoe UI', 36)
        )
        icon_label.pack(anchor='w')

        value_label = ctk.CTkLabel(
            content,
            text=value,
            font=('Segoe UI', 32, 'bold'),
            text_color=color
        )
        value_label.pack(anchor='w', pady=(10, 0))

        label_widget = ctk.CTkLabel(
            content,
            text=label,
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        label_widget.pack(anchor='w')

    def handle_search(self):
        """Handle patient search"""
        national_id = self.search_entry.get().strip()

        if not national_id:
            messagebox.showwarning(
                "Input Required", "Please enter a National ID")
            return

        # Search patient
        patient = search_engine.search_by_national_id(national_id)

        if not patient:
            messagebox.showerror(
                "Patient Not Found",
                f"No patient found with National ID: {national_id}"
            )
            return

        # Show patient profile
        self.show_patient_profile(patient)
    def show_patient_profile(self, patient):
        """Display patient profile with all enhanced features"""
        try:
            self.current_patient = patient
            
            # Clear content
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            
            # Create tabview
            tabview = ctk.CTkTabview(
                self.content_frame,
                corner_radius=RADIUS['lg'],
                fg_color=COLORS['bg_medium'],
                segmented_button_fg_color=COLORS['bg_light'],
                segmented_button_selected_color=COLORS['primary'],
                segmented_button_unselected_color=COLORS['bg_light']
            )
            tabview.pack(fill='both', expand=True)
            
            # ========================================
            # TAB 1: PROFILE (Enhanced Patient Card)
            # ========================================
            tabview.add("Profile")
            
            profile_scroll = ctk.CTkScrollableFrame(
                tabview.tab("Profile"),
                fg_color='transparent'
            )
            profile_scroll.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Enhanced Patient Card (Phase 3 - with badges)
            from gui.components.patient_card import PatientCard
            
            patient_card = PatientCard(profile_scroll, patient)
            patient_card.pack(fill='both', expand=True)
            
            # ========================================
            # TAB 2: MEDICAL PROFILE (NEW - Phase 3)
            # ========================================
            # This tab includes action buttons for:
            # - Add Surgery
            # - Add Hospitalization
            # - Add Vaccination
            # - Update Family History
            # - Update Disability Info
            tabview.add("Medical Profile")
            
            from gui.components.medical_profile_tab import MedicalProfileTab
            
            self.medical_profile_tab = MedicalProfileTab(
                tabview.tab("Medical Profile"),
                patient,
                self.user_data  # Doctor data
            )
            self.medical_profile_tab.pack(fill='both', expand=True, padx=10, pady=10)
            
            # ========================================
            # TAB 3: MEDICAL HISTORY (with Timeline option)
            # ========================================
            tabview.add("Medical History")
            
            from gui.components.history_tab import HistoryTab
            
            self.history_tab = HistoryTab(
                tabview.tab("Medical History"),
                patient,
                self.user_data,
                self.show_add_visit_dialog
            )
            self.history_tab.pack(fill='both', expand=True, padx=10, pady=10)
            
            # ========================================
            # TAB 4: LAB RESULTS (Enhanced - Phase 5)
            # ========================================
            tabview.add("Lab Results")
            
            from gui.components.lab_results_manager import EnhancedLabResultsManager
            
            self.lab_tab = EnhancedLabResultsManager(
                tabview.tab("Lab Results"),
                patient,
                is_doctor=True  # Shows "Add Lab Result" button
            )
            self.lab_tab.pack(fill='both', expand=True, padx=10, pady=10)
            
            # ========================================
            # TAB 5: IMAGING (Enhanced - Phase 5)
            # ========================================
            tabview.add("Imaging")
            
            from gui.components.imaging_results_manager import EnhancedImagingResultsManager
            
            self.imaging_tab = EnhancedImagingResultsManager(
                tabview.tab("Imaging"),
                patient,
                is_doctor=True  # Shows "Add Imaging" button
            )
            self.imaging_tab.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Set default tab to Medical Profile (most important)
            tabview.set("Medical Profile")
        
        except Exception as e:
            print(f"Error showing patient profile: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Could not load patient profile: {str(e)}")
            """Display patient profile"""
            try:
                self.current_patient = patient
                
                # Clear content
                for widget in self.content_frame.winfo_children():
                    widget.destroy()
                
                # Create tabview
                tabview = ctk.CTkTabview(
                    self.content_frame,
                    corner_radius=RADIUS['lg'],
                    fg_color=COLORS['bg_medium'],
                    segmented_button_fg_color=COLORS['bg_light'],
                    segmented_button_selected_color=COLORS['primary'],
                    segmented_button_unselected_color=COLORS['bg_light']
                )
                tabview.pack(fill='both', expand=True)
                
                # Add tabs
                tabview.add("Profile")
                # Buttons to launch dialogs:
                # add_surgery_dialog.AddSurgeryDialog()
                # add_hospitalization_dialog.AddHospitalizationDialog()
                # add_vaccination_dialog.AddVaccinationDialog()
                # family_history_dialog.FamilyHistoryDialog()
                # disability_dialog.DisabilityDialog()
                tabview.add("Medical History")
                tabview.add("Lab Results")
                tabview.add("Imaging")
                
                # Profile tab
                profile_scroll = ctk.CTkScrollableFrame(
                    tabview.tab("Profile"),
                    fg_color='transparent'
                )
                profile_scroll.pack(fill='both', expand=True, padx=10, pady=10)
                
                # Patient card WITH emergency callback
                patient_card = PatientCard(profile_scroll, patient, on_emergency=self.show_emergency_card)
                patient_card.pack(fill='both', expand=True)
                
                # Medical History tab
                from gui.components.history_tab import HistoryTab
                
                self.history_tab = HistoryTab(
                    tabview.tab("Medical History"),
                    patient,
                    self.user_data,
                    self.show_add_visit_dialog
                )
                self.history_tab.pack(fill='both', expand=True, padx=10, pady=10)
                
                # Lab Results tab
                from gui.components.lab_results_tab import LabResultsTab
                
                self.lab_tab = LabResultsTab(
                    tabview.tab("Lab Results"),
                    patient,
                    self.user_data,
                    is_doctor=True
                )
                self.lab_tab.pack(fill='both', expand=True, padx=10, pady=10)
                
                # Imaging tab
                from gui.components.imaging_tab import ImagingTab
                
                self.imaging_tab = ImagingTab(
                    tabview.tab("Imaging"),
                    patient,
                    self.user_data,
                    is_doctor=True
                )
                self.imaging_tab.pack(fill='both', expand=True, padx=10, pady=10)
            
            except Exception as e:
                print(f"Error showing patient profile: {e}")
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Could not load patient profile: {str(e)}")

    def show_emergency_card(self):
        """Show emergency card for current patient"""
        if not self.current_patient:
            messagebox.showwarning("No Patient", "Please select a patient first")
            return
        
        from gui.components.emergency_dialog import EmergencyDialog
        dialog = EmergencyDialog(self, self.current_patient)
        dialog.wait_window()
    def show_add_visit_dialog(self):
        """Show add visit dialog"""
        if not self.current_patient:
            messagebox.showwarning("No Patient", "Please select a patient first")
            return

        from gui.components.add_visit_dialog import AddVisitDialog

        dialog = AddVisitDialog(
            self,
            self.current_patient,
            self.user_data,
            self.on_visit_added
        )
        dialog.wait_window()


    def on_visit_added(self):
        """Callback after visit is added"""
        # Refresh history tab
        if hasattr(self, 'history_tab'):
            self.history_tab.refresh()

    def add_patient(self):
        """Add new patient - placeholder"""
        messagebox.showinfo(
            "Coming Soon", "Add Patient feature coming in Phase 4!")

    def add_visit(self):
        """Add visit record - placeholder"""
        if not self.current_patient:
            messagebox.showwarning(
                "No Patient", "Please select a patient first")
            return
        messagebox.showinfo(
            "Coming Soon", "Add Visit feature coming in Phase 3!")

    def emergency_mode(self):
        """Emergency mode - placeholder"""
        messagebox.showinfo(
            "Coming Soon", "Emergency Protocol coming in Phase 6!")

    def view_stats(self):
        """View statistics - placeholder"""
        messagebox.showinfo(
            "Coming Soon", "Statistics Dashboard coming in Phase 6!")

    def show_add_visit_dialog(self):
        """Show add visit dialog"""
        if not self.current_patient:
            messagebox.showwarning(
                "No Patient", "Please select a patient first")
            return

        from gui.components.add_visit_dialog import AddVisitDialog

        dialog = AddVisitDialog(
            self,
            self.current_patient,
            self.user_data,
            self.on_visit_added
        )
        dialog.wait_window()

    def on_visit_added(self):
        """Callback after visit is added"""
        # Refresh history tab
        if hasattr(self, 'history_tab'):
            self.history_tab.refresh()

    def handle_logout(self):
        """Handle logout"""
        result = messagebox.askyesno(
            "Confirm Logout",
            "Are you sure you want to logout?"
        )

        if result:
            self.destroy()

    def show_emergency_card(self):
        """Show emergency card for current patient"""
        if not self.current_patient:
            messagebox.showwarning("No Patient", "Please select a patient first")
            return
        
        from gui.components.emergency_dialog import EmergencyDialog
        dialog = EmergencyDialog(self, self.current_patient)
        dialog.wait_window()
if __name__ == "__main__":
    # Test dashboard
    setup_theme()

    test_user = {
        'full_name': 'Dr. Ahmed Mohamed',
        'specialization': 'Cardiology',
        'hospital': 'Cairo University Hospital'
    }

    app = ctk.CTk()
    app.withdraw()
    dashboard = DoctorDashboard(app, test_user)
    dashboard.mainloop()
