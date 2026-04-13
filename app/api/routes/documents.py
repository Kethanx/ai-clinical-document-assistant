from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, File, UploadFile

from app.api.services.blob_service import BlobService
from app.api.services.queue_service import QueueService

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    blob_service = BlobService()
    queue_service = QueueService()

    contents = await file.read()
    document_id = str(uuid4())

    blob_name = f"{document_id}-{file.filename}"
    blob_url = blob_service.upload_file(blob_name, contents)

    message = {
        "document_id": document_id,
        "blob_name": blob_name,
        "document_name": file.filename,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
    }

    queue_service.send_document_for_processing(message)

    return {
        "document_id": document_id,
        "filename": file.filename,
        "blob_name": blob_name,
        "blob_url": blob_url,
        "message": "Document uploaded and queued for processing",
    }