from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import MonitoringData, Base 

engine = create_engine('sqlite:///monitoring.db')
Session = sessionmaker(bind=engine)
session = Session()

records = session.query(MonitoringData).all()

for record in records:
    print(f"ID: {record.id}, CPU: {record.cpu}%, RAM: {record.ram}%, Disk: {record.disk}%")


session.close()
