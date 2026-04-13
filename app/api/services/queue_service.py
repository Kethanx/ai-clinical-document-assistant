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

    def receive_message(self):
        messages = self.queue_client.receive_messages(messages_per_page=1)
        page = next(messages.by_page(), [])

        for message in page:
            return message

        return None

    def parse_message(self, message) -> dict:
        return json.loads(message.content)

    def delete_message(self, message) -> None:
        self.queue_client.delete_message(
            message.id,
            message.pop_receipt,
        )