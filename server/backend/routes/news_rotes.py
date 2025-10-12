# from typing import List
import json
from schemas import SNewsBase, SNewsOut
from routes.base_routes import BaseRoutes
from controllers import NewsController
from fastapi import Depends, UploadFile, Form
from core.utils.register_router import register_router
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_session


@register_router
class NewsRoutes(BaseRoutes):
    tag = "News"

    def _register_routes(self):
        
        @self.router.post("/news/", tags=[self.tag])
        async def create_doctor(
            news: str = Form(json_schema_extra=SNewsBase.model_json_schema()),
            images: list[UploadFile] = [],
            session: AsyncSession = Depends(get_session),
        ):
            controller = NewsController(session=session)
            return await controller.create_news(news, images)

        @self.router.get(
            "/news/", response_model=list[SNewsOut], tags=[self.tag]
        )
        async def get_all(session: AsyncSession = Depends(get_session)):
            controller = NewsController(session=session)
            return await controller.get_all()

        @self.router.get("/news/{news_id}", response_model=SNewsOut, tags=[self.tag])
        async def get_by_id(
            news_id: int, session: AsyncSession = Depends(get_session)
        ):
            controller = NewsController(session=session)
            return await controller.get_by_id(news_id)
