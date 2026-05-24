# Cardiology Assistant

Cardiology Assistant is a cloud-native Retrieval-Augmented Generation (RAG) application that allows users to ask natural language questions over curated cardiology references, including clinical guidelines for atrial fibrillation, heart failure, and hypertension.

The system combines document ingestion, vector search, Azure OpenAI embeddings, and grounded answer generation with citations. It is designed as a portfolio project to demonstrate cloud engineering, AI system design, backend development, containerization, Kubernetes deployment, and CI/CD on Azure.

---

## Project Overview

This project implements a cardiology-focused AI assistant that can answer questions from uploaded clinical reference PDFs.

Users can ask questions such as:

- What is atrial fibrillation?
- What are the stages of heart failure?
- What are the risk factors for high blood pressure?
- What are treatment options for atrial fibrillation?

The assistant retrieves relevant chunks from indexed cardiology documents, sends the retrieved context to an Azure OpenAI chat model, and returns a grounded answer with reference citations.

---

## Key Features

- Upload and store clinical reference PDFs in Azure Blob Storage
- Queue uploaded documents for asynchronous processing
- Extract text from PDFs
- Chunk documents into page-aware sections
- Generate embeddings using Azure OpenAI
- Store vectors and metadata in Azure AI Search
- Perform hybrid retrieval using keyword search and vector search
- Generate grounded answers using Azure OpenAI
- Return structured references with title, authors, publication date, and pages
- Support multi-turn conversation memory
- Rewrite follow-up questions into standalone retrieval queries
- Provide a Streamlit frontend for interactive chat
- Containerize API, worker, and frontend services with Docker
- Deploy services to Azure Kubernetes Service
- Automate Docker image build, push, and AKS deployment using GitHub Actions

---

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

### AI / Retrieval

- Azure OpenAI
- Azure AI Search
- Vector embeddings
- Hybrid search
- Retrieval-Augmented Generation

### Document Processing

- PyPDF
- Custom page-aware chunking
- Azure Blob Storage
- Azure Queue Storage

### Frontend

- Streamlit

### Cloud / DevOps

- Docker
- Docker Compose
- Azure Container Registry
- Azure Kubernetes Service
- Kubernetes manifests
- GitHub Actions CI/CD

---

## High-Level Architecture

```text
User
 │
 ▼
Streamlit Frontend
 │
 ▼
FastAPI Backend
 │
 ├── Question Answering Flow
 │   ├── Rewrite follow-up question
 │   ├── Generate question embedding
 │   ├── Perform hybrid search in Azure AI Search
 │   ├── Retrieve relevant cardiology chunks
 │   └── Generate grounded answer with Azure OpenAI
 │
 └── Document Upload Flow
     ├── Upload PDF to Azure Blob Storage
     ├── Send message to Azure Queue Storage
     └── Worker processes queued document
           ├── Download PDF
           ├── Extract page-aware text
           ├── Chunk content
           ├── Generate embeddings
           └── Index chunks in Azure AI Search
```
