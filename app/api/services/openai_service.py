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

    def generate_grounded_answer(self, question: str, chunks: list[dict]) -> str:
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
            "You are a clinical document assistant. "
            "Answer the user's question using only the provided context. "
            "Do not make up facts. "
            "If the answer is not in the context, say that the information is not available "
            "in the uploaded documents. "
            "Cite the supporting sources using the Source numbers."
        )

        user_prompt = (
            f"Question:\n{question}\n\n"
            f"Context:\n{context}\n\n"
            "Return a concise answer followed by a short Sources section."
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