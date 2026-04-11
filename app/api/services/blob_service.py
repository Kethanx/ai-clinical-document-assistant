from azure.storage.blob import BlobServiceClient
from app.api.core.config import (
    AZURE_STORAGE_CONNECTION_STRING,
    BLOB_CONTAINER_NAME,
)

class BlobService:
    def __init__(self):
        if not AZURE_STORAGE_CONNECTION_STRING:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING is not set")

        self.container_name = BLOB_CONTAINER_NAME
        self.blob_service_client = BlobServiceClient.from_connection_string(
            AZURE_STORAGE_CONNECTION_STRING
        )

    def upload_file(self, file_name: str, data: bytes) -> str:
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name,
            blob=file_name
        )
        blob_client.upload_blob(
        data,
        overwrite=True,
        content_type="application/pdf"
    )
        return blob_client.url