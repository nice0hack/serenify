from sqlalchemy import DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime
from core.db import Base


class ImageModel(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    hash: Mapped[str] = mapped_column(nullable=False, unique=True)
    alt: Mapped[str] = mapped_column(nullable=True)
    title: Mapped[str] = mapped_column(nullable=True)
    uploaded_at: Mapped[DateTime] = mapped_column(DateTime,default=datetime.utcnow)

    links = relationship("FileLinkModel", back_populates="image", cascade="all, delete")
