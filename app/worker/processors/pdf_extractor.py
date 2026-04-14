from typing import List, Dict
from pypdf import PdfReader


def extract_pages_from_pdf(file_path: str) -> List[Dict]:
    reader = PdfReader(file_path)
    pages = []

    for index, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()
        if page_text and page_text.strip():
            pages.append({
                "page_number": index,
                "text": page_text.strip()
            })

    return pages