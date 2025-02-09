from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton
from PyQt6.QtCore import pyqtSignal
import json

class SettingsUI(QDialog):
    settings_applied = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.temp_label = QLabel("Start Temperature (°C):")
        self.temp_input = QSpinBox()
        self.temp_input.setRange(10, 50)
        layout.addWidget(self.temp_label)
        layout.addWidget(self.temp_input)

        self.duration_label = QLabel("Process Duration (min):")
        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 60)
        layout.addWidget(self.duration_label)
        layout.addWidget(self.duration_input)

        self.apply_button = QPushButton("Apply")
        self.apply_button.setStyleSheet("font-size: 16px; padding: 10px; background-color: #007ACC; color: white;")
        self.apply_button.clicked.connect(self.apply_settings)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)
        self.load_settings()

    def load_settings(self):
        try:
            with open("config.json", "r") as file:
                settings = json.load(file)
                self.temp_input.setValue(settings.get("start_temperature", 30))
                self.duration_input.setValue(settings.get("duration", 5))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def apply_settings(self):
        settings = {
            "start_temperature": self.temp_input.value(),
            "duration": self.duration_input.value()
        }
        with open("config.json", "w") as file:
            json.dump(settings, file, indent=4)
        self.settings_applied.emit(settings)
        self.close()
