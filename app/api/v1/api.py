from typing import List
from fastapi import FastAPI, UploadFile, File
from app.schemas.schemas import DocumentResponse, MessageResponse, TextResponse
from app.view.service import DocumentService

app = FastAPI()

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
async def upload_file(files: List[UploadFile] = File(...)):
    service = DocumentService()
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
async def delete_file(id_doc: int):
    service = DocumentService()
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
async def doc_analyse(id_doc: int):
    service = DocumentService()
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
async def get_text(id_doc: int):
    service = DocumentService()
    text = await service.get_text(id_doc)
    return {"text": text}