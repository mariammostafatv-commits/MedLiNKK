"""
Patient dashboard - Complete interface for patients
"""
import customtkinter as ctk
import os
from tkinter import messagebox
from gui.styles import *
from gui.components.patient_profile_tab import PatientProfileTab
from gui.components.my_history_tab import MyHistoryTab
from gui.components.link_accounts_dialog import LinkAccountsDialog
from core.patient_manager import patient_manager
from gui.components.lab_results_tab import LabResultsTab
from gui.components.imaging_tab import ImagingTab


class PatientDashboard(ctk.CTkToplevel):
    """Main patient dashboard window"""

    def __init__(self, parent, user_data):
        super().__init__(parent)

        self.parent = parent
        self.user_data = user_data

        # Get patient data
        self.patient_data = patient_manager.get_patient_by_id(
            user_data.get('national_id')
        )
        
        # Debug: Check if patient data exists
        print(f"🔍 Loading patient dashboard for: {user_data.get('national_id')}")
        print(f"Patient data found: {self.patient_data is not None}")
        
        if not self.patient_data:
            print("❌ ERROR: No patient data found!")
            messagebox.showerror(
                "Error",
                "Could not load patient information. Please contact support."
            )
            self.destroy()
            return

        # Configure window
        self.title("MedLink - Patient Portal")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # Setup theme
        setup_theme()

        # Force window to show
        self.deiconify()
        self.lift()
        self.focus_force()

        # Create UI
        self.after(100, self.create_ui)
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
        """Create patient dashboard interface"""
        try:
            print("🔍 Starting patient dashboard UI creation...")
            print(f"Patient data: {self.patient_data.get('full_name', 'Unknown')}")
            
            # Main container
            main_container = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
            main_container.pack(fill='both', expand=True)

            # Sidebar
            sidebar = self.create_sidebar(main_container)
            sidebar.pack(side='left', fill='y')

            # Main content area
            content_area = ctk.CTkFrame(
                main_container,
                fg_color=COLORS['bg_dark']
            )
            content_area.pack(side='right', fill='both', expand=True)

            # Top bar
            top_bar = ctk.CTkFrame(
                content_area,
                fg_color=COLORS['bg_medium'],
                height=80
            )
            top_bar.pack(fill='x', padx=20, pady=20)
            top_bar.pack_propagate(False)

            top_content = ctk.CTkFrame(top_bar, fg_color='transparent')
            top_content.pack(fill='both', expand=True, padx=20, pady=15)

            # Greeting
            greeting_label = ctk.CTkLabel(
                top_content,
                text=f"Welcome, {self.patient_data.get('full_name', 'Patient')}! 👋",
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

            # Tab view
            self.tabview = ctk.CTkTabview(
                content_area,
                corner_radius=RADIUS['lg'],
                fg_color=COLORS['bg_medium'],
                segmented_button_fg_color=COLORS['bg_light'],
                segmented_button_selected_color=COLORS['primary'],
                segmented_button_unselected_color=COLORS['bg_light']
            )
            self.tabview.pack(fill='both', expand=True, padx=20, pady=(0, 20))

            print("✅ Tabview created")

            # Add tabs
            self.tabview.add("My Profile")
            self.tabview.add("Medical History")
            self.tabview.add("Lab Results")
            self.tabview.add("Imaging Results")

            print("✅ Tabs added")

            # My Profile tab
            try:
                print("Creating Profile tab...")
                self.profile_tab = PatientProfileTab(
                    self.tabview.tab("My Profile"),
                    self.patient_data,
                    self.user_data
                )
                self.profile_tab.pack(fill='both', expand=True, padx=10, pady=10)
                print("✅ Profile tab created")
            except Exception as e:
                print(f"❌ Error creating Profile tab: {e}")
                import traceback
                traceback.print_exc()

            # Medical History tab
            try:
                print("Creating Medical History tab...")
                self.history_tab = MyHistoryTab(
                    self.tabview.tab("Medical History"),
                    self.patient_data
                )
                self.history_tab.pack(fill='both', expand=True, padx=10, pady=10)
                print("✅ Medical History tab created")
            except Exception as e:
                print(f"❌ Error creating Medical History tab: {e}")
                import traceback
                traceback.print_exc()

            # Lab Results tab
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

            # Imaging Results tab
            try:
                print("Creating Imaging Results tab...")
                self.imaging_tab = ImagingTab(
                    self.tabview.tab("Imaging Results"),
                    self.patient_data,
                    is_doctor=False
                )
                self.imaging_tab.pack(fill='both', expand=True, padx=10, pady=10)
                print("✅ Imaging Results tab created")
            except Exception as e:
                print(f"❌ Error creating Imaging Results tab: {e}")
                import traceback
                traceback.print_exc()

            print("✅ Patient dashboard UI created successfully!")
            self.update()

        except Exception as e:
            print(f"❌ Error creating patient dashboard: {e}")
            import traceback
            traceback.print_exc()


    def create_sidebar(self, parent):
        """Create sidebar"""
        sidebar = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_medium'],
            corner_radius=0,
            width=260
        )
        sidebar.pack_propagate(False)

        # Header
        header_frame = ctk.CTkFrame(sidebar, fg_color='transparent')
        header_frame.pack(fill='x', padx=20, pady=(30, 20))

        logo_label = ctk.CTkLabel(
            header_frame,
            text="🏥",
            font=('Segoe UI', 36)
        )
        logo_label.pack()

        app_name = ctk.CTkLabel(
            header_frame,
            text="MedLink",
            font=('Segoe UI', 20, 'bold'),
            text_color=COLORS['text_primary']
        )
        app_name.pack(pady=(5, 0))

        # Divider
        ctk.CTkFrame(
            sidebar,
            height=1,
            fg_color=COLORS['bg_hover']
        ).pack(fill='x', padx=20, pady=20)

        # User card
        user_card = ctk.CTkFrame(
            sidebar,
            fg_color=COLORS['bg_light'],
            corner_radius=RADIUS['md']
        )
        user_card.pack(fill='x', padx=20, pady=(0, 30))

        user_content = ctk.CTkFrame(user_card, fg_color='transparent')
        user_content.pack(fill='x', padx=15, pady=15)

        icon = ctk.CTkLabel(
            user_content,
            text="👤",
            font=('Segoe UI', 32)
        )
        icon.pack()

        name_label = ctk.CTkLabel(
            user_content,
            text=self.patient_data.get('full_name', 'Patient'),
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        name_label.pack(pady=(5, 0))

        id_label = ctk.CTkLabel(
            user_content,
            text=f"ID: {self.patient_data.get('national_id', 'N/A')[:8]}...",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        id_label.pack()

        # Quick info
        info_frame = ctk.CTkFrame(sidebar, fg_color='transparent')
        info_frame.pack(fill='x', padx=20, pady=(0, 20))

        self.create_info_item(
            info_frame, "🩸", self.patient_data.get('blood_type', 'N/A'))
        self.create_info_item(
            info_frame, "🎂", f"{self.patient_data.get('age', 'N/A')} years")

        # Action buttons
        nav_frame = ctk.CTkFrame(sidebar, fg_color='transparent')
        nav_frame.pack(fill='x', padx=20)

        link_btn = ctk.CTkButton(
            nav_frame,
            text="🔗  Link Accounts",
            command=self.show_link_accounts,
            font=FONTS['body'],
            height=45,
            fg_color=COLORS['bg_light'],
            hover_color=COLORS['bg_hover'],
            anchor='w'
        )
        link_btn.pack(fill='x', pady=5)

        download_btn = ctk.CTkButton(
            nav_frame,
            text="💾  Download Records",
            command=self.download_records,
            font=FONTS['body'],
            height=45,
            fg_color=COLORS['bg_light'],
            hover_color=COLORS['bg_hover'],
            anchor='w'
        )
        download_btn.pack(fill='x', pady=5)

        # Spacer
        ctk.CTkFrame(nav_frame, fg_color='transparent').pack(expand=True)

        # Logout
        logout_btn = ctk.CTkButton(
            sidebar,
            text="🚪  Logout",
            command=self.handle_logout,
            font=FONTS['body'],
            fg_color='transparent',
            hover_color=COLORS['danger'],
            height=45,
            anchor='w'
        )
        logout_btn.pack(fill='x', padx=20, pady=20, side='bottom')

        return sidebar

    def create_info_item(self, parent, icon, value):
        """Create info item in sidebar"""
        item = ctk.CTkFrame(
            parent, fg_color=COLORS['bg_light'], corner_radius=RADIUS['sm'])
        item.pack(fill='x', pady=5)

        content = ctk.CTkFrame(item, fg_color='transparent')
        content.pack(fill='x', padx=10, pady=10)

        icon_label = ctk.CTkLabel(
            content,
            text=icon,
            font=('Segoe UI', 20)
        )
        icon_label.pack(side='left', padx=(0, 10))

        value_label = ctk.CTkLabel(
            content,
            text=value,
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        value_label.pack(side='left')

    def show_emergency_card(self):
        """Show emergency card"""
        from gui.components.emergency_dialog import EmergencyDialog
        dialog = EmergencyDialog(self, self.patient_data)
        dialog.wait_window()

    def show_link_accounts(self):
        """Show link accounts dialog"""
        dialog = LinkAccountsDialog(
            self,
            self.patient_data,
            self.on_accounts_linked
        )
        dialog.wait_window()

    def on_accounts_linked(self):
        """Callback after accounts are linked"""
        # Refresh patient data
        self.patient_data = patient_manager.get_patient_by_id(
            self.user_data.get('national_id')
        )

    def download_records(self):
        """Download complete medical records as PDF"""
        try:
            from tkinter import filedialog
            from utils.pdf_generator import generate_medical_record_pdf
            from core.patient_manager import patient_manager
            
            # Get all data
            national_id = self.patient_data.get('national_id')
            visits = patient_manager.get_patient_visits(national_id)
            lab_results = patient_manager.get_patient_lab_results(national_id)
            imaging = patient_manager.get_patient_imaging(national_id)
            
            # Ask where to save
            default_filename = f"Medical_Records_{self.patient_data.get('full_name', 'Patient').replace(' ', '_')}.pdf"
            
            file_path = filedialog.asksaveasfilename(
                title="Save Medical Records",
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
                initialfile=default_filename
            )
            
            if not file_path:
                return
            
            # Generate PDF
            success = generate_medical_record_pdf(
                self.patient_data,
                visits,
                lab_results,
                imaging,
                file_path
            )
            
            if success:
                messagebox.showinfo(
                    "Success",
                    f"Medical records saved successfully!\n\n{file_path}"
                )
                
                # Ask if user wants to open
                if messagebox.askyesno("Open File", "Would you like to open the PDF now?"):
                    import platform
                    import subprocess
                    
                    if platform.system() == 'Windows':
                        os.startfile(file_path)
                    elif platform.system() == 'Darwin':
                        subprocess.call(['open', file_path])
                    else:
                        subprocess.call(['xdg-open', file_path])
            else:
                messagebox.showerror("Error", "Failed to generate medical records PDF")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download records: {str(e)}")
            import traceback
            traceback.print_exc()

    def handle_logout(self):
        """Handle logout"""
        result = messagebox.askyesno(
            "Confirm Logout",
            "Are you sure you want to logout?"
        )

        if result:
            self.destroy()