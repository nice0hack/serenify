from schemas import SNewsBase, SNewsOut
from models import NewsModel, FileLinkModel
from controllers.base_controller import BaseController
from controllers.base_controller import BaseController
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select
from sqlalchemy.orm import selectinload
from fastapi import UploadFile, HTTPException
from typing import List
from core.utils.file_linker import save_image, create_file_link
import json

class NewsController(BaseController[NewsModel, SNewsBase]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, NewsModel, SNewsBase)

    async def get_by_id(self, news_id: int) -> SNewsOut:
        stmt = (
            select(NewsModel)
            .where(NewsModel.id == news_id)
            .options(selectinload(NewsModel.images).selectinload(FileLinkModel.image))
        )
        result = await self.session.execute(stmt)
        news = result.scalar_one_or_none()

        if not news:
            raise HTTPException(status_code=404, detail="Новость не найдена")

        return SNewsOut.model_validate(news)

    # --- Получить все новости ---
    async def get_all(self) -> list[SNewsOut]:
        stmt = (
            select(NewsModel)
            .options(selectinload(NewsModel.images).selectinload(FileLinkModel.image))
        )
        result = await self.session.execute(stmt)
        news_list = result.scalars().all()
        return [SNewsOut.model_validate(news) for news in news_list]

    # --- Создать новость ---
    async def create_news(
        self,
        news: str,
        images: List[UploadFile] = [],
    ) -> dict:
        news = json.loads(news)
        news = SNewsBase.model_validate(news)

        # Проверяем дубликаты по slug или title
        stmt = select(NewsModel).where(
            or_(
                NewsModel.title == news.title
            )
        )
        result = await self.session.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=400, detail="Новость с таким slug или названием уже существует")

        news_model = NewsModel(**news.model_dump())
        self.session.add(news_model)
        await self.session.flush()  # получить id до коммита

        # Привязка изображений
        for file in images:
            image = await save_image(file, self.session, news_model.title, news_model.title)
            await create_file_link(self.session, image.id, "news", str(news_model.id))

        await self.session.commit()
        return {"success": True, "msg": "Новость успешно создана"}