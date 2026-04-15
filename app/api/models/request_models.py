from pydantic import BaseModel


class AskQuestionRequest(BaseModel):
    question: str
    top_k: int = 5