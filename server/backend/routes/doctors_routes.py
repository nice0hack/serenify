# from typing import List
import json
from schemas import SDoctors, SDoctorsInDB, SScheduleEntry, SExceptionEntry
from routes.base_routes import BaseRoutes
from controllers import DoctorsController
from fastapi import Depends, UploadFile, Form
from core.utils.register_router import register_router
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_session


@register_router
class DoctorsRoutes(BaseRoutes):
    tag = "Doctors"

    def _register_routes(self):
        
        @self.router.post("/doctors/", tags=[self.tag])
        async def create_doctor(
            doctor: str = Form(json_schema_extra=SDoctors.model_json_schema()),
            images: list[UploadFile] = [],
            weekly_schedule: list[SScheduleEntry] = Form(json_schema_extra=SScheduleEntry.model_json_schema()),
            exceptions_schedule: str | None = Form(None, json_schema_extra=SExceptionEntry.model_json_schema()),
            session: AsyncSession = Depends(get_session),
        ):
            controller = DoctorsController(session=session)
            return await controller.create_doctor(doctor, weekly_schedule, exceptions_schedule, images)

        @self.router.get(
            "/doctors/", response_model=list[SDoctorsInDB], tags=[self.tag]
        )
        async def get_all(session: AsyncSession = Depends(get_session), specialty: str|None = None):
            controller = DoctorsController(session=session)
            return await controller.get_all(specialty=specialty)

        @self.router.get("/doctors/{doctor_id}", response_model=SDoctorsInDB, tags=[self.tag])
        async def get_by_id(
            doctor_id: int, session: AsyncSession = Depends(get_session)
        ):
            controller = DoctorsController(session=session)
            return await controller.get_by_id(doctor_id)

        @self.router.get("/doctors/search/{query}", response_model=list[SDoctorsInDB], tags=[self.tag])
        async def search_doctors(query: str, session: AsyncSession = Depends(get_session)):
            controller = DoctorsController(session=session)
            return await controller.search_doctors(query)
