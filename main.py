"""
    MedLink - Unified Medical Records System
    Entry point for the application
"""
import customtkinter as ctk
from gui.login_window import LoginWindow
from gui.styles import setup_theme

76
def main():
    """Main application entry point"""
    # Setup theme
    setup_theme()

    # Create and run login window
    app = LoginWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
