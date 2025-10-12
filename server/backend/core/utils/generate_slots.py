from datetime import datetime, timedelta, time
from sqlalchemy import select, and_
from models import WorkerWeeklyScheduleModel, WorkerExceptionsSheduleModel, AppointmentsModel
import calendar
from sqlalchemy.ext.asyncio import AsyncSession

async def get_free_slots(doctor_id: int, date_: datetime.date, session: AsyncSession):
        weekday = date_.isoweekday()

        # Проверяем исключения (например, выходной)
        exception_stmt = select(WorkerExceptionsSheduleModel).where(
            and_(
                WorkerExceptionsSheduleModel.doctor_id == doctor_id,
                WorkerExceptionsSheduleModel.date == date_
            )
        )
        exception = (await session.execute(exception_stmt)).scalars().first()

        if exception and exception.is_day_off:
            return []  # Выходной день

        if exception and exception.start_time and exception.end_time:
            start, end = exception.start_time, exception.end_time
        else:
            # Берём стандартное расписание
            schedule_stmt = select(WorkerWeeklyScheduleModel).where(
                and_(
                    WorkerWeeklyScheduleModel.doctor_id == doctor_id,
                    WorkerWeeklyScheduleModel.weekday == weekday
                )
            )
            schedule = (await session.execute(schedule_stmt)).scalars().first()
            if not schedule:
                return []  # Нет расписания
            start, end = schedule.start_time, schedule.end_time

        # Получаем все записи на этот день
        appointments_stmt = select(AppointmentsModel).where(
            and_(
                AppointmentsModel.doctor_id == doctor_id,
                AppointmentsModel.date == date_,
                AppointmentsModel.status == "booked"
            )
        )
        appointments = (await session.execute(appointments_stmt)).scalars().all()

        # Создаём интервалы по 30 минут (можно заменить на schedule.slot_duration)
        slot_duration = schedule.slot_duration
        slots = []
        current = datetime.combine(date_, start)
        end_datetime = datetime.combine(date_, end)

        # Генерируем все потенциальные слоты
        while current + slot_duration <= end_datetime:
            slot_start = current.time()
            slot_end = (current + slot_duration).time()

            # Проверяем пересечения с существующими записями
            conflict = any(
                (a.start_time.strftime("%H:%M") < slot_end.strftime("%H:%M") and a.end_time.strftime("%H:%M") > slot_start.strftime("%H:%M"))
                for a in appointments
            )

            if not conflict:
                slots.append({
                    "start": slot_start.strftime("%H:%M"),
                    "end": slot_end.strftime("%H:%M")
                })

            current += slot_duration

        return slots

async def get_free_slots_for_month(doctor_id: int, session: AsyncSession) -> list[dict]:
    today = datetime.today().date()
    end_date = today + timedelta(days=30)
    free_slots = []

    current_date = today
    while current_date <= end_date:
        slots = await get_free_slots(doctor_id=doctor_id, date_=current_date, session=session)
        free_slots.append({current_date.isoformat(): slots})
        current_date += timedelta(days=1)

    return free_slots