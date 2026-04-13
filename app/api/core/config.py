import os
from dotenv import load_dotenv

load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME", "documents")
QUEUE_NAME = os.getenv("QUEUE_NAME", "document-ingestion")
LOCAL_STORAGE_PATH = os.getenv("LOCAL_STORAGE_PATH", "data")