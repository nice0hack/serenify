from routes.base_routes import BaseRoutes
from schemas import SServices, SServicesInDB, SServicesCreate
from sqlalchemy.ext.asyncio import AsyncSession
from core.utils.register_router import register_router
from controllers import ServicesController
from fastapi import Depends
from core.db import get_session


@register_router
class ServiceRoutes(BaseRoutes):
    tag = "Service"

    def _register_routes(self):

        @self.router.post("/services/", tags=[self.tag])
        async def create_service(
            service: SServicesCreate,
            session: AsyncSession = Depends(get_session),
        ):
            controller = ServicesController(session=session)
            return await controller.create_service(service)

        @self.router.get("/services/", response_model=list[SServicesInDB], tags=[self.tag])
        async def get_all(session: AsyncSession = Depends(get_session)):
            controller = ServicesController(session=session)
            return await controller.get_all()

        @self.router.get("/services/{service_id}", response_model=SServicesInDB, tags=[self.tag])
        async def get_by_id(
            service_id: int, session: AsyncSession = Depends(get_session)
        ):
            controller = ServicesController(session=session)
            return await controller.get_by_id(service_id)
        
        @self.router.get("/services/search/{query}", response_model=list[SServicesInDB], tags=[self.tag])
        async def search_services(query: str, session: AsyncSession = Depends(get_session)):
            controller = ServicesController(session=session)
            return await controller.search_services(query)