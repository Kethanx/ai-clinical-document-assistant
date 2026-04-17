from pydantic import BaseModel


class Citation(BaseModel):
    document_name: str
    document_title: str
    publication_date: str
    authors: str
    pages: list[int]


class AskQuestionResponse(BaseModel):
    question: str
    answer: str
    citations: list[Citation]