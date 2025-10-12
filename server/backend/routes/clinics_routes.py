from core.utils.register_router import register_router
from sqlalchemy.ext.asyncio import AsyncSession
from controllers.clinics_controller import ClinicsController
from routes.base_routes import BaseRoutes
from core.db import get_session
from schemas import SClinics, SClinicsInDB, SClinicsWithImages
from fastapi import UploadFile, Depends, Form


@register_router
class ClinicsRoutes(BaseRoutes):

    tag = "Clinics"

    def _register_routes(self):

        @self.router.post("/clinics/", tags=[self.tag])
        async def create_clinic(
            clinic: str = Form(json_schema_extra=SClinics.model_json_schema()),
            images: list[UploadFile] = [],
            session: AsyncSession = Depends(get_session),
        ):
            controller = ClinicsController(session=session)
            return await controller.create_clinic(clinic, images)

        @self.router.get("/clinics/{clinic_id}", response_model=SClinicsInDB, tags=[self.tag])
        async def get_clinic(
            clinic_id: int, coordinates: str | None = None, session: AsyncSession = Depends(get_session)
        ):
            controller = ClinicsController(session=session)
            return await controller.get_by_id(clinic_id, coordinates=coordinates)

        @self.router.get("/clinics/", response_model=list[SClinicsWithImages], tags=[self.tag])
        async def get_clinics(sort: str = "name", coordinates: str | None = None, session: AsyncSession = Depends(get_session)):
            controller = ClinicsController(session=session)
            return await controller.get_all(sort=sort, coordinates=coordinates)

        @self.router.get('/clinics/search/{query}', response_model=list[SClinicsWithImages], tags=[self.tag])
        async def search_clinics(query:str, coordinates: str|None = None, session: AsyncSession = Depends(get_session)):
            controller = ClinicsController(session=session)
            return await controller.search_clinics(query=query, coordinates=coordinates)