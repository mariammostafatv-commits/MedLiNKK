"""
Face Authentication GUI for MedLink
Enhanced with live camera preview, real-time status, and animations
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import threading
import time
import os
from face_auth_manager import FaceAuthManager


class FaceRegistrationDialog(ctk.CTkToplevel):
    """Dialog for registering team members with live preview"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Register Team Member Face")
        self.geometry("600x750")
        self.resizable(False, False)
        
        self.face_manager = FaceAuthManager()
        self.selected_photo = None
        
        self._create_widgets()
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (750 // 2)
        self.geometry(f"600x750+{x}+{y}")
        
        # Make modal
        self.transient(parent)
        self.grab_set()
    
    def _create_widgets(self):
        # Title
        title = ctk.CTkLabel(
            self,
            text="🎭 Register Team Member",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)
        
        # Info frame
        info_frame = ctk.CTkFrame(self)
        info_frame.pack(pady=10, padx=20, fill="x")
        
        # Username
        ctk.CTkLabel(
            info_frame,
            text="Username:",
            font=("Arial", 14)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.username_entry = ctk.CTkEntry(
            info_frame,
            width=300,
            placeholder_text="e.g., youssef"
        )
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Full Name
        ctk.CTkLabel(
            info_frame,
            text="Full Name:",
            font=("Arial", 14)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.fullname_entry = ctk.CTkEntry(
            info_frame,
            width=300,
            placeholder_text="e.g., Youssef Ahmed"
        )
        self.fullname_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Role
        ctk.CTkLabel(
            info_frame,
            text="Role:",
            font=("Arial", 14)
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.role_combo = ctk.CTkComboBox(
            info_frame,
            width=300,
            values=["Doctor", "Admin", "Nurse", "Receptionist"]
        )
        self.role_combo.grid(row=2, column=1, padx=10, pady=10)
        self.role_combo.set("Doctor")
        
        # Photo preview
        self.photo_label = ctk.CTkLabel(
            self,
            text="No photo selected\n\nClick 'Capture from Webcam' or 'Choose Photo'",
            width=400,
            height=300,
            fg_color="gray20",
            font=("Arial", 14)
        )
        self.photo_label.pack(pady=20)
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)
        
        # Capture from webcam
        ctk.CTkButton(
            btn_frame,
            text="📷 Capture from Webcam",
            command=self.capture_from_webcam,
            width=200,
            height=40,
            font=("Arial", 13, "bold")
        ).pack(side="left", padx=10)
        
        # Choose file
        ctk.CTkButton(
            btn_frame,
            text="📁 Choose Photo",
            command=self.choose_photo,
            width=200,
            height=40,
            font=("Arial", 13, "bold")
        ).pack(side="left", padx=10)
        
        # Register button
        self.register_btn = ctk.CTkButton(
            self,
            text="✅ Register",
            command=self.register_member,
            width=420,
            height=50,
            font=("Arial", 18, "bold"),
            fg_color="green",
            hover_color="darkgreen",
            corner_radius=25
        )
        self.register_btn.pack(pady=20)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 12)
        )
        self.status_label.pack(pady=10)
    
    def capture_from_webcam(self):
        """Capture photo from webcam with LIVE preview"""
        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                messagebox.showerror("Error", "Could not open webcam!")
                return
            
            # Read a test frame
            ret, test_frame = cap.read()
            if not ret:
                cap.release()
                messagebox.showerror("Error", "Could not read from webcam!")
                return
            
            # Release for now
            cap.release()
            
            # Create preview window
            preview_window = ctk.CTkToplevel(self)
            preview_window.title("📷 Webcam Preview")
            preview_window.geometry("680x620")
            preview_window.resizable(False, False)
            
            # Title
            title = ctk.CTkLabel(
                preview_window,
                text="📷 Live Camera Preview",
                font=("Arial", 22, "bold")
            )
            title.pack(pady=15)
            
            # Camera feed
            label = ctk.CTkLabel(
                preview_window, 
                text="",
                width=640,
                height=480
            )
            label.pack(pady=5)
            
            # Instructions
            instruction_frame = ctk.CTkFrame(preview_window)
            instruction_frame.pack(pady=10, fill="x", padx=20)
            
            self.countdown_label = ctk.CTkLabel(
                instruction_frame,
                text="Position your face in the green box",
                font=("Arial", 14, "bold"),
                text_color="yellow"
            )
            self.countdown_label.pack(pady=5)
            
            # Button frame
            btn_frame = ctk.CTkFrame(preview_window)
            btn_frame.pack(pady=5)
            
            # Capture button
            capture_button = ctk.CTkButton(
                btn_frame,
                text="📸 CAPTURE (Space)",
                command=lambda: on_capture(),
                width=200,
                height=45,
                font=("Arial", 16, "bold"),
                fg_color="green",
                hover_color="darkgreen",
                corner_radius=22
            )
            capture_button.pack(side="left", padx=10)
            
            # Cancel button
            cancel_button = ctk.CTkButton(
                btn_frame,
                text="❌ Cancel (Esc)",
                command=lambda: on_cancel(),
                width=200,
                height=45,
                font=("Arial", 16, "bold"),
                fg_color="red",
                hover_color="darkred",
                corner_radius=22
            )
            cancel_button.pack(side="left", padx=10)
            
            captured = [False]
            captured_frame = [None]
            
            cap = cv2.VideoCapture(0)
            
            def update_frame():
                if not captured[0]:
                    ret, frame = cap.read()
                    if ret:
                        # Convert to RGB
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        
                        # Draw face detection guide
                        h, w = frame_rgb.shape[:2]
                        center_x, center_y = w // 2, h // 2
                        box_size = 300
                        
                        # Draw rectangle guide (green)
                        cv2.rectangle(
                            frame_rgb,
                            (center_x - box_size//2, center_y - box_size//2),
                            (center_x + box_size//2, center_y + box_size//2),
                            (0, 255, 0),
                            4
                        )
                        
                        # Draw corners for style
                        corner_len = 40
                        thickness = 6
                        # Top-left
                        cv2.line(frame_rgb, 
                                (center_x - box_size//2, center_y - box_size//2),
                                (center_x - box_size//2 + corner_len, center_y - box_size//2),
                                (0, 255, 255), thickness)
                        cv2.line(frame_rgb,
                                (center_x - box_size//2, center_y - box_size//2),
                                (center_x - box_size//2, center_y - box_size//2 + corner_len),
                                (0, 255, 255), thickness)
                        
                        # Top-right
                        cv2.line(frame_rgb,
                                (center_x + box_size//2, center_y - box_size//2),
                                (center_x + box_size//2 - corner_len, center_y - box_size//2),
                                (0, 255, 255), thickness)
                        cv2.line(frame_rgb,
                                (center_x + box_size//2, center_y - box_size//2),
                                (center_x + box_size//2, center_y - box_size//2 + corner_len),
                                (0, 255, 255), thickness)
                        
                        # Bottom-left
                        cv2.line(frame_rgb,
                                (center_x - box_size//2, center_y + box_size//2),
                                (center_x - box_size//2 + corner_len, center_y + box_size//2),
                                (0, 255, 255), thickness)
                        cv2.line(frame_rgb,
                                (center_x - box_size//2, center_y + box_size//2),
                                (center_x - box_size//2, center_y + box_size//2 - corner_len),
                                (0, 255, 255), thickness)
                        
                        # Bottom-right
                        cv2.line(frame_rgb,
                                (center_x + box_size//2, center_y + box_size//2),
                                (center_x + box_size//2 - corner_len, center_y + box_size//2),
                                (0, 255, 255), thickness)
                        cv2.line(frame_rgb,
                                (center_x + box_size//2, center_y + box_size//2),
                                (center_x + box_size//2, center_y + box_size//2 - corner_len),
                                (0, 255, 255), thickness)
                        
                        # Add text
                        cv2.putText(
                            frame_rgb,
                            "Position Your Face Here",
                            (center_x - 180, center_y - box_size//2 - 15),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (0, 255, 0),
                            2
                        )
                        
                        img = Image.fromarray(frame_rgb)
                        img = img.resize((640, 480))
                        photo = ImageTk.PhotoImage(img)
                        
                        label.configure(image=photo, text="")
                        label.image = photo
                        
                        preview_window.after(30, update_frame)
            
            def on_capture():
                ret, frame = cap.read()
                if ret:
                    captured[0] = True
                    captured_frame[0] = frame
                    cap.release()
                    
                    # Show captured message
                    self.countdown_label.configure(
                        text="✅ Photo Captured Successfully!",
                        text_color="green"
                    )
                    capture_button.configure(state="disabled")
                    cancel_button.configure(state="disabled")
                    
                    preview_window.after(800, preview_window.destroy)
                    
                    # Save temp file
                    os.makedirs("data", exist_ok=True)
                    self.selected_photo = "data/temp_capture.jpg"
                    cv2.imwrite(self.selected_photo, frame)
                    
                    # Update preview
                    self._update_photo_preview()
                    self.status_label.configure(
                        text="✅ Photo captured successfully!",
                        text_color="green"
                    )
            
            def on_cancel():
                captured[0] = True
                cap.release()
                preview_window.destroy()
            
            def on_key(event):
                if event.char == ' ':  # Space key
                    on_capture()
                elif event.keysym == 'Escape':
                    on_cancel()
            
            preview_window.bind('<Key>', on_key)
            preview_window.focus_set()
            
            # Handle window close
            def on_closing():
                captured[0] = True
                if cap.isOpened():
                    cap.release()
                preview_window.destroy()
            
            preview_window.protocol("WM_DELETE_WINDOW", on_closing)
            
            update_frame()
            
        except Exception as e:
            messagebox.showerror("Error", f"Webcam error: {str(e)}")
    
    def choose_photo(self):
        """Choose photo from file"""
        file_path = filedialog.askopenfilename(
            title="Select Photo",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.selected_photo = file_path
            self._update_photo_preview()
            self.status_label.configure(
                text="✅ Photo selected successfully!",
                text_color="green"
            )
    
    def _update_photo_preview(self):
        """Update photo preview"""
        if self.selected_photo:
            img = Image.open(self.selected_photo)
            img.thumbnail((400, 300))
            photo = ImageTk.PhotoImage(img)
            
            self.photo_label.configure(image=photo, text="")
            self.photo_label.image = photo
    
    def register_member(self):
        """Register team member"""
        username = self.username_entry.get().strip()
        fullname = self.fullname_entry.get().strip()
        role = self.role_combo.get().lower()
        
        if not username or not fullname:
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        if not self.selected_photo:
            messagebox.showerror("Error", "Please select or capture a photo!")
            return
        
        # Show processing
        self.status_label.configure(
            text="⏳ Processing... Please wait",
            text_color="yellow"
        )
        self.register_btn.configure(state="disabled", text="⏳ Registering...")
        self.update()
        
        # Register in thread
        def register():
            result = self.face_manager.register_team_member(
                username=username,
                full_name=fullname,
                role=role,
                photo_path=self.selected_photo
            )
            
            self.after(0, lambda: self._handle_registration_result(result))
        
        thread = threading.Thread(target=register, daemon=True)
        thread.start()
    
    def _handle_registration_result(self, result):
        """Handle registration result"""
        self.register_btn.configure(state="normal", text="✅ Register")
        
        if result["success"]:
            self.status_label.configure(
                text=result["message"],
                text_color="green"
            )
            messagebox.showinfo("Success", result["message"])
            self.destroy()
        else:
            self.status_label.configure(
                text=result["message"],
                text_color="red"
            )
            messagebox.showerror("Error", result["message"])


class FaceLoginDialog(ctk.CTkToplevel):
    """Dialog for face recognition login with LIVE preview"""
    
    def __init__(self, parent, on_success_callback=None):
        super().__init__(parent)
        
        self.title("Face Recognition Login")
        self.geometry("720x850")
        self.resizable(False, False)
        
        self.face_manager = FaceAuthManager()
        self.on_success_callback = on_success_callback
        
        self.cap = None
        self.is_scanning = False
        self.preview_running = False
        
        self._create_widgets()
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (720 // 2)
        y = (self.winfo_screenheight() // 2) - (850 // 2)
        self.geometry(f"720x850+{x}+{y}")
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Start preview when window opens
        self.after(500, self.start_preview)
        
        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def _create_widgets(self):
        # Title
        title = ctk.CTkLabel(
            self,
            text="🎭 Face Recognition Login",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=20)
        
        # Instructions
        instructions = ctk.CTkLabel(
            self,
            text="Position your face in front of the camera",
            font=("Arial", 14),
            text_color="gray"
        )
        instructions.pack(pady=5)
        
        # Live preview frame
        preview_frame = ctk.CTkFrame(self, fg_color="black")
        preview_frame.pack(pady=20, padx=20)
        
        # Camera preview (bigger size for better visibility)
        self.preview_label = ctk.CTkLabel(
            preview_frame,
            text="📷 Initializing camera...",
            width=640,
            height=480,
            fg_color="gray20",
            font=("Arial", 16)
        )
        self.preview_label.pack(padx=5, pady=5)
        
        # Status container
        status_container = ctk.CTkFrame(self)
        status_container.pack(pady=15, fill="x", padx=40)
        
        # Status icon
        self.status_icon = ctk.CTkLabel(
            status_container,
            text="⏺",
            font=("Arial", 45),
            text_color="gray"
        )
        self.status_icon.pack(side="left", padx=15)
        
        # Status text
        status_text_frame = ctk.CTkFrame(status_container, fg_color="transparent")
        status_text_frame.pack(side="left", fill="x", expand=True)
        
        self.status_label = ctk.CTkLabel(
            status_text_frame,
            text="Ready to scan",
            font=("Arial", 20, "bold"),
            text_color="gray",
            anchor="w"
        )
        self.status_label.pack(anchor="w", pady=2)
        
        self.details_label = ctk.CTkLabel(
            status_text_frame,
            text="Press 'Scan Face' to begin",
            font=("Arial", 13),
            text_color="gray",
            anchor="w"
        )
        self.details_label.pack(anchor="w")
        
        # Scan button
        self.scan_btn = ctk.CTkButton(
            self,
            text="📷 Scan Face",
            command=self.scan_face,
            width=450,
            height=65,
            font=("Arial", 22, "bold"),
            fg_color="blue",
            hover_color="darkblue",
            corner_radius=32
        )
        self.scan_btn.pack(pady=20)
        
        # Info frame
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(pady=10)
        
        # Registered users count
        users = self.face_manager.get_registered_users()
        users_label = ctk.CTkLabel(
            info_frame,
            text=f"👥 {len(users)} team members registered",
            font=("Arial", 12),
            text_color="gray"
        )
        users_label.pack()
    
    def start_preview(self):
        """Start live camera preview"""
        try:
            self.cap = cv2.VideoCapture(0)
            
            if not self.cap.isOpened():
                self.preview_label.configure(
                    text="❌ Camera not available\n\nPlease check your webcam connection",
                    font=("Arial", 16, "bold"),
                    text_color="red"
                )
                self.scan_btn.configure(state="disabled")
                self.status_label.configure(text="Camera Error", text_color="red")
                self.details_label.configure(text="Cannot access webcam")
                return
            
            self.preview_running = True
            self.update_preview()
            
        except Exception as e:
            self.preview_label.configure(
                text=f"❌ Camera Error\n\n{str(e)}",
                font=("Arial", 14),
                text_color="red"
            )
            self.scan_btn.configure(state="disabled")
    
    def update_preview(self):
        """Update camera preview continuously"""
        if not self.preview_running or self.cap is None:
            return
        
        try:
            ret, frame = self.cap.read()
            
            if ret:
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Resize to fit preview
                frame_resized = cv2.resize(frame_rgb, (640, 480))
                
                # Draw overlay based on state
                if self.is_scanning:
                    # SCANNING mode - yellow overlay
                    overlay = frame_resized.copy()
                    
                    # Draw pulsing border
                    border_thickness = 15
                    cv2.rectangle(
                        overlay, 
                        (border_thickness, border_thickness), 
                        (640-border_thickness, 480-border_thickness), 
                        (0, 255, 255),  # Yellow
                        border_thickness
                    )
                    
                    # Blend
                    frame_resized = cv2.addWeighted(frame_resized, 0.7, overlay, 0.3, 0)
                    
                    # Add scanning text with background
                    text = "SCANNING..."
                    font = cv2.FONT_HERSHEY_BOLD
                    text_size = cv2.getTextSize(text, font, 1.5, 3)[0]
                    text_x = (640 - text_size[0]) // 2
                    text_y = 50
                    
                    # Background rectangle for text
                    cv2.rectangle(
                        frame_resized,
                        (text_x - 10, text_y - text_size[1] - 10),
                        (text_x + text_size[0] + 10, text_y + 10),
                        (0, 0, 0),
                        -1
                    )
                    
                    # Text
                    cv2.putText(
                        frame_resized,
                        text,
                        (text_x, text_y),
                        font,
                        1.5,
                        (0, 255, 255),
                        3
                    )
                else:
                    # READY mode - subtle green corners
                    h, w = frame_resized.shape[:2]
                    corner_len = 50
                    thickness = 4
                    color = (0, 255, 0)  # Green
                    
                    # Top-left
                    cv2.line(frame_resized, (20, 20), (20+corner_len, 20), color, thickness)
                    cv2.line(frame_resized, (20, 20), (20, 20+corner_len), color, thickness)
                    
                    # Top-right
                    cv2.line(frame_resized, (w-20, 20), (w-20-corner_len, 20), color, thickness)
                    cv2.line(frame_resized, (w-20, 20), (w-20, 20+corner_len), color, thickness)
                    
                    # Bottom-left
                    cv2.line(frame_resized, (20, h-20), (20+corner_len, h-20), color, thickness)
                    cv2.line(frame_resized, (20, h-20), (20, h-20-corner_len), color, thickness)
                    
                    # Bottom-right
                    cv2.line(frame_resized, (w-20, h-20), (w-20-corner_len, h-20), color, thickness)
                    cv2.line(frame_resized, (w-20, h-20), (w-20, h-20-corner_len), color, thickness)
                
                # Convert to PhotoImage
                img = Image.fromarray(frame_resized)
                photo = ImageTk.PhotoImage(img)
                
                # Update label
                self.preview_label.configure(image=photo, text="")
                self.preview_label.image = photo
            
            # Continue updating
            if self.preview_running:
                self.after(30, self.update_preview)  # ~33 FPS
                
        except Exception as e:
            print(f"Preview error: {e}")
    
    def scan_face(self):
        """Scan face and recognize"""
        # Update UI
        self.is_scanning = True
        self.status_icon.configure(text="🔍", text_color="yellow")
        self.status_label.configure(text="Searching...", text_color="yellow")
        self.details_label.configure(text="Analyzing face features...", text_color="yellow")
        self.scan_btn.configure(state="disabled", text="⏳ Processing...")
        self.update()
        
        # Run recognition in thread
        def recognize():
            time.sleep(1.5)  # Give time to see "searching" message
            
            result = self.face_manager.recognize_from_webcam()
            
            # Update UI in main thread
            self.after(0, lambda: self._handle_result(result))
        
        thread = threading.Thread(target=recognize, daemon=True)
        thread.start()
    
    def _handle_result(self, result):
        """Handle recognition result"""
        self.is_scanning = False
        self.scan_btn.configure(state="normal", text="📷 Scan Face")
        
        if result["success"]:
            # SUCCESS! 🎉
            self.status_icon.configure(text="✅", text_color="green")
            self.status_label.configure(
                text=f"Welcome, {result['full_name']}!",
                text_color="green"
            )
            self.details_label.configure(
                text=f"Role: {result['role'].title()} | Confidence: {result['confidence']}%",
                text_color="green"
            )
            
            # Change button
            self.scan_btn.configure(
                text="✅ Login Successful!",
                fg_color="green",
                hover_color="green",
                state="disabled"
            )
            
            # Play success animation
            self._success_animation()
            
            # Call callback
            if self.on_success_callback:
                self.on_success_callback(result)
            
            # Close after delay
            self.after(3000, self.on_closing)
            
        else:
            # FAILED ❌
            self.status_icon.configure(text="❌", text_color="red")
            self.status_label.configure(
                text="Face Not Recognized",
                text_color="red"
            )
            self.details_label.configure(
                text=result["message"],
                text_color="red"
            )
            
            # Shake animation
            self._error_animation()
    
    def _success_animation(self):
        """Success flash animation"""
        original_color = self.cget("fg_color")
        
        def flash(count):
            if count > 0:
                # Flash green
                if count % 2 == 0:
                    self.configure(fg_color=("green", "darkgreen"))
                else:
                    self.configure(fg_color=original_color)
                
                self.after(200, lambda: flash(count - 1))
            else:
                self.configure(fg_color=original_color)
        
        flash(6)
    
    def _error_animation(self):
        """Error shake animation"""
        original_x = self.winfo_x()
        
        def shake(count, direction):
            if count > 0:
                offset = 15 if direction else -15
                self.geometry(f"+{original_x + offset}+{self.winfo_y()}")
                self.after(50, lambda: shake(count - 1, not direction))
            else:
                self.geometry(f"+{original_x}+{self.winfo_y()}")
        
        shake(8, True)
    
    def on_closing(self):
        """Clean up when closing"""
        self.preview_running = False
        
        if self.cap is not None:
            self.cap.release()
        
        self.destroy()


# Test application
if __name__ == "__main__":
    # Set appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = ctk.CTk()
    app.geometry("500x400")
    app.title("🎭 MedLink Face Recognition Test")
    
    # Title
    title = ctk.CTkLabel(
        app,
        text="🎭 MedLink Face Recognition",
        font=("Arial", 28, "bold")
    )
    title.pack(pady=30)
    
    # Subtitle
    subtitle = ctk.CTkLabel(
        app,
        text="AI-Powered Team Authentication System",
        font=("Arial", 14),
        text_color="gray"
    )
    subtitle.pack(pady=5)
    
    # Buttons frame
    btn_frame = ctk.CTkFrame(app, fg_color="transparent")
    btn_frame.pack(pady=40)
    
    def test_registration():
        dialog = FaceRegistrationDialog(app)
    
    def test_login():
        def on_success(result):
            messagebox.showinfo(
                "Login Successful!",
                f"Welcome {result['full_name']}!\n\n"
                f"Username: {result['username']}\n"
                f"Role: {result['role'].title()}\n"
                f"Confidence: {result['confidence']}%"
            )
        
        dialog = FaceLoginDialog(app, on_success)
    
    # Register button
    ctk.CTkButton(
        btn_frame,
        text="➕ Register New Member",
        command=test_registration,
        width=300,
        height=60,
        font=("Arial", 18, "bold"),
        fg_color="green",
        hover_color="darkgreen",
        corner_radius=30
    ).pack(pady=15)
    
    # Login button
    ctk.CTkButton(
        btn_frame,
        text="🎭 Face Login Test",
        command=test_login,
        width=300,
        height=60,
        font=("Arial", 18, "bold"),
        fg_color="blue",
        hover_color="darkblue",
        corner_radius=30
    ).pack(pady=15)
    
    # Info label
    info = ctk.CTkLabel(
        app,
        text="Make sure your webcam is connected",
        font=("Arial", 11),
        text_color="gray"
    )
    info.pack(pady=20)
    
    app.mainloop()