from fastapi import FastAPI
from pydantic import BaseModel
from rag_chain import get_rag_chain

app = FastAPI(title="Groq RAG API")

qa_chain = get_rag_chain()

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QueryRequest):
    response = qa_chain(request.question)
    return {
        "answer": response["result"]
    }
