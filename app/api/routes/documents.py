from fastapi import APIRouter, UploadFile, File
from app.api.services.blob_service import BlobService

router = APIRouter(prefix="/documents", tags=["Documents"])

blob_service = BlobService()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    contents = await file.read()

    blob_url = blob_service.upload_file(
        file.filename,
        contents
    )

    return {
        "filename": file.filename,
        "blob_url": blob_url
    }