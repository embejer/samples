from sqlalchemy import Column, Float, String, Integer
from database import Base

class Geolocs(Base):
    __tablename__ = 'Geolocs'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)