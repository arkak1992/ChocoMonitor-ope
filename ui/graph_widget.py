import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer, pyqtSignal
import numpy as np
import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt

class GraphWidget(QWidget):
    process_completed = pyqtSignal()

    def __init__(self, arduino_reader):
        super().__init__()
        self.arduino_reader = arduino_reader
        self.init_ui()
        self.data_points = []
        self.running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.time_stamps = []  # ✅ إضافة قائمة لتخزين الزمن المرتبط بكل قراءة

    def init_ui(self):
        layout = QVBoxLayout()
        self.graph = pg.PlotWidget()
        self.graph.setBackground("#1A1A1A")
        self.graph.setTitle("Temperature vs Time", color="w", size="18pt")
        self.graph.setLabel("left", "Temperature (°C)", color="white", size="14pt")
        self.graph.setLabel("bottom", "Time (s)", color="white", size="14pt")
        self.curve = self.graph.plot(pen=pg.mkPen(color="c", width=2))
        layout.addWidget(self.graph)
        self.setLayout(layout)

    def start_graph(self):
        if not self.running:
            self.data_points = []
            self.time_stamps = []  # ✅ إعادة تعيين قائمة الزمن عند كل تشغيل جديد
            self.running = True
            self.start_time = datetime.datetime.now()
            self.timer.start(1000)
            print("✅ Graph started")

    def stop_graph(self):
        if self.running:
            self.running = False
            self.timer.stop()
            print("🛑 Graph stopped")
            self.save_results()
            self.process_completed.emit()

    def update_plot(self):
        temperature = self.arduino_reader.get_latest_temperature()
        if temperature is not None:
            elapsed_time = (datetime.datetime.now() - self.start_time).total_seconds()
            self.data_points.append(temperature)
            self.time_stamps.append(elapsed_time)
            self.curve.setData(self.time_stamps, self.data_points)  # ✅ ربط درجات الحرارة بالزمن

    def save_results(self):
        if not self.data_points:
            print("⚠ No data to save")
            return

        folder = "results"
        os.makedirs(folder, exist_ok=True)
        file_name = os.path.join(folder, f"graph_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png")

        plt.figure()
        plt.plot(self.time_stamps, self.data_points, label="Temperature", color='blue')
        plt.xlabel("Time (s)")
        plt.ylabel("Temperature (°C)")
        plt.title("Temperature Graph")
        plt.legend()
        plt.grid()
        plt.savefig(file_name, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"📷 Graph saved at {file_name}")
