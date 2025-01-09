from sqlalchemy import create_engine, Column, Integer, Float, Table, MetaData
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
