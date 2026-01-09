from langchain_groq import ChatGroq
from langchain.chains.retrieval_qa.base import RetrievalQA
from vector_store import load_vector_store
from config import LLM_MODEL

def get_rag_chain():
    llm = ChatGroq(
        model=LLM_MODEL,
        temperature=0.2
    )

    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True
    )

    return qa_chain
