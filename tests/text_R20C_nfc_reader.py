# import serial

# import serial

# # R20C usually appears as virtual serial port
# nfc = serial.Serial('COM10', baudrate=57600, timeout=2)

# print("Waiting for NFC card... Place card on reader")
# while True:
#     data = nfc.readline()
#     if data:
#         uid = data.decode('utf-8').strip()
#         print(f"✅ Card UID detected: {uid}")
#         break

# nfc.close()

# print("Place card on reader (Ctrl+C to exit):")

# while True:
#     card_id = input(">> ")  # القارئ هيكتب الكود هنا ويعمل Enter
#     if card_id.strip() == "":
#         continue  # لو دخل سطر فاضي
#     print(f"Card read: {card_id!r}")


import tkinter as tk
from tkinter import messagebox

buffer = ""  # store card ID until Enter pressed

def on_key(event):
    global buffer

    if event.keysym == "Return":
        card_id = buffer.strip()
        buffer = ""  # reset buffer
        if card_id:
            process_card(card_id)
    else:
        # Append only characters (ignore special keys)
        if len(event.char) > 0:
            buffer += event.char

def process_card(card_id):
    print("Card read:", card_id)
    with open("card_id.txt", "a") as f:
        valid_card_id = f.write(card_id + "\n")
    if valid_card_id == "0724975956":
        # messagebox.showinfo("Access", "Login Success")
        ...
    else:
        # messagebox.showerror("Access", "Access Denied")
        ...

root = tk.Tk()
root.title("NFC Login (Hidden Input)")
root.geometry("400x200")

label = tk.Label(root, text="Scan your card to login", font=("Arial", 14))
label.pack(pady=50)

root.bind("<Key>", on_key)  # read every keystroke globally

root.mainloop()

