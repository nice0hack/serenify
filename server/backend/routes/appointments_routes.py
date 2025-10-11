from controllers import AppointmentsController
from routes.base_routes import BaseRoutes
from fastapi import Depends
from core.utils.register_router import register_router
from core.utils.permissions import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_session
from schemas import SAppointments,SAppointmentsInDB, SUserTokenPayload

@register_router
class AppointmentsRoutes(BaseRoutes):
    tag = "Appointments"

    def _register_routes(self):

        @self.router.post("/appointments/", response_model=dict, tags=[self.tag])
        async def book_appointment(
            appointment: SAppointments,
            user: SUserTokenPayload = Depends(get_current_user),
            session: AsyncSession = Depends(get_session),
        ):
            controller = AppointmentsController(session=session)
            return await controller.book_appointment(appointment, user)

        @self.router.post("/appointments/{appointment_id}/cancel", response_model=dict, tags=[self.tag])
        async def cancel_appointment(
            appointment_id: int,
            user: SUserTokenPayload = Depends(get_current_user),
            session: AsyncSession = Depends(get_session),
        ):
            controller = AppointmentsController(session=session)
            return await controller.cancel_appointment(appointment_id, user)

        @self.router.post("/appointments/{appointment_id}/complete", response_model=dict, tags=[self.tag])
        async def complete_appointment(
            appointment_id: int,
            user: SUserTokenPayload = Depends(get_current_user),
            session: AsyncSession = Depends(get_session),
        ):
            controller = AppointmentsController(session=session)
            return await controller.complete_appointment(appointment_id, user)
        
        @self.router.get("/appointments/", response_model=list[SAppointmentsInDB], tags=[self.tag])
        async def get_appointments(
            user: SUserTokenPayload = Depends(get_current_user),
            session: AsyncSession = Depends(get_session),
        ):
            controller = AppointmentsController(session=session)
            return await controller.get_appointments_for_user(user)
