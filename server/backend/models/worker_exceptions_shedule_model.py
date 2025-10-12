from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from core.db import Base
import datetime

class WorkerExceptionsSheduleModel(Base):
    __tablename__ = "worker_schedule_exceptions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False
    )
    date: Mapped[datetime.date] = mapped_column(nullable=False)
    is_day_off: Mapped[bool] = mapped_column( default=False)  # выходной день
    start_time: Mapped[datetime.time] = mapped_column(nullable=True)
    end_time: Mapped[datetime.time] = mapped_column(nullable=True)

    doctors = relationship("DoctorsModel", back_populates="exceptions_schedule")
