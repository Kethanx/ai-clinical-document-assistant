from openai import AzureOpenAI

from app.api.core.config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
    AZURE_OPENAI_CHAT_DEPLOYMENT,
)


class OpenAIService:
    def __init__(self):
        if not AZURE_OPENAI_ENDPOINT:
            raise ValueError("AZURE_OPENAI_ENDPOINT is not set")
        if not AZURE_OPENAI_API_KEY:
            raise ValueError("AZURE_OPENAI_API_KEY is not set")

        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_version=AZURE_OPENAI_API_VERSION,
        )

    def create_embedding(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
            input=text,
        )
        return response.data[0].embedding

    def rewrite_query(self, question: str, conversation_history: str = "") -> str:
        """
        Rewrite a follow-up question into a standalone question for retrieval.
        If there is no useful prior context, the rewritten question should remain
        close to the original.
        """
        system_prompt = (
            "You rewrite user questions into standalone search queries for a "
            "cardiology reference assistant. "
            "Use conversation history only when needed to resolve follow-up questions. "
            "Return only the rewritten standalone question. "
            "Do not answer the question."
        )

        user_prompt = (
            f"Conversation History:\n{conversation_history or 'No prior conversation.'}\n\n"
            f"User Question:\n{question}\n\n"
            "Rewrite this into a concise standalone question for document retrieval."
        )

        response = self.client.chat.completions.create(
            model=AZURE_OPENAI_CHAT_DEPLOYMENT,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
        )

        rewritten_question = response.choices[0].message.content or question
        return rewritten_question.strip()

    def generate_grounded_answer(
        self,
        question: str,
        chunks: list[dict],
        conversation_history: str = "",
    ) -> str:
        context = "\n\n".join(
            [
                (
                    f"[Source {i + 1}] "
                    f"Document: {chunk['document_name']}, "
                    f"Page: {chunk['page_number']}\n"
                    f"{chunk['chunk_text']}"
                )
                for i, chunk in enumerate(chunks)
            ]
        )

        system_prompt = (
            "You are a cardiology reference assistant. "
            "Answer the user's question using only the provided context. "
            "Use conversation history only to understand follow-up questions. "
            "Do not make up facts. "
            "If the answer is not in the context, say that the information is not available "
            "in the references. "
            "Do not include a References or Sources section."
        )

        user_prompt = (
            f"Conversation History:\n{conversation_history or 'No prior conversation.'}\n\n"
            f"Question:\n{question}\n\n"
            f"Context:\n{context}\n\n"
            "Return only a concise answer."
        )

        response = self.client.chat.completions.create(
            model=AZURE_OPENAI_CHAT_DEPLOYMENT,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
        )

        return response.choices[0].message.content or ""