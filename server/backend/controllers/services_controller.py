from fastapi import HTTPException
from schemas import SServicesInDB, SServices, SServicesCreate
from models import ServicesModel, ClinicsModel, ServicesClinicsModel
from controllers.base_controller import BaseController
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select
from sqlalchemy.orm import selectinload


class ServicesController(BaseController[ServicesModel, SServicesInDB]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ServicesModel, SServicesInDB)

    async def get_by_id(self, service_id: int) -> SServicesInDB:
        stmt = (
            select(ClinicsModel)
            .where(ClinicsModel.id == service_id)
            .options(
                selectinload(
                    ClinicsModel.clinics
                )  # Предполагается, что связь называется clinics
            )
        )
        result = await self.session.execute(stmt)
        service = result.scalar_one_or_none()
        if not service:
            raise HTTPException(status_code=404, detail="Услуга не найден")
        return SServicesInDB.model_validate(service)

    async def get_all(self) -> list[SServices]:
        stmt = select(ServicesModel).options(
            selectinload(ServicesModel.clinics).selectinload(
                ServicesClinicsModel.clinic
            )
        )
        result = await self.session.execute(stmt)
        services = result.scalars().all()
        print(services)
        return [SServicesInDB.model_validate(s) for s in services]

    async def create_service(self, service_data: SServicesCreate) -> SServicesInDB:
        service = ServicesModel(**service_data.model_dump(exclude={"clinics"}))
        self.session.add(service)
        await self.session.flush()  # Получаем ID услуги без коммита

        if service_data.clinics:
            clinic_ids = [c["id"] for c in service_data.clinics]
            stmt = select(ClinicsModel).where(ClinicsModel.id.in_(clinic_ids))
            result = await self.session.execute(stmt)
            clinics = result.scalars().all()

            if clinics:
                for c in service_data.clinics:
                    association = ServicesClinicsModel(
                        service_id=service.id, clinic_id=c["id"], price=c["price"]
                    )
                    self.session.add(association)

        await self.session.commit()
        await self.session.refresh(
            service
        )  # Обновляем модель, чтобы получить все данные
        return {"success": True, "msg": "Услуга успешно создана"}

    async def search_services(self, query: str):
        if not query:
            stmt = select(ServicesModel).order_by(ServicesModel.name.asc())
        else:
            stmt = (
                select(ServicesModel)
                .where(
                    or_(
                        ServicesModel.name.ilike(f"%{query}%"),
                        ServicesModel.description.ilike(f"%{query}%"),
                    )
                )
                .options(
                    selectinload(ServicesModel.clinics).selectinload(
                        ServicesClinicsModel.clinic
                    )
                )
                .order_by(ServicesModel.name.asc())
            )

        result = await self.session.execute(stmt)
        services = result.scalars().all()
        return [SServicesInDB.model_validate(service) for service in services]
