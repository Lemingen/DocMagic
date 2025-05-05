from typing import List
from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.schemas import DocumentResponse, MessageResponse, TextResponse
from app.view.service import DocumentService, LocalStorage, PostgresRepository
from app.settings.database import get_async_session

app = FastAPI()

def get_document_service(session: AsyncSession = Depends(get_async_session)) -> DocumentService:
    storage = LocalStorage()
    repository = PostgresRepository(session=session)
    return DocumentService(storage=storage, repository=repository)

@app.post(
    "/upload_files/",
    summary="Загрузка картинок",
    description="Загружает один или несколько картинок на сервер и сохраняет путь и дату в базу данных.",
    response_description="Успешная загрузка картинок",
    response_model=List[DocumentResponse],
    responses={
        201: {"description": "Картинкa(и) успешно загружены"},
        422: {"description": "Ошибка валидации файлов (например, пустой список)"}
    }
)
async def upload_file(
    files: List[UploadFile] = File(...),
    service: DocumentService = Depends(get_document_service),
):
    return await service.upload_file(files)

@app.delete(
    "/delete_files/{id_doc}",
    summary="Удаление картинок",
    description="Удаляет картинку с сервера и запись о нёй из базы данных по id_doc.",
    responses={
        200: {"description": "Файл успешно удалён"},
        404: {"description": "Документ не найден"}
    },
    response_model=MessageResponse
)
async def delete_file(
    id_doc: int,
    service: DocumentService = Depends(get_document_service),
):
    await service.delete_file(id_doc)
    return {"message": f"Документ с ID {id_doc} успешно удалён."}

@app.post(
    '/doc_analyse/{id_doc}',
    summary="Поставить картинку в очередь на обработку",
    description="Отправляет задачу по анализу картинки по id_doc в очередь Celery.",
    responses={
        200: {"description": "Документ поставлен в очередь"},
        404: {"description": "Документ не найден"}
    },
    response_model=MessageResponse
)
async def doc_analyse(
    id_doc: int,
    service: DocumentService = Depends(get_document_service),
):
    service.doc_analyse(id_doc)
    return {"message": f"Картинка {id_doc} поставлена в очередь на обработку."}

@app.get(
    '/get_text/{id_doc}',
    summary="Получение текста картинки",
    description="Возвращает ранее извлечённый текст из картинки по его id_doc из DocumentsTextOrm.",
    responses={
        200: {"description": "Текст успешно получен"},
        404: {"description": "Документ с текстом не найден"}
    },
    response_model=TextResponse
)
async def get_text(
    id_doc: int,
    service: DocumentService = Depends(get_document_service)
):
    text = await service.get_text(id_doc)
    return {"text": text}