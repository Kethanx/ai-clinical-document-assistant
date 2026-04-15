from fastapi import APIRouter

from app.api.models.request_models import AskQuestionRequest
from app.api.models.response_models import AskQuestionResponse, Citation
from app.api.services.openai_service import OpenAIService
from app.api.services.search_service import SearchService

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/ask", response_model=AskQuestionResponse)
async def ask_question(request: AskQuestionRequest):
    openai_service = OpenAIService()
    search_service = SearchService()

    question_embedding = openai_service.create_embedding(request.question)

    retrieved_chunks = search_service.vector_search(
        embedding=question_embedding,
        top_k=request.top_k,
    )

    answer = openai_service.generate_grounded_answer(
        question=request.question,
        chunks=retrieved_chunks,
    )

    citations = [
        Citation(
            document_name=chunk["document_name"],
            page_number=chunk["page_number"],
        )
        for chunk in retrieved_chunks
    ]

    return AskQuestionResponse(
        question=request.question,
        answer=answer,
        citations=citations,
    )