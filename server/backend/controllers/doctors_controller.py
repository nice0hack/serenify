from controllers.base_controller import BaseController
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select
from sqlalchemy.orm import selectinload
from fastapi import UploadFile, HTTPException
from core.utils.generate_slots import get_free_slots_for_month
from models import  DoctorsModel, FileLinkModel, WorkerWeeklyScheduleModel, WorkerExceptionsSheduleModel
from schemas import SDoctorsInDB, SDoctors
from core.utils.file_linker import save_image, create_file_link
from typing import List
import json
from datetime import datetime, date, time, timedelta

class DoctorsController(BaseController[DoctorsModel, SDoctors]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, DoctorsModel, SDoctors)

    async def get_by_id(self, doctor_id: int) -> SDoctorsInDB:
            stmt = (
                select(DoctorsModel)
                .where(DoctorsModel.id == doctor_id)
                .options(
                    selectinload(DoctorsModel.clinics),
                    selectinload(DoctorsModel.images).selectinload(FileLinkModel.image)
                )
            )
            result = await self.session.execute(stmt)
            doctor = result.scalar_one_or_none()
            if not doctor:
                raise HTTPException(status_code=404, detail="Врач не найден")
            doctor.slots = await get_free_slots_for_month(doctor_id=doctor.id, session=self.session)
            return SDoctorsInDB.model_validate(doctor)
    
    async def get_all(self, specialty: str|None = None) -> list[SDoctorsInDB]:
        if specialty is not None:
            stmt = (
            select(DoctorsModel)
            .where(DoctorsModel.specialty == specialty)
            .options(
                selectinload(DoctorsModel.clinics),
                selectinload(DoctorsModel.images).selectinload(FileLinkModel.image)
                )
            )
        else:
            stmt = (
                select(DoctorsModel)
                .options(
                    selectinload(DoctorsModel.clinics),
                    selectinload(DoctorsModel.images).selectinload(FileLinkModel.image)
                )
            )
        result = await self.session.execute(stmt)
        doctors = result.scalars().all()

        for doctor in doctors:
            doctor.slots = await get_free_slots_for_month(doctor_id=doctor.id, session=self.session)
        return [SDoctorsInDB.model_validate(doctor) for doctor in doctors]

    async def create_doctor(self, doctor: str, weekly_schedule: List[dict], exceptions_schedule: List[dict] | None, images: List[UploadFile] = []) -> dict:
        doctor = json.loads(doctor)
        doctor = SDoctors.model_validate(doctor)
        stmt = select(DoctorsModel).where(or_(DoctorsModel.name == doctor.name, DoctorsModel.email == doctor.email))
        result = await self.session.execute(stmt)
        existing_doctor = result.scalar_one_or_none()
        if existing_doctor:
            raise HTTPException(status_code=400, detail="Doctor with this name or email already exists")

        doctor_model = DoctorsModel(**doctor.model_dump())
        self.session.add(doctor_model)
        await self.session.flush()  # получаем ID врача без коммита

        # --- Привязка изображений ---
        for file in images:
            image = await save_image(file, self.session, doctor_model.name, doctor_model.name)
            await create_file_link(self.session, image.id, "doctors", str(doctor_model.id))

        # --- Основное расписание ---
        weekly_schedule = json.loads(weekly_schedule)
        for entry in weekly_schedule:
            entry["doctor_id"] = doctor_model.id

            # Преобразуем строку дня недели в int, если пришло как строка
            if isinstance(entry.get("weekday"), str):
                entry["weekday"] = int(entry["weekday"])

            # Преобразуем время в datetime.time
            if isinstance(entry.get("start_time"), str):
                entry["start_time"] = datetime.strptime(entry["start_time"], "%H:%M:%S").time()
            if isinstance(entry.get("end_time"), str):
                entry["end_time"] = datetime.strptime(entry["end_time"], "%H:%M:%S").time()
            
            if isinstance(entry["slot_duration"], int):
                entry["slot_duration"] = timedelta(minutes=entry["slot_duration"])

            self.session.add(WorkerWeeklyScheduleModel(**entry))


        # --- Исключения в расписании ---
        if exceptions_schedule is not None:
            exceptions_schedule = json.loads(exceptions_schedule)
            for entry in exceptions_schedule:
                entry["doctor_id"] = doctor_model.id

                # Преобразуем дату
                if isinstance(entry.get("date"), str):
                    entry["date"] = datetime.strptime(entry["date"], "%Y-%m-%d").date()

                # Преобразуем время (если есть)
                if isinstance(entry.get("start_time"), str) and entry["start_time"]:
                    entry["start_time"] = datetime.strptime(entry["start_time"], "%H:%M:%S").time()
                if isinstance(entry.get("end_time"), str) and entry["end_time"]:
                    entry["end_time"] = datetime.strptime(entry["end_time"], "%H:%M:%S").time()

                self.session.add(WorkerExceptionsSheduleModel(**entry))

        await self.session.commit()
        return {"success": True, "msg": "Doctor created"}
    
    async def search_doctors(self, query: str):
        if not query:
            stmt = select(DoctorsModel).order_by(DoctorsModel.name.asc())
        else:
            stmt = (
                select(DoctorsModel)
                .where(
                    or_(
                        DoctorsModel.name.ilike(f"%{query}%"),
                        DoctorsModel.specialty.ilike(f"%{query}%"),
                        DoctorsModel.description.ilike(f"%{query}%"),
                    )
                )
                .order_by(DoctorsModel.name.asc())
            )

        result = await self.session.execute(stmt)
        doctors = result.scalars().all()
        return [SDoctorsInDB.model_validate(doctor) for doctor in doctors]