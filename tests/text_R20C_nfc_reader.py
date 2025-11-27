import serial

# R20C usually appears as virtual serial port
nfc = serial.Serial('COM4', baudrate=9600, timeout=2)

print("Waiting for NFC card... Place card on reader")
while True:
    data = nfc.readline()
    if data:
        uid = data.decode('utf-8').strip()
        print(f"✅ Card UID detected: {uid}")
        break

nfc.close()