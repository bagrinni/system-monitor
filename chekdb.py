from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import MonitoringData, Base  # импортируйте модель MonitoringData

# Подключение к базе данных
engine = create_engine('sqlite:///monitoring.db')
Session = sessionmaker(bind=engine)
session = Session()

# Получаем все записи из таблицы monitoring_data
records = session.query(MonitoringData).all()

# Выводим все записи
for record in records:
    print(f"ID: {record.id}, CPU: {record.cpu}%, RAM: {record.ram}%, Disk: {record.disk}%")

# Закрываем сессию
session.close()
