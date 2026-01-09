from document_loader import load_and_split_documents
from vector_store import create_vector_store

docs = load_and_split_documents("data.pdf")
create_vector_store(docs)

print("FAISS index created successfully")
