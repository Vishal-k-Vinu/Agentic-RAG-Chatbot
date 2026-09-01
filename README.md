# Agentic RAG Chatbot

A production-grade Retrieval-Augmented Generation (RAG) chatbot designed to act as a medical knowledge assistant. The application leverages a local Large Language Model (LLM) equipped with tool-calling capabilities to intelligently decide when to retrieve information from a curated medical knowledge base.

## Architecture

The system is composed of several decoupled components:

- **Frontend**: A Streamlit-based web interface for user interaction.
- **Backend API**: A FastAPI service exposing the chat endpoint.
- **Agent System**: A Python-based routing agent powered by Ollama (using Llama 3.2 1B). It determines if a user query requires medical domain knowledge and executes tool calls accordingly.
- **Vector Database**: A local ChromaDB instance used to index and retrieve chunked medical text data for accurate context injection.

## Project Structure

```
.
├── backend/
│   ├── main.py                 # FastAPI application and endpoint definitions
│   ├── agent.py                # LLM agent logic and tool-calling configuration
│   ├── retriever.py            # ChromaDB initialization, document chunking, and search
│   └── document/
│       └── medical_knowledge_base.txt  # Source knowledge text for the vector database
├── frontend/
│   └── app.py                  # Streamlit chat interface
├── requirements.txt            # Python dependencies
└── .gitignore                  # Git ignore rules for virtual environments and databases
```

## Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com/) installed and running locally
- Llama 3.2 1B model pulled in Ollama (`ollama run llama3.2:1b`)

## Installation

1. Clone the repository and navigate to the project root.
2. Create and activate a virtual environment (e.g., using Conda or venv).
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Setup and Initialization

Before running the application, you must initialize the vector database by parsing and embedding the medical knowledge base.

```bash
cd backend
python retriever.py
cd ..
```
This script will chunk the text document, generate embeddings, and store them persistently in a local `chroma_db` directory.

## Running the Application

The application requires both the backend API and the frontend UI to be running simultaneously.

### 1. Start the Backend (FastAPI)

In your terminal, run the FastAPI server using Uvicorn:

```bash
uvicorn backend.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### 2. Start the Frontend (Streamlit)

Open a new terminal session, activate your environment, and start the Streamlit application:

```bash
streamlit run frontend/app.py
```
The UI will automatically open in your default web browser (typically at `http://localhost:8501`).

## Usage

Interact with the chatbot through the Streamlit interface. 
- If you ask a medical-related question (e.g., "What are the symptoms of asthma?"), the agent will autonomously trigger the search tool, retrieve relevant context from ChromaDB, and formulate a response based strictly on that data.
- If you ask a non-medical question or send a simple greeting, the agent will bypass the retrieval tool and respond appropriately based on its system instructions.


