# Resonsible for load different file types and chunking them
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader


def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
        
    return text

def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return text

def load_and_chunk(file_path):
    if file_path.endswith(".pdf"):
        text = load_pdf(file_path)
    elif file_path.endswith(".txt"):
        text = load_text(file_path)
    else:
        raise ValueError("Unsupported file type. Please upload a .pdf or .txt file.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    
    return chunks