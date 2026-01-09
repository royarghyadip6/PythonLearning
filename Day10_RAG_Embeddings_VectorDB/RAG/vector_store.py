from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from config import EMBEDDING_MODEL, FAISS_INDEX_PATH
import os

def create_vector_store(documents):
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(FAISS_INDEX_PATH)
    return vectorstore


def load_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError("FAISS index not found")
    return FAISS.load_local(FAISS_INDEX_PATH, embeddings)
