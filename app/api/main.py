from fastapi import FastAPI
from app.api.routes import health, documents, questions

app = FastAPI(
    title="AI Clinical Document Assistant",
    description="RAG platform for querying clinical documents",
    version="0.1.0"
)

app.include_router(health.router)
app.include_router(documents.router)
app.include_router(questions.router)