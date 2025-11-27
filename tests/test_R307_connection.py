import serial
import time

# Open serial port (adjust COM port)
ser = serial.Serial('COM3', baudrate=57600, timeout=2)

# Send handshake command
handshake = bytes([0xEF, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0x01, 0x00, 0x03, 0x01, 0x00, 0x05])
ser.write(handshake)
response = ser.read(12)

if len(response) == 12 and response[9] == 0x00:
    print("✅ R307 Connected Successfully!")
else:
    print("❌ Connection Failed")
    
ser.close()