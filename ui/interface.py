import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QGridLayout, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QFrame
from PyQt6.QtCore import QTimer, QDateTime, Qt
from PyQt6.QtGui import QFont
from ui.sensor_widget import SensorWidget
from ui.graph_widget import GraphWidget
from ui.control_buttons import ControlButtons
from ui.settings_ui import SettingsUI
from ui.print_ui import PrintUI
from sensors.arduino_reader import ArduinoReader
from algorithms.data_analysis import analyze_and_save

class ChocoMonitorUI(QWidget):
    def __init__(self, arduino_reader):
        super().__init__()
        self.setWindowTitle("ChocoMonitor - Temperature Analyzer")
        self.setGeometry(100, 100, 1024, 600)
        self.arduino_reader = arduino_reader

        main_layout = QVBoxLayout()

        # Top Bar
        self.top_bar = QHBoxLayout()
        self.time_label = QLabel()
        self.time_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.temp_label = QLabel("Temperature: -- °C")
        self.temp_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.top_bar.addWidget(self.time_label)
        self.top_bar.addStretch()
        self.top_bar.addWidget(self.temp_label)

        # Main Display (Real-time Temperature)
        self.main_display = QLabel("--")
        self.main_display.setFont(QFont("Arial", 60, QFont.Weight.Bold))
        self.main_display.setStyleSheet("color: yellow;")

        # Graph Display
        self.graph_widget = GraphWidget(self.arduino_reader)

        # Control Buttons
        self.buttons_widget = ControlButtons()
        self.buttons_widget.start_clicked.connect(self.start_graph)
        self.buttons_widget.stop_clicked.connect(self.stop_graph)
        self.buttons_widget.settings_clicked.connect(self.open_settings)
        self.buttons_widget.reset_clicked.connect(self.reset_graph)

        # Bottom Bar
        self.bottom_bar = QHBoxLayout()
        self.bottom_bar.addWidget(self.buttons_widget)

        # Sidebar Menu (Collapsible)
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("background-color: gray;")
        self.sidebar.hide()
        self.toggle_sidebar_button = QPushButton("☰")
        self.toggle_sidebar_button.setFixedSize(50, 50)
        self.toggle_sidebar_button.clicked.connect(self.toggle_sidebar)

        main_layout.addLayout(self.top_bar)
        main_layout.addWidget(self.main_display, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.graph_widget)
        main_layout.addLayout(self.bottom_bar)
        main_layout.addWidget(self.toggle_sidebar_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

        # Timer to update time and temp
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(1000)

    def start_graph(self):
        self.graph_widget.start_graph()

    def stop_graph(self):
        self.graph_widget.stop_graph()

    def reset_graph(self):
        self.graph_widget.stop_graph()
        self.graph_widget.start_graph()
        print("🔄 Graph reset.")

    def open_settings(self):
        self.settings_window = SettingsUI(self)
        self.settings_window.show()

    def update_display(self):
        current_time = QDateTime.currentDateTime().toString("dd/MM/yyyy HH:mm")
        self.time_label.setText(current_time)
        temperature = self.arduino_reader.get_latest_temperature()
        if temperature is not None:
            self.temp_label.setText(f"Temperature: {temperature:.2f} °C")
            self.main_display.setText(f"{temperature:.2f}")
        else:
            self.temp_label.setText("Temperature: -- °C")
            self.main_display.setText("--")

    def toggle_sidebar(self):
        if self.sidebar.isVisible():
            self.sidebar.hide()
        else:
            self.sidebar.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    arduino_reader = ArduinoReader()
    arduino_reader.start_reading()
    window = ChocoMonitorUI(arduino_reader)
    window.show()
    sys.exit(app.exec())