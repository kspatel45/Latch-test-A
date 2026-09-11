import os
import sys
import serial
import serial.tools.list_ports
import webview

class Api:
    def __init__(self):
        self.serial_port = None

    def get_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect(self, port_name, baudrate=115200):
        try:
            self.serial_port = serial.Serial(port_name, baudrate=baudrate, timeout=1)
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def write_data(self, data):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.write(data.encode('utf-8'))
            return True
        return False

    def read_data(self):
        if self.serial_port and self.serial_port.is_open:
            if self.serial_port.in_waiting > 0:
                return self.serial_port.readline().decode('utf-8', errors='ignore').strip()
        return ""

    def disconnect(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        return True

if __name__ == '__main__':
    api = Api()
    html_path = os.path.abspath('Locker Tesster V3.html')
    
    # Create native window wrapping your HTML UI
    window = webview.create_window(
        'Signifi Kiosk Latch Tester', 
        f'file://{html_path}', 
        js_api=api,
        width=1200, 
        height=800
    )
    webview.start()
