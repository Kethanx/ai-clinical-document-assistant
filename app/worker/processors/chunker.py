from typing import List
from uuid import uuid4

from app.shared.schemas.chunk import DocumentChunk


def chunk_pages(
    pages: List[dict],
    document_id: str,
    document_name: str,
    chunk_size: int = 1000,
    overlap: int = 100,
) -> List[DocumentChunk]:
    chunks: List[DocumentChunk] = []

    for page in pages:
        page_number = page["page_number"]
        text = page["text"]

        if not text:
            continue

        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    DocumentChunk(
                        chunk_id=str(uuid4()),
                        document_id=document_id,
                        document_name=document_name,
                        page_number=page_number,
                        chunk_text=chunk_text,
                    )
                )

            if end >= text_length:
                break

            start += chunk_size - overlap

    return chunks