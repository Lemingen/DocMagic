import pytest
from unittest.mock import AsyncMock, MagicMock
from app.view.service import DocumentService
from app.schemas.schemas import DocumentResponse


@pytest.mark.asyncio
async def test_upload_file():
    mock_file = MagicMock(filename="test.jpg", file=MagicMock())
    mock_storage = AsyncMock()
    mock_repo = AsyncMock()

    # mocked DocumentsOrm instance returned by storage
    mock_doc = MagicMock(path="documents/test.jpg", date="2024-01-01")
    mock_storage.saving_files.return_value = [mock_doc]

    service = DocumentService(storage=mock_storage, repository=mock_repo)
    result = await service.upload_file([mock_file])

    assert result == [DocumentResponse(path="documents/test.jpg", date="2024-01-01")]
    mock_storage.saving_files.assert_awaited_once()
    mock_repo.create_records.assert_awaited_once_with([mock_doc])


@pytest.mark.asyncio
async def test_delete_file():
    mock_storage = AsyncMock()
    mock_repo = AsyncMock()
    mock_repo.delete_record.return_value = "documents/test.jpg"

    service = DocumentService(storage=mock_storage, repository=mock_repo)
    await service.delete_file(1)

    mock_repo.delete_record.assert_awaited_once_with(1)
    mock_storage.removing_file.assert_awaited_once_with("documents/test.jpg")


@pytest.mark.asyncio
async def test_get_text():
    mock_repo = AsyncMock()
    mock_repo.receive_text.return_value = "some text"
    service = DocumentService(storage=AsyncMock(), repository=mock_repo)

    result = await service.get_text(1)
    assert result == "some text"
    mock_repo.receive_text.assert_awaited_once_with(1)
