import json
import asyncio # New import required
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import shutil
import os

from app.graph.builder import build_graph
from app.rag.ingest import process_pdf_to_chunks
from app.rag.vectorstore import incremental_update_faiss

compiled_graph = build_graph()

app = FastAPI(title="Private-Pulse API")

class QueryRequest(BaseModel):
    query: str
    session_id: str

async def graph_event_generator(query: str):
    inputs = {"query": query}
    
    try:
        async for event in compiled_graph.astream_events(inputs, version="v2"):
            kind = event["event"]
            
            if kind == "on_chain_start":
                node_name = event.get("name", "")
                if node_name in ["router", "pdf", "web", "critic", "responder"]:
                    payload = {"type": "log", "content": f"⚙️ Entering node: {node_name.upper()}"}
                    yield f"data: {json.dumps(payload)}\n\n"
            
            elif kind == "on_chat_model_stream":
                chunk = event.get("data", {}).get("chunk")
                if chunk and chunk.content:
                    payload = {"type": "token", "content": chunk.content}
                    yield f"data: {json.dumps(payload)}\n\n"
                    
            elif kind == "on_chain_end" and event.get("name") == "critic":
                output = event.get("data", {}).get("output", {})
                payload = {"type": "log", "content": f"⚖️ Critic Evaluation: {output}"}
                yield f"data: {json.dumps(payload)}\n\n"

            elif kind == "on_chain_end" and event.get("name") == "responder":
                output = event.get("data", {}).get("output", {})
                if "answer" in output and output["answer"]:
                    payload = {"type": "token", "content": "\n\n" + output["answer"]}
                    yield f"data: {json.dumps(payload)}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    # --- NEW: Catch the disconnect signal ---
    except asyncio.CancelledError:
        print("\n🚫 [API] Stream cancelled by user. Terminating LangGraph execution.\n")
        # Reraise the error so FastAPI knows to cleanly close the HTTP stream
        raise 
        
    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

@app.post("/api/chat/stream")
async def chat_stream(request: QueryRequest):
    return StreamingResponse(
        graph_event_generator(request.query), 
        media_type="text/event-stream"
    )

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    os.makedirs("data/pdfs", exist_ok=True)
    file_path = f"data/pdfs/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    chunks = process_pdf_to_chunks(file_path)
    incremental_update_faiss(chunks)
    
    return {"status": "success", "message": f"Successfully indexed {file.filename}"}