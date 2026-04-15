from pydantic import BaseModel


class Citation(BaseModel):
    document_name: str
    page_number: int


class AskQuestionResponse(BaseModel):
    question: str
    answer: str
    citations: list[Citation]