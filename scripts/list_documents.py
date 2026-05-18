from app.api.services.search_service import SearchService


def main():
    search_service = SearchService()

    results = search_service.search_client.search(
        search_text="*",
        select=["document_name"],
        top=5000,
    )

    documents = set()

    for result in results:
        documents.add(result["document_name"])

    print("\nDocuments in Azure AI Search:\n")

    for document in sorted(documents):
        print(f"- {document}")


if __name__ == "__main__":
    main()