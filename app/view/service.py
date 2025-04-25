from datetime import date
from app.models.models import DocumentsOrm, DocumentsTextOrm
import os, shutil
from fastapi import UploadFile, HTTPException
from sqlalchemy import select

from app.schemas.schemas import DocumentResponse
from app.tasks.tasks import process_doc
from app.settings.database import async_session_factory



class DocumentService:
    async def upload_file(self, files: list[UploadFile]):
        UPLOAD_DIR = 'documents'
        doc_lst = []
        for file in files:
            file_location = os.path.join(UPLOAD_DIR, file.filename)  # Путь к файлу в папке
            with open(file_location, "wb") as f:
                shutil.copyfileobj(file.file, f)
            doc_lst.append(DocumentsOrm(
                path=file_location,
                date=date.today()
            ))
        async with async_session_factory() as session:
            session.add_all(doc_lst)
            await session.commit()

        return [DocumentResponse(path=doc.path, date=doc.date) for doc in doc_lst]

    async def delete_file(self, id_doc: int):
        async with async_session_factory() as session:
            query = select(DocumentsOrm).where(DocumentsOrm.id == id_doc)
            result = await session.execute(query)
            doc = result.scalar_one_or_none()

            if not doc:
                raise HTTPException(status_code=404, detail="Document not found")

            if os.path.exists(doc.path):
                os.remove(doc.path)

            await session.delete(doc)
            await session.commit()

    def doc_analyse(self, id_doc: int):
        process_doc.apply_async([id_doc])

    async def get_text(self, id_doc: int):
        async with async_session_factory() as session:
            query = select(DocumentsTextOrm).where(DocumentsTextOrm.id_doc == id_doc)
            result = await session.execute(query)
            text_msg = result.scalar_one_or_none()

            if not text_msg:
                raise HTTPException(status_code=404, detail="Текст документа не найден")

        return text_msg.text