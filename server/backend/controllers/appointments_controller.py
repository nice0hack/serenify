from datetime import date, datetime
from models import DoctorsModel, ServicesModel, FileLinkModel, AppointmentsModel
from schemas import SAppointmentsInDB, SAppointments, SUserTokenPayload
from controllers.base_controller import BaseController
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import  HTTPException

class AppointmentsController(BaseController[AppointmentsModel, SAppointments]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AppointmentsModel, SAppointments)

    async def book_appointment(self, appointment: SAppointments, user: SUserTokenPayload) -> int:
        if appointment.doctor_id is None and appointment.services_id is None:
            raise HTTPException(status_code=400, detail="doctor_id или services_id должен быть заполнен")
        if appointment.doctor_id is not None:
            doc_stmt = select(DoctorsModel).where(DoctorsModel.id == appointment.doctor_id)
            result = await self.session.execute(statement=doc_stmt)
            doctor = result.scalar_one_or_none()
            if not doctor:
                raise HTTPException(status_code=404, detail="Врач не найден")
            app_stmt = select(AppointmentsModel).where(
            AppointmentsModel.doctor_id == appointment.doctor_id,
            AppointmentsModel.user_id == user.id,
            AppointmentsModel.status == "booked"
            )
            result = await self.session.execute(statement=app_stmt)
            existing_appointment = result.scalar_one_or_none()
            if existing_appointment:
                raise HTTPException(status_code=400, detail="Appointment already booked")
        else:
            service_stmt = select(ServicesModel).where(ServicesModel.id == appointment.services_id)
            result = await self.session.execute(statement=service_stmt)
            service = result.scalar_one_or_none()
            if not service:
                raise HTTPException(status_code=404, detail="Service not found")
            app_stmt = select(AppointmentsModel).where(
            AppointmentsModel.services_id == appointment.services_id,
            AppointmentsModel.user_id == user.id,
            AppointmentsModel.status == "booked"
            )
            result = await self.session.execute(statement=app_stmt)
            existing_appointment = result.scalar_one_or_none()
            if existing_appointment:
                raise HTTPException(status_code=400, detail="Appointment already booked")
        appointment_data = appointment.model_dump()
        appointment_data["date"] =  datetime.strptime(appointment_data["date"], "%Y-%m-%d").date()
        if appointment_data["start_time"] and appointment_data["end_time"]:
            appointment_data["start_time"] = datetime.strptime(appointment_data["start_time"], "%H:%M").time()
            appointment_data["end_time"] = datetime.strptime(appointment_data["end_time"], "%H:%M").time()
        appointment_data['user_id'] = user.id
        appointment_data['status'] = "booked"
        appointment = AppointmentsModel(**appointment_data)
        self.session.add(appointment)
        await self.session.commit()

        return {"success": True, "msg": "Appointment booked", "appointment_id": appointment.id}
    
    async def cancel_appointment(self, appointment_id: int, user: SUserTokenPayload) -> dict:
        stmt = select(AppointmentsModel).where(
            AppointmentsModel.id == appointment_id,
            AppointmentsModel.user_id == user.id
        )
        result = await self.session.execute(stmt)
        appointment = result.scalar_one_or_none()
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")

        if appointment.status == "cancelled":
            raise HTTPException(status_code=400, detail="Appointment already cancelled")

        appointment.status = "cancelled"
        await self.session.commit()
        return {"success": True, "msg": "Appointment cancelled"}
    
    async def complete_appointment(self, appointment_id: int, user: SUserTokenPayload) -> dict:
        stmt = select(AppointmentsModel).where(
            AppointmentsModel.id == appointment_id,
            AppointmentsModel.user_id == user.id
        )
        result = await self.session.execute(stmt)
        appointment = result.scalar_one_or_none()
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")

        if appointment.status == "completed":
            raise HTTPException(status_code=400, detail="Appointment already completed")

        appointment.status = "completed"
        await self.session.commit()
        return {"success": True, "msg": "Appointment completed"}
    
    async def get_appointments_for_user(self, user: SUserTokenPayload) -> list[SAppointmentsInDB]:
        if user.role ==1:
            stmt = (
            select(AppointmentsModel)
            .where(AppointmentsModel.doctor_id == user.doctor_id)
            .options(
                selectinload(AppointmentsModel.doctors).selectinload(DoctorsModel.images).selectinload(FileLinkModel.image)
                )
            )
        else:
            stmt = (
            select(AppointmentsModel)
            .where(AppointmentsModel.user_id == user.id)
            .options(
                selectinload(AppointmentsModel.doctors).selectinload(DoctorsModel.images).selectinload(FileLinkModel.image)
            )
        )
            
        result = await self.session.execute(stmt)
        appointments = result.scalars().all()

        return [SAppointmentsInDB.model_validate(app).model_dump() for app in appointments]