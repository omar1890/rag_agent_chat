from utils.config import UPLOAD_DIR
from utils.document_loader import load_and_chunk
from utils.vector_store import store_chunks, get_all_documents
from fastapi import FastAPI, File, UploadFile, Form
from tools.calculator_tool import get_calculator_tool
from tools.rag_tool import get_rag_tool
from agent import initialize_chat_agent
from langchain.schema import AgentAction
from fastapi.middleware.cors import CORSMiddleware

import shutil
import os

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    chunks = load_and_chunk(file_path)
    store_chunks(chunks)

    all_docs = get_all_documents()

    return {
        "status": "Upload complete.",
        "saved_chunks": len(chunks),
        "total_documents": len(all_docs),
        "documents": all_docs  
    }


@app.post("/chat")
async def chat(question: str = Form(...)):
    tools = [get_calculator_tool(), get_rag_tool()]
    agent = initialize_chat_agent(tools)
    result = agent(question)

    response = result["output"]
    steps = result.get("intermediate_steps", [])

    reasoning = []
    used_inputs = set()
    fallback = False

    for step in steps:
        action, observation = step
        input_key = (action.tool, action.tool_input.strip().lower())

        if input_key in used_inputs:
            continue  # skip duplicate tool calls
        used_inputs.add(input_key)

        reasoning.append({
            "thought": action.log.strip(),
            "tool": action.tool,
            "tool_input": action.tool_input,
            "observation": observation
        })

    # Fallback trigger conditions
    if len(steps) >= 15 or any("error" in str(obs).lower() for _, obs in steps):
        response = "❌ Sorry, I wasn't able to solve that equation accurately. Try rephrasing or simplifying it."
        fallback = True

    return {
        "answer": response,
        "reasoning": reasoning,
        "fallback": fallback
    }