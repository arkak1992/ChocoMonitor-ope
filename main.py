import sys
from PyQt6.QtWidgets import QApplication
from sensors.arduino_reader import ArduinoReader
from ui.interface import ChocoMonitorUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    arduino_reader = ArduinoReader()
    arduino_reader.start_reading()
    window = ChocoMonitorUI(arduino_reader)
    window.show()
    sys.exit(app.exec())