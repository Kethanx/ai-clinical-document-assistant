from pydantic import BaseModel
from typing import List


class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    document_name: str
    page_number: int
    chunk_text: str
    embedding: List[float] | None = None