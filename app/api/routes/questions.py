from fastapi import APIRouter

from app.api.models.request_models import AskQuestionRequest
from app.api.models.response_models import AskQuestionResponse, Citation
from app.api.services.document_metadata import get_document_metadata
from app.api.services.memory_store import memory_service
from app.api.services.openai_service import OpenAIService
from app.api.services.search_service import SearchService

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/ask", response_model=AskQuestionResponse)
async def ask_question(request: AskQuestionRequest):
    openai_service = OpenAIService()
    search_service = SearchService()

    conversation_history = memory_service.format_history(request.conversation_id)

    rewritten_question = openai_service.rewrite_query(
        question=request.question,
        conversation_history=conversation_history,
    )

    question_embedding = openai_service.create_embedding(rewritten_question)

    retrieved_chunks = search_service.vector_search(
        query_text=rewritten_question,
        embedding=question_embedding,
        top_k=request.top_k,
    )

    answer = openai_service.generate_grounded_answer(
        question=request.question,
        chunks=retrieved_chunks,
        conversation_history=conversation_history,
    )

    memory_service.add_turn(
        conversation_id=request.conversation_id,
        question=request.question,
        answer=answer,
    )

    grouped_citations = {}

    for chunk in retrieved_chunks:
        document_name = chunk["document_name"]
        page_number = chunk["page_number"]

        if document_name not in grouped_citations:
            metadata = get_document_metadata(document_name)

            grouped_citations[document_name] = {
                "document_name": document_name,
                "document_title": metadata["document_title"],
                "publication_date": metadata["publication_date"],
                "authors": metadata["authors"],
                "pages": set(),
            }

        grouped_citations[document_name]["pages"].add(page_number)

    citations = [
        Citation(
            document_name=value["document_name"],
            document_title=value["document_title"],
            publication_date=value["publication_date"],
            authors=value["authors"],
            pages=sorted(value["pages"]),
        )
        for value in grouped_citations.values()
    ]

    citations.sort(key=lambda c: c.document_title)

    if "not available in the references" in answer.lower():
        citations = []

    return AskQuestionResponse(
        question=request.question,
        answer=answer,
        citations=citations,
    )