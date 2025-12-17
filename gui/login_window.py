"""
Login window with NFC support - KEEPS YOUR ORIGINAL DESIGN
Only adds background NFC scanning, no UI changes
Location: gui/login_window.py (REPLACE)
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from core.auth_manager import AuthManager
from core.card_manager import card_manager 
from core.data_manager import data_manager
from utils.validators import validate_national_id
from config.localization import get_string as _


class LoginWindow(ctk.CTk):
    """Modern login window with NFC card support (invisible)"""

    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        self.card_manager = card_manager
        # NFC card reading (background)
        self.card_buffer = ""
        self.card_reading_active = True

        # Configure window
        self.title("MedLink - Medical Records System")
        self.geometry("900x600")
        self.resizable(False, False)

        # Setup theme
        setup_theme()

        # Center window
        self.center_window()

        # Create UI
        self.create_ui()

        # Bind key events for NFC (invisible to user)
        self.bind("<Key>", self.on_key_press)

    def center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def on_key_press(self, event):
        """Handle NFC card scanning (background, invisible)"""
        if not self.card_reading_active:
            return

        # Don't interfere if typing in fields
        focused = self.focus_get()
        if isinstance(focused, ctk.CTkEntry):
            return

        # Enter key = card scan complete
        if event.keysym == "Return":
            card_id = self.card_buffer.strip()
            self.card_buffer = ""

            if card_id and len(card_id) >= 8:
                self.process_card(card_id)
        else:
            # Build card ID
            if len(event.char) > 0 and event.char.isprintable():
                self.card_buffer += event.char

    def process_card(self, card_id):
        """Process scanned NFC card"""
        print(f"🔍 Card scanned: {card_id}")

        # Get card information (WORKS NOW!)
        card_info = self.card_manager.get_card(card_id)
        
        print(card_info)
        if card_info:
            if card_info['card_type'] == 'doctor':
                user = card_info['user']
            else:
                patient = card_info['patient']
                if not card_info:
                    print("❌ Card not found")
                    return
        else:
            print("❌ Card not recognized")
            return False
        # Check card type
        print(card_info)
        if card_info['card_type'] == 'doctor':
            user = card_info['user']  # Full User object
            role = user.get('role', 'Unknown')
            print(role)
            print(f"✅ Doctor: {user.get('full_name', 'Unknown')}")
            self.open_dashboard(role, user)

        elif card_info['card_type'] == 'patient':
            patient = card_info['patient']  # Full Patient object
            print(f"✅ Patient: {patient.full_name}")
            self.open_patient_dashboard(patient)

    def create_ui(self):
        """Create beautiful login interface"""
        # Main container with gradient effect
        main_container = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        main_container.pack(fill='both', expand=True)

        # Left side - Branding and info
        left_panel = ctk.CTkFrame(
            main_container,
            fg_color=COLORS['primary'],
            corner_radius=0
        )
        left_panel.pack(side='left', fill='both', expand=True)

        # Branding content
        branding_frame = ctk.CTkFrame(left_panel, fg_color='transparent')
        branding_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Large medical icon
        icon_label = ctk.CTkLabel(
            branding_frame,
            text="🏥",
            font=('Segoe UI', 80)
        )
        icon_label.pack(pady=(0, 20))

        # App name with modern styling
        app_name = ctk.CTkLabel(
            branding_frame,
            text="MedLink",
            font=('Segoe UI', 42, 'bold'),
            text_color='white'
        )
        app_name.pack()

        # Tagline
        tagline = ctk.CTkLabel(
            branding_frame,
            text="Unified Medical Records System",
            font=('Segoe UI', 16),
            text_color='white'
        )
        tagline.pack(pady=(10, 20))

        # NFC indicator (small, bottom of left panel)
        nfc_indicator = ctk.CTkLabel(
            left_panel,
            text="💳 NFC Card Ready",
            font=('Segoe UI', 10),
            text_color='white'
        )
        nfc_indicator.pack(side='bottom', pady=20)

        # Right side - Login form
        right_panel = ctk.CTkFrame(
            main_container,
            fg_color=COLORS['bg_dark'],
            corner_radius=0
        )
        right_panel.pack(side='right', fill='both', expand=True)

        # Form container
        form_container = ctk.CTkFrame(right_panel, fg_color='transparent')
        form_container.place(relx=0.5, rely=0.5, anchor='center')

        # Welcome text
        welcome_label = ctk.CTkLabel(
            form_container,
            text="Welcome Back!",
            font=('Segoe UI', 32, 'bold'),
            text_color=COLORS['text_primary']
        )
        welcome_label.pack(pady=(0, 10))

        subtitle_label = ctk.CTkLabel(
            form_container,
            text="Sign in to continue to MedLink",
            font=('Segoe UI', 13),
            text_color=COLORS['text_secondary']
        )
        subtitle_label.pack(pady=(0, 40))

        # Login card
        login_card = ctk.CTkFrame(
            form_container,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg'],
            width=380,
            height=450
        )
        login_card.pack_propagate(False)
        login_card.pack()

        # Card content with padding
        card_content = ctk.CTkFrame(login_card, fg_color='transparent')
        card_content.pack(fill='both', expand=True, padx=35, pady=35)

        # Role selection with modern tabs
        role_label = ctk.CTkLabel(
            card_content,
            text="I am a",
            font=FONTS['subheading'],
            text_color=COLORS['text_primary']
        )
        role_label.pack(anchor='w', pady=(0, 15))

        # Modern segmented button for role
        self.role_var = ctk.StringVar(value="doctor")

        role_segment = ctk.CTkSegmentedButton(
            card_content,
            values=["doctor", "patient"],
            variable=self.role_var,
            font=FONTS['body'],
            height=45
        )
        role_segment.pack(fill='x', pady=(0, 25))

        # Username field with icon
        username_frame = ctk.CTkFrame(card_content, fg_color='transparent')
        username_frame.pack(fill='x', pady=(0, 20))

        username_label = ctk.CTkLabel(
            username_frame,
            text="👤  Username",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        username_label.pack(anchor='w', pady=(0, 8))

        self.username_entry = ctk.CTkEntry(
            username_frame,
            placeholder_text="Enter your username",
            font=FONTS['body'],
            height=45,
            corner_radius=RADIUS['md'],
            border_width=2,
            fg_color=COLORS['bg_light'],
            border_color=COLORS['bg_hover']
        )
        self.username_entry.pack(fill='x')

        # Password field with icon
        password_frame = ctk.CTkFrame(card_content, fg_color='transparent')
        password_frame.pack(fill='x', pady=(0, 30))

        password_label = ctk.CTkLabel(
            password_frame,
            text="🔒  Password",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        password_label.pack(anchor='w', pady=(0, 8))

        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Enter your password",
            font=FONTS['body'],
            height=45,
            corner_radius=RADIUS['md'],
            border_width=2,
            show="●",
            fg_color=COLORS['bg_light'],
            border_color=COLORS['bg_hover']
        )
        self.password_entry.pack(fill='x')

        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.handle_login())

        # Login button - large and prominent
        login_btn = ctk.CTkButton(
            card_content,
            text="Sign In",
            command=self.handle_login,
            font=('Segoe UI', 14, 'bold'),
            height=50,
            corner_radius=RADIUS['md'],
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_hover']
        )
        login_btn.pack(fill='x', pady=(0, 20))

        # Divider
        divider_frame = ctk.CTkFrame(card_content, fg_color='transparent')
        divider_frame.pack(fill='x', pady=(0, 20))

        ctk.CTkFrame(
            divider_frame,
            height=1,
            fg_color=COLORS['bg_hover']
        ).pack(side='left', fill='x', expand=True)

        ctk.CTkLabel(
            divider_frame,
            text="  OR  ",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        ).pack(side='left')

        ctk.CTkFrame(
            divider_frame,
            height=1,
            fg_color=COLORS['bg_hover']
        ).pack(side='left', fill='x', expand=True)

        # Register button
        register_btn = ctk.CTkButton(
            card_content,
            text="Create Patient Account",
            command=self.show_register_dialog,
            font=FONTS['body'],
            height=45,
            corner_radius=RADIUS['md'],
            fg_color='transparent',
            hover_color=COLORS['bg_light'],
            border_width=2,
            border_color=COLORS['secondary'],
            text_color=COLORS['secondary']
        )
        register_btn.pack(fill='x')

        # Footer
        footer_label = ctk.CTkLabel(
            right_panel,
            text="v1.0.0 | © 2024 MedLink Systems",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        footer_label.pack(side='bottom', pady=20)

    def handle_login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        role = self.role_var.get()

        # Validate inputs
        if not username or not password:
            messagebox.showerror(
                "Input Required",
                "Please enter both username and password"
            )
            return

        # Disable card reading during manual login
        self.card_reading_active = False

        # Attempt login
        # success, message, user_data = self.auth_manager.login(username, password, role)
        success, message, user_data = self.auth_manager.login(
            username, password, role)

        if success:
            # Close login window and open appropriate dashboard
            self.withdraw()
            self.open_dashboard(role, user_data)
        else:
            messagebox.showerror("Login Failed", message)
            # Clear password field
            self.password_entry.delete(0, 'end')
            self.card_reading_active = True

    def open_dashboard(self, role: str, user_data: dict):
        """Open appropriate dashboard based on role"""
        try:
            if role == 'doctor':
                from gui.doctor_dashboard import DoctorDashboard
                dashboard = DoctorDashboard(self, user_data)
                dashboard.deiconify()
            else:
                from gui.patient_dashboard import PatientDashboard
                dashboard = PatientDashboard(self, user_data)
                dashboard.deiconify()

            dashboard.protocol("WM_DELETE_WINDOW",
                               lambda: self.on_dashboard_close(dashboard))
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to open dashboard: {str(e)}")
            print(f"Dashboard error: {e}")
            self.deiconify()
            self.card_reading_active = True

    def on_dashboard_close(self, dashboard):
        """Handle dashboard window close"""
        dashboard.destroy()
        self.auth_manager.logout()
        self.deiconify()
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.card_reading_active = True

    def show_register_dialog(self):
        """Show patient registration dialog"""
        try:
            from gui.components.register_dialog import RegisterDialog
            dialog = RegisterDialog(self)
            dialog.wait_window()
        except ImportError:
            # If register dialog doesn't exist, show placeholder
            messagebox.showinfo(
                "Registration",
                "Patient registration feature will be available soon.\n\n"
                "For now, please contact hospital administration to create an account."
            )


if __name__ == "__main__":
    # Test the card manager
    manager = card_manager()

    # Example 1: Get card info
    print("\n=== Example 1: Get Card Info ===")
    card_info = manager.get_card("0724184100")
    if card_info:
        print(f"Card Type: {card_info['card_type']}")
        print(f"Name: {card_info['full_name']}")
        if card_info['card_type'] == 'doctor':
            print(f"Specialization: {card_info['user'].specialization}")

    # Example 2: Authenticate card
    print("\n=== Example 2: Authenticate Card ===")
    success, data, message = manager.authenticate_card("0724184100")
    print(f"Success: {success}")
    print(f"Message: {message}")

    # Example 3: Check card type
    print("\n=== Example 3: Check Card Type ===")
    if manager.is_doctor_card("0724184100"):
        print("This is a doctor card")
        doctor = manager.get_doctor_by_card("0724184100")
        print(f"Doctor: {doctor.full_name}")

    # Example 4: Get patient by card
    print("\n=== Example 4: Get Patient by Card ===")
    patient_card_uid = "0725755156"  # Example patient card
    patient = manager.get_patient_by_card(patient_card_uid)
    if patient:
        print(f"Patient: {patient.full_name}")
        print(f"National ID: {patient.national_id}")
