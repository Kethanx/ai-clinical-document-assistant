import os

from app.api.core.config import (
    AZURE_OPENAI_EMBEDDING_DIMENSIONS,
    LOCAL_STORAGE_PATH,
)
from app.api.services.blob_service import BlobService
from app.api.services.queue_service import QueueService
from app.api.services.search_service import SearchService
from app.worker.processors.pdf_extractor import extract_pages_from_pdf
from app.worker.processors.chunker import chunk_pages
from app.api.services.openai_service import OpenAIService


def process_next_document():
    queue_service = QueueService()
    blob_service = BlobService()
    openai_service = OpenAIService()
    search_service = SearchService()

    message = queue_service.receive_message()

    if not message:
        print("No messages in queue.")
        return

    payload = queue_service.parse_message(message)

    document_id = payload["document_id"]
    blob_name = payload["blob_name"]
    document_name = payload["document_name"]

    local_file_path = os.path.join(
        LOCAL_STORAGE_PATH,
        f"{document_id}-{document_name}"
    )

    print(f"Processing document: {document_name}")
    blob_service.download_file(blob_name, local_file_path)

    pages = extract_pages_from_pdf(local_file_path)
    print(f"Extracted text from {len(pages)} pages.")

    chunks = chunk_pages(
        pages=pages,
        document_id=document_id,
        document_name=document_name,
    )
    print(f"Created {len(chunks)} structured chunks.")

    search_docs = []
    for chunk in chunks:
        embedding = openai_service.create_embedding(chunk.chunk_text)
        search_docs.append(
            {
                "chunk_id": chunk.chunk_id,
                "document_id": chunk.document_id,
                "document_name": chunk.document_name,
                "page_number": chunk.page_number,
                "chunk_text": chunk.chunk_text,
                "embedding": embedding,
            }
        )

    search_service.upload_chunks(search_docs)

    queue_service.delete_message(message)
    print("Message deleted from queue after successful processing.")


if __name__ == "__main__":
    process_next_document()