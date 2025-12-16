# import serial
# import time

# # Open serial port (adjust COM port)
# ser = serial.Serial('COM5', baudrate=57600, timeout=10)

# # Send handshake command
# handshake = bytes([0xEF, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0x01, 0x00, 0x03, 0x01, 0x00, 0x05])
# ser.write(handshake)
# response = ser.read(12)

# if len(response) == 12 and response[9] == 0x00:
#     print("✅ R307 Connected Successfully!")
# else:
#     print("❌ Connection Failed")

# ser.close()


import serial
import time

# Configure the serial port
# Replace 'COM3' with the actual serial port your CP2102 is connected to
# On Linux, this might be something like '/dev/ttyUSB0'
SERIAL_PORT = 'COM7'
BAUD_RATE = 9600

try:
    # Open the serial port
    ser = serial.Serial(
        port=SERIAL_PORT,
        baudrate=BAUD_RATE,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1  # Read timeout in seconds
    )

    print(
        f"Serial port {SERIAL_PORT} opened successfully at {BAUD_RATE} baud.")

    # Send a test message
    test_message = b"Hello from Python via CP2102!\n"
    ser.write(test_message)
    print(f"Sent: {test_message.decode().strip()}")

    # Wait a short moment for the data to be transmitted and received
    time.sleep(0.1)

    # Read the response (should be the same message in a loopback test)
    received_data = ser.readline()
    if received_data:
        print(f"Received: {received_data.decode().strip()}")
        if received_data == test_message:
            print("Loopback test successful: Sent and received messages match.")
        else:
            print("Loopback test failed: Sent and received messages do not match.")
    else:
        print("No data received.")

except serial.SerialException as e:
    print(f"Error opening or communicating with serial port: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # Close the serial port if it was opened
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")
