import json
from azure.storage.queue import QueueClient
from app.api.core.config import (
    AZURE_STORAGE_CONNECTION_STRING,
    QUEUE_NAME,
)


class QueueService:
    def __init__(self) -> None:
        if not AZURE_STORAGE_CONNECTION_STRING:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING is not set")

        self.queue_client = QueueClient.from_connection_string(
            conn_str=AZURE_STORAGE_CONNECTION_STRING,
            queue_name=QUEUE_NAME,
        )

    def send_document_for_processing(self, message: dict) -> None:
        self.queue_client.send_message(json.dumps(message))