from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import DocumentsOrm, DocumentsTextOrm
import os
import shutil
from fastapi import UploadFile, HTTPException
from sqlalchemy import select

from app.schemas.schemas import DocumentResponse
from app.tasks.tasks import process_doc
from abc import ABC, abstractmethod

class FileService(ABC):
    @abstractmethod
    async def saving_files(self, files: list[UploadFile]):
        pass

    @abstractmethod
    async def removing_file(self, doc_path: str):
        pass

class DocumentRepository(ABC):
    @abstractmethod
    async def create_records(self, doc_lst: list[DocumentsOrm]):
        pass

    @abstractmethod
    async def delete_record(self, id_doc: int):
        pass

    @abstractmethod
    async def receive_text(self, id_doc: int):
        pass

class LocalStorage(FileService):
    def __init__(self):
        self.UPLOAD_DIR = 'documents'
        self.doc_lst = []

    async def saving_files(self, files: list[UploadFile]):
        for file in files:
            file_location = os.path.join(self.UPLOAD_DIR, file.filename)
            with open(file_location, "wb") as f:
                shutil.copyfileobj(file.file, f)
            self.doc_lst.append(DocumentsOrm(
                path=file_location,
                date=date.today()
            ))
        return self.doc_lst

    async def removing_file(self, doc_path: str):
        if os.path.exists(doc_path):
            os.remove(doc_path)

class PostgresRepository(DocumentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_records(self, doc_lst: list[DocumentsOrm]):
        self.session.add_all(doc_lst)
        await self.session.commit()

    async def delete_record(self, id_doc: int):
        query = select(DocumentsOrm).where(DocumentsOrm.id == id_doc)
        result = await self.session.execute(query)
        doc = result.scalar_one_or_none()

        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")

        await self.session.delete(doc)
        await self.session.commit()
        return doc.path

    async def receive_text(self, id_doc: int):
        query = select(DocumentsTextOrm).where(DocumentsTextOrm.id_doc == id_doc)
        result = await self.session.execute(query)
        text_msg = result.scalar_one_or_none()

        if not text_msg:
            raise HTTPException(status_code=404, detail="Текст документа не найден")

        return text_msg.text

class DocumentService:
    def __init__(self, storage: FileService, repository: DocumentRepository):
        self.storage = storage
        self.repository = repository

    async def upload_file(self, files: list[UploadFile]):
        doc_lst = await self.storage.saving_files(files)
        await self.repository.create_records(doc_lst)
        return [DocumentResponse(path=doc.path, date=doc.date) for doc in doc_lst]


    async def delete_file(self, id_doc: int):
        doc_path = await self.repository.delete_record(id_doc)
        await self.storage.removing_file(doc_path)

    async def get_text(self, id_doc: int):
        return await self.repository.receive_text(id_doc)

    def doc_analyse(self, id_doc: int):
        process_doc.apply_async([id_doc])