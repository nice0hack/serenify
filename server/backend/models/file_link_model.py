from sqlalchemy import Integer, String, ForeignKey
from core.db import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped


class FileLinkModel(Base):
    __tablename__ = "file_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_id: Mapped[str] = mapped_column(
        Integer, ForeignKey("images.id", ondelete="CASCADE"), nullable=False
    )
    linked_type: Mapped[str] = mapped_column(
        String, nullable=False
    )  # "post", "setting" и т.д.
    linked_id: Mapped[str] = mapped_column(
        String, nullable=False
    )  # ID поста или название настройки

    image = relationship("ImageModel", back_populates="links", lazy="selectin")
