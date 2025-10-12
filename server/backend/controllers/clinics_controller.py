from core.utils.generate_slots import get_free_slots_for_month
from controllers.base_controller import BaseController
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select, func, cast, Float, literal
from sqlalchemy.orm import selectinload
from fastapi import Form, HTTPException
from models import ClinicsModel, FileLinkModel, ServicesClinicsModel
from schemas import SClinics, SClinicsInDB, SClinicsWithImages
from core.utils.file_linker import save_image, create_file_link
from fastapi import UploadFile
from typing import List
import json


class ClinicsController(BaseController[ClinicsModel, SClinics]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ClinicsModel, SClinics)

    async def get_by_id(
        self, clinic_id: int, coordinates: str | None = None
    ) -> SClinicsInDB:

        user_lat, user_lon = (
            map(float, coordinates.split(",")) if coordinates else (None, None)
        )

        lat_expr = cast(func.split_part(ClinicsModel.coordinates, ",", 1), Float)
        lon_expr = cast(func.split_part(ClinicsModel.coordinates, ",", 2), Float)

        distance_expr = (
            6371
            * func.acos(
                func.cos(func.radians(literal(user_lat)))
                * func.cos(func.radians(lat_expr))
                * func.cos(func.radians(lon_expr) - func.radians(literal(user_lon)))
                + func.sin(func.radians(literal(user_lat)))
                * func.sin(func.radians(lat_expr))
            )
        ).label("distance")

        stmt = (
            select(ClinicsModel, distance_expr)
            .where(ClinicsModel.id == clinic_id)
            .options(
                selectinload(ClinicsModel.doctors),
                selectinload(ClinicsModel.services).selectinload(
                    ServicesClinicsModel.service
                ),
                selectinload(ClinicsModel.images).selectinload(
                    FileLinkModel.image
                ),  # вложенная подгрузка
            )
        )
        result = await self.session.execute(stmt)

        clinic = result.one_or_none()
        if not clinic:
            raise HTTPException(status_code=404, detail="Клиника не найдена")

        clinic, distance = clinic
        if distance is None:
            distance = 0
        clinic.distance = round(distance, 1)
        for doctor in clinic.doctors:
            doctor.slots = await get_free_slots_for_month(
                doctor_id=doctor.id, session=self.session
            )

        return SClinicsInDB.model_validate(clinic)

    async def get_all(
        self, sort: str = "name", coordinates: str | None = None
    ) -> list[SClinicsWithImages]:

        if sort not in ["name", "-name", "closest"]:
            raise HTTPException(status_code=400, detail="Неверный параметр сортировки")

        if sort == "closest" and not coordinates:
            raise HTTPException(
                status_code=400, detail="Для сортировки 'closest' требуются координаты"
            )

        user_lat, user_lon = (
            map(float, coordinates.split(",")) if coordinates else (None, None)
        )

        lat_expr = cast(func.split_part(ClinicsModel.coordinates, ",", 1), Float)
        lon_expr = cast(func.split_part(ClinicsModel.coordinates, ",", 2), Float)

        distance_expr = (
            6371
            * func.acos(
                func.cos(func.radians(literal(user_lat)))
                * func.cos(func.radians(lat_expr))
                * func.cos(func.radians(lon_expr) - func.radians(literal(user_lon)))
                + func.sin(func.radians(literal(user_lat)))
                * func.sin(func.radians(lat_expr))
            )
        ).label("distance")

        stmt = (
            select(ClinicsModel, distance_expr)
            .options(
                selectinload(ClinicsModel.images).selectinload(FileLinkModel.image)
            )
            .order_by(
                *(
                    [ClinicsModel.name]
                    if sort == "name"
                    else (
                        [ClinicsModel.name.desc()]
                        if sort == "-name"
                        else [distance_expr]
                    )
                )
            )
        )
        result = await self.session.execute(stmt)
        clinics = result.all()
        list_clinics = []

        for clinic, distance in clinics:
            if distance is None:
                distance = 0

            clinic.distance = round(distance, 1)
            list_clinics.append(SClinicsWithImages.model_validate(clinic))

        return list_clinics

    async def create_clinic(self, clinic: str, images: List[UploadFile] = []):
        clinic = json.loads(clinic)
        clinic = SClinics.model_validate(clinic)
        clinic = SClinics.model_validate(clinic)

        clinic_model = ClinicsModel(**clinic.model_dump())
        self.session.add(clinic_model)
        await self.session.flush()  # получаем ID клиники без коммита

        # --- Привязка изображений ---
        for file in images:
            image = await save_image(
                file, self.session, clinic_model.name, clinic_model.name
            )
            await create_file_link(
                self.session, image.id, "clinics", str(clinic_model.id)
            )

        await self.session.commit()
        return {"success": True, "msg": "Clinic created"}

    async def search_clinics(self, query: str, coordinates: str | None = None):

        user_lat, user_lon = (
            map(float, coordinates.split(",")) if coordinates else (None, None)
        )

        lat_expr = cast(func.split_part(ClinicsModel.coordinates, ",", 1), Float)
        lon_expr = cast(func.split_part(ClinicsModel.coordinates, ",", 2), Float)

        distance_expr = (
            6371
            * func.acos(
                func.cos(func.radians(literal(user_lat)))
                * func.cos(func.radians(lat_expr))
                * func.cos(func.radians(lon_expr) - func.radians(literal(user_lon)))
                + func.sin(func.radians(literal(user_lat)))
                * func.sin(func.radians(lat_expr))
            )
        ).label("distance")

        if not query:
            stmt = (
                select(ClinicsModel, distance_expr)
                .options(
                    selectinload(ClinicsModel.images).selectinload(FileLinkModel.image)
                )
                .order_by(ClinicsModel.name.asc())
            )
        else:
            stmt = (
                select(ClinicsModel, distance_expr)
                .where(
                    or_(
                        ClinicsModel.name.ilike(f"%{query}%"),
                        ClinicsModel.address.ilike(f"%{query}%"),
                        ClinicsModel.description.ilike(f"%{query}%"),
                    )
                )
                .options(
                    selectinload(ClinicsModel.images).selectinload(FileLinkModel.image)
                )
                .order_by(ClinicsModel.name.asc())
            )

        result = await self.session.execute(stmt)
        clinics = result.all()
        list_clinics = []

        for clinic, distance in clinics:
            if distance is None:
                distance = 0

            clinic.distance = round(distance, 1)
            list_clinics.append(SClinicsWithImages.model_validate(clinic))

        return list_clinics
