from celery import Celery
from app.settings.database import sync_session_factory
from sqlalchemy import select
from app.models.models import DocumentsOrm, DocumentsTextOrm
from app.settings.config import settings
import pytesseract
from PIL import Image


celery_app = Celery("tasks", broker=settings.get_broker_url)

@celery_app.task
def process_doc(id_doc: int):
    ...
    with sync_session_factory() as session:
        query = select(DocumentsOrm).where(DocumentsOrm.id == id_doc)
        result = session.execute(query)
        doc_path = (result.scalar_one_or_none()).path

        image = Image.open(doc_path)
        text = pytesseract.image_to_string(image)
        session.add(DocumentsTextOrm(
            id_doc = id_doc,
            text = text
        ))
        session.commit()