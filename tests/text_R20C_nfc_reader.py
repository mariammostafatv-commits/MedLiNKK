import serial
import time
import os



import serial.tools.list_ports


def get_available_com_ports():
    """
    Lists serial port names and their descriptions.
    """
    ports = serial.tools.list_ports.comports()
    available_ports = []
    for port in ports:
        available_ports.append(f"{port.device}: {port.description}")
    return available_ports


if __name__ == "__main__":
    while True:    
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear console
        ports = get_available_com_ports()
        print("Available COM Ports:")
        for port in ports:
            print(f" - {port}")    
        time.sleep(5)  # Refresh every 5 seconds    
        # Example usage: List available COM ports   
        
