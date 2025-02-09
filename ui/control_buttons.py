from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal

class ControlButtons(QWidget):
    start_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    settings_clicked = pyqtSignal()
    reset_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.start_button = self.create_button("Start", "green", self.start_clicked)
        layout.addWidget(self.start_button)

        self.stop_button = self.create_button("Stop", "red", self.stop_clicked)
        layout.addWidget(self.stop_button)

        self.settings_button = self.create_button("Settings", "blue", self.settings_clicked)
        layout.addWidget(self.settings_button)

        self.reset_button = self.create_button("Reset", "orange", self.reset_clicked, text_color="black")
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

    def create_button(self, text, bg_color, signal, text_color="white"):
        button = QPushButton(text)
        button.setFixedHeight(50)
        button.setStyleSheet(f"font-size: 18px; background-color: {bg_color}; color: {text_color};")
        button.clicked.connect(signal.emit)
        return button
