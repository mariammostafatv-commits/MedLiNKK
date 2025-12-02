"""
Emergency card dialog - Display and generate emergency cards
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
from gui.styles import *
from utils.pdf_generator import generate_emergency_card
from utils.qr_generator import generate_patient_qr
from PIL import ImageTk
import os


class EmergencyDialog(ctk.CTkToplevel):
    """Emergency card display and generation dialog"""

    def __init__(self, parent, patient_data):
        super().__init__(parent)

        self.patient_data = patient_data

        # Configure window
        self.title("Emergency Card")
        self.geometry("700x800")
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
        """Create emergency card preview UI"""
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        main_frame.pack(fill='both', expand=True)

        # Emergency header - Red
        emergency_header = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS['danger'],
            height=120
        )
        emergency_header.pack(fill='x')
        emergency_header.pack_propagate(False)

        header_content = ctk.CTkFrame(emergency_header, fg_color='transparent')
        header_content.pack(expand=True)

        emergency_icon = ctk.CTkLabel(
            header_content,
            text="🆘",
            font=('Segoe UI', 48)
        )
        emergency_icon.pack()

        emergency_title = ctk.CTkLabel(
            header_content,
            text="EMERGENCY CARD",
            font=('Segoe UI', 28, 'bold'),
            text_color='white'
        )
        emergency_title.pack()

        # Scrollable content
        content_scroll = ctk.CTkScrollableFrame(
            main_frame,
            fg_color='transparent'
        )
        content_scroll.pack(fill='both', expand=True, padx=30, pady=30)

        # Patient Name - Large
        name_label = ctk.CTkLabel(
            content_scroll,
            text=self.patient_data.get('full_name', 'N/A'),
            font=('Segoe UI', 32, 'bold'),
            text_color=COLORS['text_primary']
        )
        name_label.pack(pady=(0, 5))

        # National ID
        id_label = ctk.CTkLabel(
            content_scroll,
            text=f"ID: {self.patient_data.get('national_id', 'N/A')}",
            font=FONTS['body'],
            text_color=COLORS['text_muted']
        )
        id_label.pack(pady=(0, 20))

        # Divider
        ctk.CTkFrame(
            content_scroll,
            height=2,
            fg_color=COLORS['bg_hover']
        ).pack(fill='x', pady=20)

        # Blood Type - Highlighted
        blood_frame = ctk.CTkFrame(
            content_scroll,
            fg_color=COLORS['danger'],
            corner_radius=RADIUS['lg'],
            height=80
        )
        blood_frame.pack(fill='x', pady=(0, 20))
        blood_frame.pack_propagate(False)

        blood_content = ctk.CTkFrame(blood_frame, fg_color='transparent')
        blood_content.place(relx=0.5, rely=0.5, anchor='center')

        blood_label = ctk.CTkLabel(
            blood_content,
            text=f"🩸 Blood Type: {self.patient_data.get('blood_type', 'Unknown')}",
            font=('Segoe UI', 24, 'bold'),
            text_color='white'
        )
        blood_label.pack()

        # Basic Info
        info_frame = ctk.CTkFrame(
            content_scroll,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['md']
        )
        info_frame.pack(fill='x', pady=(0, 20))

        info_content = ctk.CTkFrame(info_frame, fg_color='transparent')
        info_content.pack(fill='x', padx=20, pady=20)

        info_row = ctk.CTkFrame(info_content, fg_color='transparent')
        info_row.pack(fill='x')

        age_label = ctk.CTkLabel(
            info_row,
            text=f"Age: {self.patient_data.get('age', 'N/A')} years",
            font=FONTS['body'],
            text_color=COLORS['text_primary']
        )
        age_label.pack(side='left', padx=(0, 40))

        gender_label = ctk.CTkLabel(
            info_row,
            text=f"Gender: {self.patient_data.get('gender', 'N/A')}",
            font=FONTS['body'],
            text_color=COLORS['text_primary']
        )
        gender_label.pack(side='left')

        # Allergies - Red warning if present
        allergies = self.patient_data.get('allergies', [])
        if allergies:
            allergy_frame = ctk.CTkFrame(
                content_scroll,
                fg_color='#fef2f2',
                corner_radius=RADIUS['md'],
                border_width=2,
                border_color=COLORS['danger']
            )
            allergy_frame.pack(fill='x', pady=(0, 20))

            allergy_content = ctk.CTkFrame(
                allergy_frame, fg_color='transparent')
            allergy_content.pack(fill='x', padx=20, pady=20)

            allergy_title = ctk.CTkLabel(
                allergy_content,
                text="⚠️ ALLERGIES",
                font=FONTS['subheading'],
                text_color=COLORS['danger']
            )
            allergy_title.pack(anchor='w', pady=(0, 10))

            allergy_text = ctk.CTkLabel(
                allergy_content,
                text=", ".join(allergies),
                font=FONTS['body_bold'],
                text_color='#7f1d1d',
                anchor='w'
            )
            allergy_text.pack(anchor='w')
        else:
            no_allergy_label = ctk.CTkLabel(
                content_scroll,
                text="✓ No known allergies",
                font=FONTS['body'],
                text_color=COLORS['secondary']
            )
            no_allergy_label.pack(anchor='w', pady=(0, 20))

        # Chronic Diseases
        chronic = self.patient_data.get('chronic_diseases', [])
        if chronic:
            chronic_frame = ctk.CTkFrame(
                content_scroll,
                fg_color=COLORS['bg_medium'],
                corner_radius=RADIUS['md']
            )
            chronic_frame.pack(fill='x', pady=(0, 20))

            chronic_content = ctk.CTkFrame(
                chronic_frame, fg_color='transparent')
            chronic_content.pack(fill='x', padx=20, pady=20)

            chronic_title = ctk.CTkLabel(
                chronic_content,
                text="🏥 Chronic Conditions",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary']
            )
            chronic_title.pack(anchor='w', pady=(0, 8))

            chronic_text = ctk.CTkLabel(
                chronic_content,
                text=", ".join(chronic),
                font=FONTS['body'],
                text_color=COLORS['text_secondary'],
                anchor='w'
            )
            chronic_text.pack(anchor='w')

        # Current Medications
        medications = self.patient_data.get('current_medications', [])
       
        if medications:
            # Extract medication names from dictionaries
            if isinstance(medications[0], dict):
                med_names = [med.get('name', 'Unknown') for med in medications[:3]]
            else:
                med_names = medications[:3]
            
            med_text = "💊 Medications: " + ", ".join(med_names)
 
        if medications:
            meds_frame = ctk.CTkFrame(
                content_scroll,
                fg_color=COLORS['bg_medium'],
                corner_radius=RADIUS['md']
            )
            meds_frame.pack(fill='x', pady=(0, 20))

            meds_content = ctk.CTkFrame(meds_frame, fg_color='transparent')
            meds_content.pack(fill='x', padx=20, pady=20)

            meds_title = ctk.CTkLabel(
                meds_content,
                text="💊 Current Medications",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary']
            )
            meds_title.pack(anchor='w', pady=(0, 10))

            for i, med in enumerate(medications[:3], 1):
                med_text = f"{i}. {med.get('name', 'N/A')} - {med.get('dosage', '')} {med.get('frequency', '')}"
                med_label = ctk.CTkLabel(
                    meds_content,
                    text=med_text,
                    font=FONTS['body'],
                    text_color=COLORS['text_secondary'],
                    anchor='w'
                )
                med_label.pack(anchor='w', pady=2)

        # Emergency Contact
        emergency = self.patient_data.get('emergency_contact', {})
        if emergency:
            contact_frame = ctk.CTkFrame(
                content_scroll,
                fg_color=COLORS['info'],
                corner_radius=RADIUS['md']
            )
            contact_frame.pack(fill='x', pady=(0, 20))

            contact_content = ctk.CTkFrame(
                contact_frame, fg_color='transparent')
            contact_content.pack(fill='x', padx=20, pady=20)

            contact_title = ctk.CTkLabel(
                contact_content,
                text="📞 Emergency Contact",
                font=FONTS['body_bold'],
                text_color='white'
            )
            contact_title.pack(anchor='w', pady=(0, 8))

            contact_name = ctk.CTkLabel(
                contact_content,
                text=f"{emergency.get('name', 'N/A')} ({emergency.get('relation', 'N/A')})",
                font=FONTS['body'],
                text_color='white',
                anchor='w'
            )
            contact_name.pack(anchor='w')

            contact_phone = ctk.CTkLabel(
                contact_content,
                text=f"Phone: {emergency.get('phone', 'N/A')}",
                font=FONTS['body_bold'],
                text_color='white',
                anchor='w'
            )
            contact_phone.pack(anchor='w')

        # QR Code
        try:
            qr_frame = ctk.CTkFrame(
                content_scroll,
                fg_color=COLORS['bg_medium'],
                corner_radius=RADIUS['md']
            )
            qr_frame.pack(fill='x')

            qr_content = ctk.CTkFrame(qr_frame, fg_color='transparent')
            qr_content.pack(padx=20, pady=20)

            qr_img = generate_patient_qr(
                self.patient_data.get('national_id', ''))
            qr_photo = ImageTk.PhotoImage(qr_img)

            qr_label = ctk.CTkLabel(
                qr_content,
                image=qr_photo,
                text=""
            )
            qr_label.image = qr_photo  # Keep reference
            qr_label.pack()

            qr_text = ctk.CTkLabel(
                qr_content,
                text="Scan for quick access",
                font=FONTS['small'],
                text_color=COLORS['text_muted']
            )
            qr_text.pack(pady=(5, 0))

        except Exception as e:
            print(f"QR code display error: {e}")

        # Action buttons
        btn_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        btn_frame.pack(fill='x', padx=30, pady=(0, 30))

        generate_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Generate PDF",
            command=self.generate_pdf,
            font=FONTS['body_bold'],
            height=50,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        generate_btn.pack(side='left', fill='x', expand=True, padx=(0, 10))

        close_btn = ctk.CTkButton(
            btn_frame,
            text="Close",
            command=self.destroy,
            font=FONTS['body_bold'],
            height=50,
            fg_color='transparent',
            hover_color=COLORS['bg_light'],
            border_width=2,
            border_color=COLORS['primary'],
            text_color=COLORS['primary']
        )
        close_btn.pack(side='right', fill='x', expand=True, padx=(10, 0))

    def generate_pdf(self):
        """Generate emergency card PDF"""
        try:
            # Ask where to save
            default_filename = f"Emergency_Card_{self.patient_data.get('full_name', 'Patient').replace(' ', '_')}.pdf"

            file_path = filedialog.asksaveasfilename(
                title="Save Emergency Card",
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
                initialfile=default_filename
            )

            if not file_path:
                return

            # Generate PDF
            success = generate_emergency_card(self.patient_data, file_path)

            if success:
                messagebox.showinfo(
                    "Success",
                    f"Emergency card saved successfully!\n\n{file_path}\n\n"
                    "Print this card and keep it in your wallet."
                )

                # Ask if user wants to open the file
                if messagebox.askyesno("Open File", "Would you like to open the PDF now?"):
                    import platform
                    import subprocess

                    if platform.system() == 'Windows':
                        os.startfile(file_path)
                    elif platform.system() == 'Darwin':  # macOS
                        subprocess.call(['open', file_path])
                    else:  # Linux
                        subprocess.call(['xdg-open', file_path])
            else:
                messagebox.showerror(
                    "Error", "Failed to generate emergency card PDF")

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to save emergency card: {str(e)}")
