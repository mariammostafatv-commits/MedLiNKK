import serial
import time

PORT = 'COM8'
BAUD = 57600

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(0.5)

handshake = bytes([
    0xEF, 0x01,
    0xFF, 0xFF, 0xFF, 0xFF,
    0x01,
    0x00, 0x03,
    0x01,
    0x00, 0x05
])

ser.write(handshake)
response = ser.read(12)

print("Response length:", len(response))
print("Response HEX:", response.hex(" "))

if len(response) == 12 and response[9] == 0x00:
    print("✅ R307 Connected Successfully")
else:
    print("❌ No valid response")

ser.close()
