"""
Patient dashboard - Enhanced with Phase 8 features
Main interface for patients with Emergency Directives and Lifestyle management
Location: gui/patient_dashboard.py
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from gui.components.patient_profile_tab import PatientProfileTab
from gui.components.patient_medical_history import PatientMedicalHistory
from gui.components.lab_results_tab import LabResultsTab
from gui.components.imaging_tab import ImagingTab
from gui.components.emergency_directives_manager import EmergencyDirectivesManager
from gui.components.lifestyle_manager import LifestyleManager
from core.patient_manager import patient_manager


class PatientDashboard(ctk.CTkToplevel):
    """Main patient dashboard window - Enhanced with Phase 8"""

    def __init__(self, parent, user_data):
        super().__init__(parent)

        self.parent = parent
        self.user_data = user_data
        self.patient_data = None

        # Configure window
        self.title("MedLink - Patient Portal")
        self.geometry("1400x800")
        self.minsize(1200, 700)

        # Setup theme
        setup_theme()

        # Load patient data
        self.load_patient_data()

        # Force window to show
        self.deiconify()
        self.lift()
        self.focus_force()

        # Create UI after small delay
        self.after(100, self.create_ui)

        # Center window
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

    def load_patient_data(self):
        """Load patient data from national ID"""
        try:
            print(f"Loading patient data for: {self.user_data}")

            # Extract national ID from user data
            national_id = self.user_data.get('national_id')

            if not national_id:
                messagebox.showerror(
                    "Error", "Could not find patient National ID")
                self.destroy()
                return

            # Get patient data
            self.patient_data = patient_manager.get_patient_by_id(
                national_id)

            if not self.patient_data:
                messagebox.showerror(
                    "Error", "Could not load patient data")
                self.destroy()
                return

            print(f"✅ Patient data loaded: {
                  self.patient_data.get('full_name')}")

        except Exception as e:
            print(f"Error loading patient data: {e}")
            messagebox.showerror("Error", f"Failed to load patient data: {
                                 str(e)}")
            self.destroy()

    def create_ui(self):
        """Create patient dashboard UI with Phase 8 enhancements"""
        try:
            print("Creating patient dashboard UI...")

            # Main container
            main_container = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
            main_container.pack(fill='both', expand=True)

            # Top bar
            top_bar = ctk.CTkFrame(
                main_container,
                fg_color=COLORS['bg_medium'],
                height=80
            )
            top_bar.pack(fill='x', padx=20, pady=(20, 10))
            top_bar.pack_propagate(False)

            top_content = ctk.CTkFrame(top_bar, fg_color='transparent')
            top_content.pack(fill='both', expand=True, padx=20, pady=15)

            # Greeting
            greeting_label = ctk.CTkLabel(
                top_content,
                text=f"Welcome, {self.patient_data.get('full_name', 'Patient')} 👋",
                font=('Segoe UI', 22, 'bold'),
                text_color=COLORS['text_primary']
            )
            greeting_label.pack(side='left')

            # Emergency button
            emergency_btn = ctk.CTkButton(
                top_content,
                text="🆘  Emergency Card",
                command=self.show_emergency_card,
                font=FONTS['body_bold'],
                height=45,
                fg_color=COLORS['danger'],
                hover_color='#dc2626'
            )
            emergency_btn.pack(side='right')

            print("✅ Top bar created")

            # Content area
            content_area = ctk.CTkFrame(
                main_container, fg_color='transparent')
            content_area.pack(fill='both', expand=True, padx=20, pady=(0, 20))

            # Tab view
            self.tabview = ctk.CTkTabview(
                content_area,
                corner_radius=RADIUS['lg'],
                fg_color=COLORS['bg_medium'],
                segmented_button_fg_color=COLORS['bg_light'],
                segmented_button_selected_color=COLORS['primary'],
                segmented_button_unselected_color=COLORS['bg_light']
            )
            self.tabview.pack(fill='both', expand=True)

            print("✅ Tabview created")

            # ========================================
            # TAB 1: MY PROFILE
            # ========================================
            self.tabview.add("My Profile")

            try:
                print("Creating Profile tab...")
                self.profile_tab = PatientProfileTab(
                    self.tabview.tab("My Profile"),
                    self.patient_data,
                    self.user_data
                )
                self.profile_tab.pack(
                    fill='both', expand=True, padx=10, pady=10)
                print("✅ Profile tab created")
            except Exception as e:
                print(f"❌ Error creating Profile tab: {e}")
                import traceback
                traceback.print_exc()

            # ========================================
            # TAB 2: MEDICAL HISTORY (View-Only)
            # ========================================
            self.tabview.add("Medical History")

            try:
                print("Creating Medical History tab...")
                self.history_tab = PatientMedicalHistory(
                    self.tabview.tab("Medical History"),
                    self.patient_data
                )
                self.history_tab.pack(
                    fill='both', expand=True, padx=10, pady=10)
                print("✅ Medical History tab created")
            except Exception as e:
                print(f"❌ Error creating Medical History tab: {e}")
                import traceback
                traceback.print_exc()

            # ========================================
            # TAB 3: EMERGENCY DIRECTIVES (NEW - Phase 8!)
            # ========================================
            self.tabview.add("Emergency Directives")

            try:
                print("Creating Emergency Directives tab...")
                self.directives_tab = EmergencyDirectivesManager(
                    self.tabview.tab("Emergency Directives"),
                    self.patient_data
                )
                self.directives_tab.pack(
                    fill='both', expand=True, padx=10, pady=10)
                print("✅ Emergency Directives tab created")
            except Exception as e:
                print(f"❌ Error creating Emergency Directives tab: {e}")
                import traceback
                traceback.print_exc()

            # ========================================
            # TAB 4: LIFESTYLE & HABITS (NEW - Phase 8!)
            # ========================================
            self.tabview.add("Lifestyle & Habits")

            try:
                print("Creating Lifestyle tab...")
                self.lifestyle_tab = LifestyleManager(
                    self.tabview.tab("Lifestyle & Habits"),
                    self.patient_data
                )
                self.lifestyle_tab.pack(
                    fill='both', expand=True, padx=10, pady=10)
                print("✅ Lifestyle tab created")
            except Exception as e:
                print(f"❌ Error creating Lifestyle tab: {e}")
                import traceback
                traceback.print_exc()

            # ========================================
            # TAB 5: LAB RESULTS
            # ========================================
            self.tabview.add("Lab Results")

            try:
                print("Creating Lab Results tab...")
                self.lab_tab = LabResultsTab(
                    self.tabview.tab("Lab Results"),
                    self.patient_data,
                    is_doctor=False
                )
                self.lab_tab.pack(fill='both', expand=True, padx=10, pady=10)
                print("✅ Lab Results tab created")
            except Exception as e:
                print(f"❌ Error creating Lab Results tab: {e}")
                import traceback
                traceback.print_exc()

            # ========================================
            # TAB 6: IMAGING RESULTS
            # ========================================
            self.tabview.add("Imaging Results")

            try:
                print("Creating Imaging Results tab...")
                self.imaging_tab = ImagingTab(
                    self.tabview.tab("Imaging Results"),
                    self.patient_data,
                    is_doctor=False
                )
                self.imaging_tab.pack(
                    fill='both', expand=True, padx=10, pady=10)
                print("✅ Imaging Results tab created")
            except Exception as e:
                print(f"❌ Error creating Imaging Results tab: {e}")
                import traceback
                traceback.print_exc()

            print("✅ Patient dashboard UI created successfully with Phase 8 features!")

        except Exception as e:
            print(f"Error creating patient dashboard: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to create dashboard: {
                                 str(e)}")

    def show_emergency_card(self):
        """Show emergency card dialog"""
        try:
            from gui.components.emergency_dialog import EmergencyDialog
            dialog = EmergencyDialog(self, self.patient_data)
            dialog.wait_window()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show emergency card: {
                                 str(e)}")

    def logout(self):
        """Logout and return to login screen"""
        self.destroy()
        self.parent.deiconify()
