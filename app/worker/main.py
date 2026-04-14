import os

from app.api.core.config import LOCAL_STORAGE_PATH
from app.api.services.blob_service import BlobService
from app.api.services.queue_service import QueueService
from app.worker.processors.pdf_extractor import extract_pages_from_pdf
from app.worker.processors.chunker import chunk_pages


def process_next_document():
    queue_service = QueueService()
    blob_service = BlobService()

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
    print(f"Blob name: {blob_name}")

    blob_service.download_file(blob_name, local_file_path)
    print(f"Downloaded to: {local_file_path}")

    pages = extract_pages_from_pdf(local_file_path)
    print(f"Extracted text from {len(pages)} pages.")

    chunks = chunk_pages(
        pages=pages,
        document_id=document_id,
        document_name=document_name,
    )
    print(f"Created {len(chunks)} structured chunks.")

    if chunks:
        first_chunk = chunks[0]
        print("First chunk preview:")
        print({
            "chunk_id": first_chunk.chunk_id,
            "document_id": first_chunk.document_id,
            "document_name": first_chunk.document_name,
            "page_number": first_chunk.page_number,
            "chunk_text_preview": first_chunk.chunk_text[:300],
        })

    queue_service.delete_message(message)
    print("Message deleted from queue after successful processing.")


if __name__ == "__main__":
    process_next_document()