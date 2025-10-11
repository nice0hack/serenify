from sqlalchemy import Column, Integer, String, ForeignKey
from core.db import Base
from sqlalchemy.orm import relationship

class FileLinkModel(Base):
    __tablename__ = "file_links"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("images.id", ondelete="CASCADE"), nullable=False)
    linked_type = Column(String, nullable=False)  # "post", "setting" и т.д.
    linked_id = Column(String, nullable=False)    # ID поста или название настройки

    image = relationship("ImageModel", back_populates="links", lazy="selectin")

