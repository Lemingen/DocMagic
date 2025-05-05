import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from app.settings.config import settings
from app.settings.database import Base
from app.models.models import DocumentsOrm, DocumentsTextOrm

# Подключаем тестовую БД SQLite в памяти
engine = create_engine(settings.sync_database_url, echo=False)
SessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)
    clear_mappers()

def test_create_document(db_session):
    doc = DocumentsOrm(path="/some/path/doc.pdf", date=datetime.date(2024, 1, 1))
    db_session.add(doc)
    db_session.commit()

    result = db_session.query(DocumentsOrm).first()
    assert result is not None
    assert result.path == "/some/path/doc.pdf"
    assert result.date == datetime.date(2024, 1, 1)

def test_create_document_text(db_session):
    # Сначала создаём сам документ
    doc = DocumentsOrm(path="/another/path.pdf", date=datetime.date(2023, 12, 12))
    db_session.add(doc)
    db_session.commit()

    text = DocumentsTextOrm(id_doc=doc.id, text="Extracted text from document.")
    db_session.add(text)
    db_session.commit()

    result = db_session.query(DocumentsTextOrm).first()
    assert result is not None
    assert result.text == "Extracted text from document."
    assert result.id_doc == doc.id
