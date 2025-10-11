from typing import Any, Type, List, Generic, TypeVar
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import hashlib
# Определяем типовые переменные для модели SQLAlchemy и выходной схемы Pydantic
TModel = TypeVar("TModel")
TSchemaOut = TypeVar("TSchemaOut", bound=BaseModel)

class BaseController(Generic[TModel, TSchemaOut]):
    def __init__(self, session: AsyncSession, model: Type[TModel], schema: Type[TSchemaOut]):
        self.session = session
        self.model = model
        self.schema = schema

    async def get_all(self) -> List[TSchemaOut]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return [self.schema.model_validate(item) for item in items]

    async def get_by_id(self, item_id: int) -> TSchemaOut:
        stmt = select(self.model).where(self.model.id == item_id)
        result = await self.session.execute(stmt)
        item = result.scalars().first()
        if not item:
            raise Exception(f"Item with id={item_id} not found")
        return self.schema.model_validate(item)

    async def delete_by_id(self, item_id: int):
        stmt = select(self.model).where(self.model.id == item_id)
        result = await self.session.execute(stmt)
        item = result.scalars().first()
        if not item:
            raise Exception(f"Item with id={item_id} not found")
        await self.session.delete(item)
        await self.session.commit()

        return {"success": True, "msg": f"Item with id={item_id} deleted"}

    async def check_exists(self, **unique_fields: Any):
        stmt = select(self.model)
        for field_name, value in unique_fields.items():
            stmt = stmt.where(getattr(self.model, field_name) == value)
        result = await self.session.execute(stmt)
        existing = result.scalars().first()
        if existing:
            details = ", ".join(f"{k}='{v}'" for k, v in unique_fields.items())
            raise HTTPException(
                status_code=409,
                detail=f"Object with {details} already exists"
            )