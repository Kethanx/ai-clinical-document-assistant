from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "message": "Upload endpoint working"
    }