from fastapi import APIRouter

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/ask")
async def ask_question(question: str):
    return {
        "question": question,
        "answer": "RAG pipeline not implemented yet"
    }