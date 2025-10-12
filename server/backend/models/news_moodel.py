from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core.db import Base


class NewsModel(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(index=True)
    html_text: Mapped[str] = mapped_column(TEXT, nullable=False)

    images = relationship(
        "FileLinkModel",
        primaryjoin="and_(foreign(FileLinkModel.linked_id) == cast(NewsModel.id, String), "
        "FileLinkModel.linked_type == 'news')",
        lazy="selectin",
        cascade="all, delete",
        backref="news",
    )