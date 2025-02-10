import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
from PyQt6.QtCore import QTimer, QDateTime, Qt
from PyQt6.QtGui import QFont
from ui.graph_widget import GraphWidget
from ui.control_buttons import ControlButtons
from ui.settings_ui import SettingsUI
from sensors.arduino_reader import ArduinoReader

class ChocoMonitorUI(QWidget):
    def __init__(self, arduino_reader):
        super().__init__()
        self.setWindowTitle("ChocoMonitor - Temperature Analyzer")
        self.setGeometry(100, 100, 1280, 720)
        self.setStyleSheet("background-color: #121212; color: white;")
        self.arduino_reader = arduino_reader

        main_layout = QVBoxLayout()

        # Top Bar
        self.top_bar = QHBoxLayout()
        self.time_label = QLabel()
        self.time_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.top_bar.addWidget(self.time_label)
        self.top_bar.addStretch()

        # Graph Display
        self.graph_frame = QFrame()
        self.graph_frame.setStyleSheet("background-color: #1E1E1E; border-radius: 15px; padding: 10px;")
        self.graph_layout = QVBoxLayout()
        self.graph_widget = GraphWidget(self.arduino_reader)
        self.graph_layout.addWidget(self.graph_widget)
        self.graph_frame.setLayout(self.graph_layout)

        # Control Buttons
        self.buttons_layout = QHBoxLayout()
        self.buttons_widget = ControlButtons()
        self.buttons_widget.start_clicked.connect(self.start_graph)
        self.buttons_widget.stop_clicked.connect(self.stop_graph)
        self.buttons_widget.settings_clicked.connect(self.open_settings)

        # Results Button (Replacing Reset Button)
        self.results_button = QPushButton("📂 View Results")
        self.results_button.setStyleSheet("font-size: 20px; padding: 15px; background-color: #007ACC; color: white; border-radius: 10px;")
        self.results_button.setFixedHeight(60)
        self.results_button.clicked.connect(self.open_results)

        self.buttons_layout.addWidget(self.buttons_widget)
        self.buttons_layout.addWidget(self.results_button)

        main_layout.addLayout(self.top_bar)
        main_layout.addWidget(self.graph_frame)
        main_layout.addLayout(self.buttons_layout)

        self.setLayout(main_layout)

        # Timer to update time
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def start_graph(self):
        self.graph_widget.start_graph()

    def stop_graph(self):
        self.graph_widget.stop_graph()

    def open_settings(self):
        self.settings_window = SettingsUI(self)
        self.settings_window.show()

    def open_results(self):
        os.startfile(os.path.abspath("results"))

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("dd/MM/yyyy HH:mm")
        self.time_label.setText(current_time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    arduino_reader = ArduinoReader()
    arduino_reader.start_reading()
    window = ChocoMonitorUI(arduino_reader)
    window.show()
    sys.exit(app.exec())
