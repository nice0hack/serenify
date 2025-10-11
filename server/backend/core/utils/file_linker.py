import hashlib, os, shutil
from uuid import uuid4
from datetime import datetime
from fastapi import UploadFile
from sqlalchemy import select
from models import ImageModel
from sqlalchemy.ext.asyncio import AsyncSession
from models import FileLinkModel

async def save_image(file: UploadFile, db: AsyncSession, alt: str = None, title: str = None) -> ImageModel:
    file_bytes = await file.read()
    file_hash = hashlib.sha256(file_bytes).hexdigest()

    result = await db.execute(select(ImageModel).filter_by(hash=file_hash))
    existing = result.scalar_one_or_none() 
    if existing:
        return existing

    now = datetime.now()
    folder = f"static/uploads/{now.year}/{now.month:02d}/"
    os.makedirs(folder, exist_ok=True)

    ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid4().hex}{ext}"
    file_path = os.path.join(folder, unique_name)

    with open(file_path, "wb") as buffer:
        buffer.write(file_bytes)

    url = f"/images/uploads/{now.year}/{now.month:02d}/{unique_name}"

    image = ImageModel(
        filename=file.filename,
        url=url,
        hash=file_hash,
        alt=alt,
        title=title,
    )
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


async def create_file_link(db: AsyncSession, file_id: int, linked_type: str, linked_id: str) -> FileLinkModel:
    result = await db.execute(select(FileLinkModel).filter_by(
        file_id=file_id,
        linked_type=linked_type,
        linked_id=linked_id
    ))
    existing = result.scalar_one_or_none() 
    if existing:
        return existing

    link = FileLinkModel(
        file_id=file_id,
        linked_type=linked_type,
        linked_id=str(linked_id)
    )
    db.add(link)
    await db.commit()
    await db.refresh(link)
    return link


async def unlink_removed_links(
    db: AsyncSession,
    linked_type: str,
    linked_id: str,
    new_file_ids: set[int]
):
    result = await db.execute(select(FileLinkModel).filter_by(
        linked_type=linked_type,
        linked_id=linked_id
    ))
    old_links = result.scalars().all()

    for link in old_links:
        if link.file_id not in new_file_ids:
            await db.delete(link)
    await db.commit()


# def get_or_create_link(
#     db: Session,
#     file_id: int,
#     linked_type: str,
#     linked_id: str
# ) -> FileLinkModel:
#     exists = db.query(FileLinkModel).filter_by(
#         file_id=file_id,
#         linked_type=linked_type,
#         linked_id=str(linked_id)
#     ).first()
#     if exists:
#         return exists

#     link = FileLinkModel(
#         file_id=file_id,
#         linked_type=linked_type,
#         linked_id=str(linked_id)
#     )
#     db.add(link)
#     db.commit()
#     db.refresh(link)
#     return link
