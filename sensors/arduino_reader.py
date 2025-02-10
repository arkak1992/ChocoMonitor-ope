import serial
import time
import atexit
from threading import Thread, Event, Lock

class ArduinoReader:
    def __init__(self, port='COM3', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.running = False
        self.latest_temperature = None
        self.previous_temperature = None
        self.lock = Lock()
        self.stop_event = Event()
        atexit.register(self.cleanup)

    def connect(self):
        max_retries = 5
        for attempt in range(max_retries):
            try:
                if self.ser and self.ser.is_open:
                    self.ser.close()
                self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
                time.sleep(2)
                self.ser.reset_input_buffer()
                print(f"✅ Connected to {self.port} at {self.baudrate} baud rate.")
                return True
            except serial.SerialException as e:
                print(f"❌ Serial Error [{attempt+1}/{max_retries}]: {e}")
                time.sleep(2)
        print("❌ Failed to connect to Arduino.")
        return False

    def start_reading(self):
        if not self.connect():
            return
        self.running = True
        self.stop_event.clear()
        self.thread = Thread(target=self.read_loop, daemon=True)
        self.thread.start()

    def read_loop(self):
        while self.running and not self.stop_event.is_set():
            try:
                if self.ser and self.ser.in_waiting > 0:
                    data = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if self.is_valid_temperature(data):
                        temp = round(float(data), 2)
                        with self.lock:
                            self.previous_temperature = self.latest_temperature
                            self.latest_temperature = temp
                            print(f"🌡 Updated Temperature: {self.latest_temperature} °C")
            except serial.SerialException:
                print("🔌 Serial Error: Lost connection, attempting to reconnect...")
                self.connect()
            except ValueError:
                print("⚠ Invalid numeric conversion")
            time.sleep(1)
        self.cleanup()

    def is_valid_temperature(self, data):
        try:
            float(data)
            return True
        except ValueError:
            return False

    def get_latest_temperature(self):
        with self.lock:
            return self.latest_temperature

    def stop_reading(self):
        self.running = False
        self.stop_event.set()
        self.cleanup()

    def cleanup(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("🔌 Serial connection closed safely.")
