from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer

class SensorWidget(QWidget):
    def __init__(self, arduino_reader):
        super().__init__()
        self.arduino_reader = arduino_reader
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_temperature)
        self.timer.start(1000)  # تحديث كل ثانية

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("🌡 Temperature: -- °C")
        self.label.setStyleSheet("font-size: 22px; font-weight: bold; color: #00FF00;")
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_temperature(self):
        temp = self.arduino_reader.get_latest_temperature()
        if temp is not None:
            self.label.setText(f"🌡 Temperature: {temp:.2f} °C")  # ✅ عرض الحرارة بدقة منزلتين عشريتين
        else:
            self.label.setText("🌡 Temperature: -- °C")
