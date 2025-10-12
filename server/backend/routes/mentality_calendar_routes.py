from fastapi import Depends
from pydantic import Field
from routes.base_routes import BaseRoutes
from core.utils.register_router import register_router
from controllers import MentalityCalendarController
from sqlalchemy.ext.asyncio import AsyncSession
from core.utils.permissions import get_current_user
from core.db import get_session
from schemas import SUserTokenPayload, SMentalityCalendar


@register_router
class MentalityCalendarRoutes(BaseRoutes):
    tag = "Mentality Calendar"

    def _register_routes(self):

        @self.router.get("/calendars/", tags=[self.tag])
        async def get_by_user(
            user: SUserTokenPayload = Depends(get_current_user),
            session: AsyncSession = Depends(get_session),
        ):
            controller = MentalityCalendarController(session=session)
            return await controller.get_by_user(user)

        @self.router.post("/calendars/", tags=[self.tag])
        async def create_update_calendar(
            calendar: SMentalityCalendar,
            user: SUserTokenPayload = Depends(get_current_user),
            session: AsyncSession = Depends(get_session),
        ):
            controller = MentalityCalendarController(session=session)
            return await controller.create_and_update_calendar(
                user=user, calendar=calendar
            )
