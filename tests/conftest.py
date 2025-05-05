import pytest
from unittest.mock import MagicMock, AsyncMock
from httpx import AsyncClient
from app.api.v1.api import app
from app.schemas.schemas import DocumentResponse
from app.view.service import DocumentService, LocalStorage, PostgresRepository

@pytest.fixture
async def async_client(mock_document_service):
    app.dependency_overrides[DocumentService] = lambda: mock_document_service
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def mock_document_service():
    # Мокинг класса DocumentService
    mock_service = MagicMock(spec=DocumentService)

    # Мокируем методы
    mock_service.upload_file = AsyncMock(return_value=[
        DocumentResponse(path="documents/file1.jpg", date="2025-05-04"),
        DocumentResponse(path="documents/file2.jpg", date="2025-05-04")
    ])

    mock_service.delete_file = AsyncMock()
    mock_service.get_text = AsyncMock(return_value="Sample text extracted from document.")
    mock_service.doc_analyse = AsyncMock()

    return mock_service


@pytest.fixture
def client(mock_document_service):
    from fastapi.testclient import TestClient
    from app.api.v1.api import app
    app.dependency_overrides[DocumentService] = lambda: mock_document_service
    return TestClient(app)

