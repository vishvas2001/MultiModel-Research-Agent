import os
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from app.rag.ingest import ingest_pdfs

# Dynamically find the project root to guarantee path accuracy
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

# Use absolute paths
INDEX_PATH = os.path.join(PROJECT_ROOT, "data", "faiss_index")
INDEX_FILE = os.path.join(INDEX_PATH, "index.faiss")
PDF_PATH = os.path.join(PROJECT_ROOT, "data", "pdfs")


def get_embedding_model():
    """
    Load embedding model
    """
    return OllamaEmbeddings(
        model="qwen3-embedding:8b"
    )


def create_vectorstore(chunks):
    """
    Create FAISS index from document chunks
    """
    print("[VectorStore] Creating embeddings...")

    embedding_model = get_embedding_model()

    vectorstore = FAISS.from_documents(
        chunks,
        embedding_model
    )

    print("[VectorStore] FAISS index created")

    return vectorstore


def save_vectorstore(vectorstore, path=INDEX_PATH):
    """
    Save FAISS index locally
    """
    vectorstore.save_local(path)
    print(f"[VectorStore] Saved at {path}")


def load_vectorstore():
    embedding_model = get_embedding_model()

    # Fix: Check for the actual file, not just the directory
    if not os.path.exists(INDEX_FILE):
        print("[VectorStore] Index file not found → rebuilding...")

        # Fix: Use the absolute path for the PDFs as well
        chunks = ingest_pdfs(PDF_PATH) 
        vectorstore = FAISS.from_documents(chunks, embedding_model)
        vectorstore.save_local(INDEX_PATH)

        print("[VectorStore] Rebuilt and saved")

        return vectorstore

    # Otherwise load normally
    print("[VectorStore] Loading from disk")

    return FAISS.load_local(
        INDEX_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )

# --- NEW FUNCTION FOR FASTAPI UPLOADS ---
def incremental_update_faiss(new_chunks):
    """
    Adds new documents to an existing FAISS index without full rebuild.
    """
    embedding_model = get_embedding_model()
    
    # Create a temporary index with just the new chunks
    new_db = FAISS.from_documents(new_chunks, embedding_model)
    
    if os.path.exists(INDEX_FILE):
        # Load existing and merge
        existing_db = FAISS.load_local(INDEX_PATH, embedding_model, allow_dangerous_deserialization=True)
        existing_db.merge_from(new_db)
        existing_db.save_local(INDEX_PATH)
        print("[RAG] Vectorstore updated incrementally with new documents.")
    else:
        # First time setup if the index somehow didn't exist
        new_db.save_local(INDEX_PATH)
        print("[RAG] New Vectorstore created from uploaded document.")