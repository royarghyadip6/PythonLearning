import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "llama3-70b-8192"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

FAISS_INDEX_PATH = "faiss_index"
