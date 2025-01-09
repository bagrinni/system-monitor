import sys
import psutil
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QProgressBar, QWidget, QPushButton
from PyQt6.QtCore import QTimer
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class MonitoringData(Base):
    __tablename__ = "monitoring_data"

    id = Column(Integer, primary_key=True)
    cpu = Column(Float)
    ram = Column(Float)
    disk = Column(Float)

class Database:
    def __init__(self, db_name):
        self.engine = create_engine(f"sqlite:///{db_name}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def insert_data(self, data):
        session = self.Session()
        new_entry = MonitoringData(cpu=data["cpu"], ram=data["ram"], disk=data["disk"])
        session.add(new_entry)
        session.commit()
        session.close()

class SystemMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Monitor")
        self.setGeometry(100, 100, 300, 300)

        self.database = Database("monitoring.db")
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)

        self.cpu_label = QLabel("CPU Usage:")
        self.cpu_bar = QProgressBar()
        self.layout.addWidget(self.cpu_label)
        self.layout.addWidget(self.cpu_bar)

        self.ram_label = QLabel("RAM Usage:")
        self.ram_bar = QProgressBar()
        self.layout.addWidget(self.ram_label)
        self.layout.addWidget(self.ram_bar)

        self.disk_label = QLabel("Disk Usage:")
        self.disk_bar = QProgressBar()
        self.layout.addWidget(self.disk_label)
        self.layout.addWidget(self.disk_bar)

        self.toggle_button = QPushButton("Начать запись")
        self.toggle_button.clicked.connect(self.toggle_recording)
        self.layout.addWidget(self.toggle_button)

        self.time_label = QLabel("Время записи: 0 сек")
        self.layout.addWidget(self.time_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.recording = False
        self.time_elapsed = 0 
        self.timer.start(1000)

        self.update_time_timer = QTimer(self)
        self.update_time_timer.timeout.connect(self.update_time)

    def update_stats(self):
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage("/").percent

        self.cpu_bar.setValue(int(cpu_usage))
        self.cpu_label.setText(f"CPU Usage: {cpu_usage}%")

        self.ram_bar.setValue(int(ram_usage))
        self.ram_label.setText(f"RAM Usage: {ram_usage}%")

        self.disk_bar.setValue(int(disk_usage))
        self.disk_label.setText(f"Disk Usage: {disk_usage}%")

        if self.recording:
            self.database.insert_data({
                "cpu": cpu_usage,
                "ram": ram_usage,
                "disk": disk_usage
            })

    def update_time(self):
        if self.recording:
            self.time_elapsed += 1
            minutes = self.time_elapsed // 60
            seconds = self.time_elapsed % 60
            self.time_label.setText(f"Время записи: {minutes} мин {seconds} сек")

    def toggle_recording(self):
        self.recording = not self.recording
        button_text = "Остановить запись" if self.recording else "Начать запись"
        self.toggle_button.setText(button_text)

        if self.recording:
            self.time_elapsed = 0
            self.time_label.setText(f"Время записи: {self.time_elapsed} сек")
            self.update_time_timer.start(1000) 
        else:
            self.update_time_timer.stop() 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitor()
    window.show()
    sys.exit(app.exec())
