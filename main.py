import webview
import serial
import serial.tools.list_ports
import time

class SerialAPI:
    def __init__(self):
        self.ser = None

    def get_ports(self):
        """Returns a list of available COM ports on the system."""
        try:
            ports = [p.device for p in serial.tools.list_ports.comports()]
            return ports
        except Exception as e:
            print(f"Error fetching ports: {e}")
            return []

    def connect(self, port, baudrate):
        """Connects to the specified serial port."""
        try:
            if self.ser and self.ser.is_open:
                self.ser.close()
            
            self.ser = serial.Serial(port, int(baudrate), timeout=0.1)
            return True
        except Exception as e:
            print(f"Connection error on {port}: {e}")
            return False

    def disconnect(self):
        """Closes the active serial port connection."""
        try:
            if self.ser and self.ser.is_open:
                self.ser.close()
            self.ser = None
            return True
        except Exception as e:
            print(f"Disconnection error: {e}")
            return False

    def write_data(self, data):
        """Writes string commands to the open serial port."""
        try:
            if self.ser and self.ser.is_open:
                self.ser.write(data.encode('utf-8'))
                return True
        except Exception as e:
            print(f"Write error: {e}")
        return False

    def read_data(self):
        """Reads incoming response lines from the serial port buffer."""
        try:
            if self.ser and self.ser.is_open:
                line = self.ser.readline()
                if line:
                    return line.decode('utf-8', errors='ignore').strip()
        except Exception as e:
            pass
        return ""

if __name__ == '__main__':
    api = SerialAPI()
    # Bind the python API class to the pywebview window so JS can call window.pywebview.api
    window = webview.create_window(
        'Signifi Kiosk Latch Tester', 
        'index.html', 
        js_api=api,
        width=1280, 
        height=800,
        resizable=True
    )
    webview.start(debug=True)
