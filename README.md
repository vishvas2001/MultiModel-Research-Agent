# Multimodel Research Agent

A sophisticated research agent that combines multiple models and data sources to provide comprehensive answers with source verification and web search capabilities.

## Features

- **Multi-source Research**: Leverages PDF documents and web search for comprehensive information gathering
- **LLM-powered Pipeline**: Uses Ollama models for intelligent routing, retrieval, and response generation
- **RAG (Retrieval-Augmented Generation)**: FAISS-based vector store for efficient document retrieval
- **Critic Evaluation**: Built-in verification layer to evaluate response quality and accuracy
- **Streaming API**: Real-time event streaming for progressive response generation
- **Web Search Integration**: DuckDuckGo integration for current web information
- **Streamlit UI**: User-friendly interface for interacting with the agent

## Project Structure

```
├── api/                    # FastAPI server
│   └── main.py            # Main API application
├── app/
│   ├── graph/             # LangGraph workflow orchestration
│   │   ├── builder.py     # Graph construction
│   │   └── state.py       # State management
│   ├── llm/               # Language model configuration
│   │   ├── model.py       # Ollama LLM setup
│   │   └── prompts.py     # Prompts for different nodes
│   ├── nodes/             # Workflow nodes
│   │   ├── router.py      # Query routing logic
│   │   ├── pdf_node.py    # PDF retrieval
│   │   ├── web_node.py    # Web search
│   │   ├── critic.py      # Response evaluation
│   │   └── responder.py   # Final response generation
│   ├── rag/               # Retrieval-Augmented Generation
│   │   ├── ingest.py      # PDF processing pipeline
│   │   ├── retriever.py   # Document retrieval
│   │   └── vectorstore.py # FAISS vector store management
│   ├── tools/             # Utility tools
│   │   └── web_search.py  # DuckDuckGo search wrapper
│   └── utils/
│       └── logger.py      # Logging configuration
├── ui/                    # Streamlit frontend
│   └── app.py            # UI application
├── test/                  # Test suite
│   ├── test_graph.py     # Graph tests
│   └── test_rag.py       # RAG tests
└── data/
    ├── pdfs/             # Storage for PDF documents
    └── faiss_index/      # FAISS vector store
```

## Requirements

- Python 3.10+
- Ollama (for running LLMs locally)

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd "Multimodel Research Agent"
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Create .env file with your configuration
cp .env.example .env  # if available
```

## Setup

### Ollama Setup
1. Install [Ollama](https://ollama.ai)
2. Pull required models:
```bash
ollama pull gemma4:e4b       # For query understanding and response
ollama pull qwen3-embedding:8b  # For embeddings
```

### Prepare Data
1. Add PDF files to `data/pdfs/` directory
2. The system will automatically process and index them on first run

## Usage

### Start the FastAPI Server
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API endpoints:
- `POST /stream` - Stream research results for a query

### Launch the Streamlit UI
```bash
streamlit run ui/app.py
```

The UI will be available at `http://localhost:8501`

### Query the Agent
```python
import requests
import json

response = requests.post(
    "http://localhost:8000/stream",
    json={"query": "Your research question", "session_id": "unique_id"}
)
```

## Running Tests

```bash
pytest test/
pytest test/test_rag.py -v
pytest test/test_graph.py -v
```

## API Response Format

Streaming responses are sent as Server-Sent Events (SSE) with the following formats:

```json
{"type": "log", "content": "⚙️ Entering node: ROUTER"}
{"type": "token", "content": "streamed response text..."}
{"type": "log", "content": "⚖️ Critic Evaluation: ..."}
```

## Configuration

Key configuration files:
- `app/llm/prompts.py` - Customize prompts for different nodes
- `app/rag/ingest.py` - Adjust document splitting parameters
- `app/graph/state.py` - Define workflow state schema

## Troubleshooting

- **Ollama not responding**: Ensure Ollama service is running (`ollama serve`)
- **No FAISS index**: Place PDFs in `data/pdfs/` and restart the application
- **CUDA/GPU issues**: The project uses `faiss-cpu`; for GPU support, install `faiss-gpu`


---

Give a Star if you found this project helpful.⭐
