# tools/rag_tool.py
from langchain.tools import Tool
from utils.vector_store import retrieve_similar_docs

def rag_retrieve(question):
    docs = retrieve_similar_docs(question)
    return "\n".join(docs)

def get_rag_tool():
    return Tool(
        name="RAGRetriever",
        description="Use this tool to fetch relevant context from uploaded documents based on the user's question.",
        func=rag_retrieve
    )
