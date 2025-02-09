import serial
import time
import atexit
from threading import Thread, Event, Lock
import csv
import os
import datetime

class ArduinoReader:
    def __init__(self, port='COM3', baudrate=115200, output_folder="data"):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.running = False
        self.latest_temperature = None
        self.previous_temperature = None
        self.lock = Lock()
        self.stop_event = Event()
        self.output_folder = output_folder
        self.data_file = None
        self.ensure_directory()
        atexit.register(self.cleanup)

    def ensure_directory(self):
        today_folder = datetime.date.today().strftime("%Y-%m-%d")
        self.output_folder = os.path.join(self.output_folder, today_folder)
        os.makedirs(self.output_folder, exist_ok=True)
        self.data_file = os.path.join(self.output_folder, f"temperature_{datetime.datetime.now().strftime('%H-%M-%S')}.csv")

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
        with open(self.data_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Time (s)", "Temperature (°C)"])
            start_time = time.time()

            while self.running and not self.stop_event.is_set():
                try:
                    if self.ser and self.ser.in_waiting > 0:
                        data = self.ser.readline().decode('utf-8', errors='ignore').strip()
                        if self.is_valid_temperature(data):
                            temp = round(float(data), 2)
                            elapsed_time = round(time.time() - start_time, 2)
                            writer.writerow([elapsed_time, temp])
                            csvfile.flush()

                            with self.lock:
                                self.previous_temperature = self.latest_temperature
                                self.latest_temperature = temp
                                print(f"🌡 Updated Temperature: {self.latest_temperature} °C at {elapsed_time}s")
                except serial.SerialException:
                    print("🔌 Serial Error: Lost connection, attempting to reconnect...")
                    self.connect()
                except ValueError:
                    print("⚠ Invalid numeric conversion")
                time.sleep(0.05)  # تحسين سرعة الاستجابة
        self.cleanup()

    def is_valid_temperature(self, data):
        try:
            temp = float(data)
            return 15 <= temp <= 50
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

if __name__ == "__main__":
    from ui.interface import ChocoMonitorUI
    from PyQt6.QtWidgets import QApplication
    import sys

    arduino_reader = ArduinoReader()
    arduino_reader.start_reading()

    app = QApplication(sys.argv)
    window = ChocoMonitorUI(arduino_reader)
    window.show()
    sys.exit(app.exec())
