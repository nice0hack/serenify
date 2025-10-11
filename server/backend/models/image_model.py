from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from core.db import Base

class ImageModel(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    url = Column(String, nullable=False)
    hash = Column(String, nullable=False, unique=True)
    alt = Column(String, nullable=True)
    title = Column(String, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    links = relationship("FileLinkModel", back_populates="image", cascade="all, delete")

