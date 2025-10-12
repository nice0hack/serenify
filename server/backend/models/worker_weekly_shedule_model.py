from sqlalchemy import Interval, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship, mapped_column, Mapped
from core.db import Base
import datetime

class WorkerWeeklyScheduleModel(Base):
    __tablename__ = "worker_weekly_schedule"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False
    )
    weekday: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 1 = Понедельник
    start_time: Mapped[datetime.time] = mapped_column(nullable=False)
    end_time: Mapped[datetime.time] = mapped_column(nullable=False)
    slot_duration: Mapped[datetime.timedelta] = mapped_column(
        Interval,
        default="30 minutes",
        nullable=True
    )  # например, шаг записи

    doctors = relationship("DoctorsModel", back_populates="weekly_schedule")
