import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_pdfs(pdf_dir: str):
    """
    Load all PDFs from a directory
    """
    documents = []

    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            path = os.path.join(pdf_dir, file)
            loader = PyPDFLoader(path)
            docs = loader.load()
            documents.extend(docs)

    return documents


def split_documents(documents):
    """
    Split documents into smaller chunks
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)
    return chunks


def ingest_pdfs(pdf_dir: str):
    """
    Full ingestion pipeline for a directory
    """
    print("[Ingest] Loading PDFs...")
    documents = load_pdfs(pdf_dir)

    print(f"[Ingest] Loaded {len(documents)} pages")

    print("[Ingest] Splitting into chunks...")
    chunks = split_documents(documents)

    print(f"[Ingest] Created {len(chunks)} chunks")

    return chunks


def process_pdf_to_chunks(file_path: str):
    """
    Ingest and chunk a single uploaded PDF file
    """
    print(f"[Ingest] Loading single PDF: {file_path}")
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    print(f"[Ingest] Splitting {len(documents)} pages into chunks...")
    chunks = split_documents(documents)
    
    print(f"[Ingest] Created {len(chunks)} chunks from uploaded file")
    return chunks