import customtkinter as ctk
from ai.face_auth_gui import FaceRegistrationDialog

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create app
app = ctk.CTk()
app.geometry("400x200")
app.title("MedLink - Register Team Member")

# Title
title = ctk.CTkLabel(
    app,
    text="🎭 MedLink Face Registration",
    font=("Arial", 20, "bold")
)
title.pack(pady=30)

# Register button
def open_registration():
    dialog = FaceRegistrationDialog(app)

register_btn = ctk.CTkButton(
    app,
    text="➕ Register New Team Member",
    command=open_registration,
    width=250,
    height=50,
    font=("Arial", 16, "bold"),
    fg_color="green",
    hover_color="darkgreen"
)
register_btn.pack(pady=20)

app.mainloop()