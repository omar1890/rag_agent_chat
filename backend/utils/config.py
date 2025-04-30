from dotenv import load_dotenv
import os

load_dotenv(override=True)

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploaded_docs")
VECTOR_DB_DIR = os.getenv("VECTOR_DB_DIR", "vector_db")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")