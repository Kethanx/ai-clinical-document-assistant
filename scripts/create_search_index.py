from app.api.services.search_service import SearchService


if __name__ == "__main__":
    service = SearchService()
    service.create_index_if_not_exists()