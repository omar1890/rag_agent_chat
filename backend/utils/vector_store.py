# utils/vector_store.py
from chromadb import PersistentClient
from langchain.embeddings import HuggingFaceEmbeddings
from utils.config import VECTOR_DB_DIR, EMBEDDING_MODEL
import uuid

client = PersistentClient(path=VECTOR_DB_DIR)
collection = client.get_or_create_collection(name="documents")

embedder = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def get_all_documents():
    result = collection.get(include=["documents"])
    return result.get("documents", [])

def store_chunks(chunks):
    session_id = str(uuid.uuid4())  # unique per upload
    embeddings = embedder.embed_documents(chunks)
    ids = [f"{session_id}_chunk_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)

def retrieve_similar_docs(query, k=3):
    embedding = embedder.embed_query(query)
    results = collection.query(
        query_embeddings=[embedding],
        n_results=k,
        include=["documents"]
    )
    print(results['documents'][0])
    return results['documents'][0] if results['documents'] else []
