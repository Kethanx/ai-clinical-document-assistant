from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SearchableField,
    SimpleField,
    VectorSearch,
    VectorSearchProfile,
)
from azure.search.documents.models import VectorizedQuery

from app.api.core.config import (
    AZURE_SEARCH_API_KEY,
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_INDEX_NAME,
    AZURE_OPENAI_EMBEDDING_DIMENSIONS,
)


class SearchService:
    def __init__(self) -> None:
        if not AZURE_SEARCH_ENDPOINT:
            raise ValueError("AZURE_SEARCH_ENDPOINT is not set")
        if not AZURE_SEARCH_API_KEY:
            raise ValueError("AZURE_SEARCH_API_KEY is not set")

        credential = AzureKeyCredential(AZURE_SEARCH_API_KEY)

        self.index_client = SearchIndexClient(
            endpoint=AZURE_SEARCH_ENDPOINT,
            credential=credential,
        )

        self.search_client = SearchClient(
            endpoint=AZURE_SEARCH_ENDPOINT,
            index_name=AZURE_SEARCH_INDEX_NAME,
            credential=credential,
        )

    def create_index_if_not_exists(self) -> None:
        existing_indexes = [idx.name for idx in self.index_client.list_indexes()]
        if AZURE_SEARCH_INDEX_NAME in existing_indexes:
            print(f"Index '{AZURE_SEARCH_INDEX_NAME}' already exists.")
            return

        fields = [
            SimpleField(name="chunk_id", type=SearchFieldDataType.String, key=True),
            SimpleField(name="document_id", type=SearchFieldDataType.String, filterable=True),
            SearchableField(name="document_name", type=SearchFieldDataType.String, filterable=True),
            SimpleField(name="page_number", type=SearchFieldDataType.Int32, filterable=True, sortable=True),
            SearchableField(name="chunk_text", type=SearchFieldDataType.String),
            SearchField(
                name="embedding",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=AZURE_OPENAI_EMBEDDING_DIMENSIONS,
                vector_search_profile_name="default-vector-profile",
            ),
        ]

        vector_search = VectorSearch(
            profiles=[
                VectorSearchProfile(
                    name="default-vector-profile",
                    algorithm_configuration_name="default-hnsw",
                )
            ],
            algorithms=[
                HnswAlgorithmConfiguration(
                    name="default-hnsw",
                )
            ],
        )

        index = SearchIndex(
            name=AZURE_SEARCH_INDEX_NAME,
            fields=fields,
            vector_search=vector_search,
        )

        self.index_client.create_index(index)
        print(f"Created index '{AZURE_SEARCH_INDEX_NAME}'.")

    def upload_chunks(self, chunks: list[dict]) -> None:
        if not chunks:
            print("No chunks to upload.")
            return

        result = self.search_client.upload_documents(documents=chunks)
        succeeded = sum(1 for item in result if item.succeeded)
        print(f"Uploaded {succeeded}/{len(chunks)} chunks to Azure AI Search.")

    def vector_search(self, embedding: list[float], top_k: int = 5) -> list[dict]:
        vector_query = VectorizedQuery(
            vector=embedding,
            k_nearest_neighbors=top_k,
            fields="embedding",
        )

        results = self.search_client.search(
            search_text=None,
            vector_queries=[vector_query],
            select=["chunk_id", "document_id", "document_name", "page_number", "chunk_text"],
            top=top_k,
        )

        chunks = []
        for result in results:
            chunks.append(
                {
                    "chunk_id": result["chunk_id"],
                    "document_id": result["document_id"],
                    "document_name": result["document_name"],
                    "page_number": result["page_number"],
                    "chunk_text": result["chunk_text"],
                }
            )

        return chunks