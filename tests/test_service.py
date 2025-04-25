import pytest
import os
from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException

from app.models.models import DocumentsOrm, DocumentsTextOrm
from app.view.service import DocumentService


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def service():
    return DocumentService()


@pytest.mark.asyncio
async def test_delete_file_success(service, mock_session):
    doc = DocumentsOrm(id=1, path="documents/test.png", date=date.today())

    with patch("app.view.service.async_session_factory", return_value=mock_session), \
            patch("os.path.exists", return_value=True), \
            patch("os.remove") as mock_remove:
        mock_session.__aenter__.return_value = mock_session
        mock_session.execute.return_value.scalar_one_or_none = MagicMock(return_value=doc)

        await service.delete_file(1)

        mock_remove.assert_called_once_with("documents/test.png")
        mock_session.delete.assert_called_once_with(doc)
        mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_file_not_found(service, mock_session):
    with patch("app.view.service.async_session_factory", return_value=mock_session):
        mock_session.__aenter__.return_value = mock_session
        mock_session.execute.return_value.scalar_one_or_none = MagicMock(return_value=None)

        with pytest.raises(HTTPException) as exc_info:
            await service.delete_file(1)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Document not found"


@pytest.mark.asyncio
async def test_get_text_success(service, mock_session):
    text_obj = DocumentsTextOrm(id_doc=1, text="Текст документа")

    with patch("app.view.service.async_session_factory", return_value=mock_session):
        mock_session.__aenter__.return_value = mock_session
        mock_session.execute.return_value.scalar_one_or_none = MagicMock(return_value=text_obj)

        result = await service.get_text(1)
        assert result == "Текст документа"


@pytest.mark.asyncio
async def test_get_text_not_found(service, mock_session):
    with patch("app.view.service.async_session_factory", return_value=mock_session):
        mock_session.__aenter__.return_value = mock_session
        mock_session.execute.return_value.scalar_one_or_none = MagicMock(return_value=None)

        with pytest.raises(HTTPException) as exc_info:
            await service.get_text(1)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Текст документа не найден"
