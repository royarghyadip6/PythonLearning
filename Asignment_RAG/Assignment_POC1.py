"""
Using RAG, Build an e-commerce assistant that provides intelligent recommendations and answers user's queries about the product.
"""


"""
E-commerce RAG assistant (LangChain 1.2.0, Python 3.13)
- Embeddings: Gemini (embedding-001) → fallback to FastEmbed (local, no API quotas)
- Vector store: Chroma (chromadb) → fallback to FAISS
- Loads GEMINI_API_KEY from .env (or GOOGLE_API_KEY), normalizes to GOOGLE_API_KEY
- Verbose prints for embeddings → retrieval → filtering → context → LLM → decision trace
"""

import os
from typing import Optional

# -----------------------------
# 0) Load .env & resolve API key
# -----------------------------
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if api_key:
    # langchain-google-genai expects GOOGLE_API_KEY; normalize
    os.environ["GOOGLE_API_KEY"] = api_key

# -----------------------------
# 1) Imports (LangChain 1.2.0)
# -----------------------------
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

# LLM (Gemini Flash 2.5)
from langchain_google_genai import ChatGoogleGenerativeAI

# Embedding fallbacks
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_google_genai._common import GoogleGenerativeAIError

# Vector store fallbacks
USE_CHROMA = True
try:
    import chromadb  # noqa: F401
    from langchain_community.vectorstores import Chroma
except Exception:
    USE_CHROMA = False
    from langchain_community.vectorstores import FAISS

# -----------------------------
# 2) Helper: choose embeddings
# -----------------------------
def get_embedding_model():
    """
    Try Gemini embeddings first; if quota/rate-limit errors or no key, fallback to FastEmbed.
    We also test a tiny embed call up front to catch quota issues early.
    """
    if os.getenv("GOOGLE_API_KEY"):
        try:
            print("🔌 Trying Gemini embeddings: models/embedding-001")
            gem = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            # Sanity test: small embed to confirm quota
            _ = gem.embed_query("sanity-check")
            print("✅ Gemini embeddings OK\n")
            return gem
        except GoogleGenerativeAIError as e:
            print(f"⚠️ Gemini embeddings failed (likely quota/rate-limit): {e}\n"
                  f"➡️ Falling back to local FastEmbed.")
        except Exception as e:
            print(f"⚠️ Gemini embeddings init error: {e}\n➡️ Falling back to local FastEmbed.")
    else:
        print("ℹ️ No GOOGLE_API_KEY/GEMINI_API_KEY set; using local FastEmbed.\n")

    # Fallback: local, no API calls
    print("🔌 Using FastEmbed (local) — model: BAAI/bge-small-en-v1.5 (default)")
    fast = FastEmbedEmbeddings()  # downloads small model on first run
    print("✅ FastEmbed ready\n")
    return fast

# -----------------------------
# 3) Initialize models
# -----------------------------
embedding_model = get_embedding_model()

# LLM: still using Gemini Flash 2.5; you can also fallback to an open-source LLM if needed.
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

# -----------------------------
# 4) Sample product catalog
# -----------------------------
products = [
    {
        "name": "Nike Air Max",
        "price": 120, "currency": "USD", "category": "Shoes",
        "desc": "Comfortable running shoes with air cushioning. Great for daily runs and casual wear."
    },
    {
        "name": "Apple iPhone 15",
        "price": 999, "currency": "USD", "category": "Smartphone",
        "desc": "Latest iPhone with A17 chip, excellent camera, and long battery life. 6.1-inch display."
    },
    {
        "name": "Sony WH-1000XM5",
        "price": 399, "currency": "USD", "category": "Headphones",
        "desc": "Noise-cancelling wireless headphones with premium sound and comfortable fit for travel/work."
    },
    {
        "name": "Asics Gel-Kayano 30",
        "price": 160, "currency": "USD", "category": "Shoes",
        "desc": "Stability running shoes with gel cushioning and great arch support for long-distance runs."
    },
    {
        "name": "Samsung Galaxy S24",
        "price": 899, "currency": "USD", "category": "Smartphone",
        "desc": "Flagship Android with strong camera, AI features, and smooth 120Hz display."
    },
]

docs = [
    Document(
        page_content=p["desc"],
        metadata={"name": p["name"], "price": p["price"], "currency": p["currency"],
                  "category": p["category"], "desc": p["desc"]},
    )
    for p in products
]

# -----------------------------
# 5) Build vector store
# -----------------------------
print(f"⏳ Building vector store with embeddings... (backend: {'Chroma' if USE_CHROMA else 'FAISS'})")
try:
    if USE_CHROMA:
        # In-memory by default. To persist, add persist_directory="./chroma_store"
        vectorstore = Chroma.from_documents(docs, embedding_model)
    else:
        vectorstore = FAISS.from_documents(docs, embedding_model)
    print("✅ Vector store ready.\n")
except Exception as e:
    # If building still fails (rare), force switch to FAISS
    print(f"⚠️ Vector store build failed: {e}\n➡️ Forcing FAISS fallback.")
    from langchain_community.vectorstores import FAISS
    vectorstore = FAISS.from_documents(docs, embedding_model)
    print("✅ FAISS vector store ready.\n")

# -----------------------------
# 6) Query helper with verbose prints
# -----------------------------
def run_query(user_query: str, k: int = 3, max_price: Optional[float] = None):
    print("=" * 80)
    print(f"USER QUERY: {user_query}")
    if max_price is not None:
        currency = docs[0].metadata.get("currency", "")
        print(f"Budget constraint: ≤ {currency} {max_price}")
    print("-" * 80)

    # 6a) Embed the query (explicit transparency). This uses the vectorstore's embedding function internally too.
    try:
        q_emb = embedding_model.embed_query(user_query)
        print(f"[Embeddings] Query vector length: {len(q_emb)}")
        print(f"[Embeddings] Vector preview (first 8 dims): {q_emb[:8]}\n")
    except Exception as e:
        print(f"⚠️ Query embedding failed: {e}\n(This is unusual with FastEmbed; continuing.)\n")

    # 6b) Retrieve top-k with scores when available
    print("🔎 Retrieving top-k similar products (cosine similarity):")
    try:
        results = vectorstore.similarity_search_with_score(user_query, k=k)
        pairs = results  # list[(Document, score)]
    except AttributeError:
        docs_only = vectorstore.similarity_search(user_query, k=k)
        pairs = [(d, float("nan")) for d in docs_only]  # score not available

    for rank, (doc, score) in enumerate(pairs, start=1):
        m = doc.metadata
        score_str = "N/A" if (score != score) else f"{score:.4f}"  # NaN check
        print(f"  #{rank} | score={score_str} | {m['name']} "
              f"({m['category']}, {m['currency']} {m['price']})")
        print(f"       snippet: {doc.page_content[:110]}...\n")

    # 6c) Apply simple price filter (decision logging)
    filtered = []
    decision_notes = []
    for doc, score in pairs:
        m = doc.metadata
        if max_price is not None and m["price"] > max_price:
            decision_notes.append(f"- EXCLUDED {m['name']} @ {m['currency']} {m['price']} (above budget)")
            continue
        filtered.append((doc, score))
        decision_notes.append(f"+ INCLUDED {m['name']} @ {m['currency']} {m['price']} (within criteria)")

    if max_price is not None:
        print("🧮 Price filter decisions:")
        for note in decision_notes:
            print(" ", note)
        print()

    # 6d) Build concise context for the LLM
    context_lines = []
    for doc, score in filtered[:2]:  # keep context small; top-2 after filtering
        m = doc.metadata
        context_lines.append(
            f"- name: {m['name']} | category: {m['category']} "
            f"| price: {m['currency']} {m['price']} | desc: {m['desc']}"
        )
    context = "\n".join(context_lines) if context_lines else "No products match constraints."

    print("📚 Context passed to the LLM:")
    print(context, "\n")

    # 6e) Prompt the LLM with explicit instructions
    prompt_tmpl = PromptTemplate.from_template(
        "You are an e-commerce assistant. Use ONLY the products from CONTEXT to answer.\n"
        "If no products are suitable, say so and suggest the closest alternative.\n"
        "Explain briefly WHY the recommendation fits the user's intent (price, features, category).\n\n"
        "USER: {query}\n"
        "CONTEXT:\n{context}\n\n"
        "Return a short, helpful answer with 1–2 recommendations max."
    )
    prompt = prompt_tmpl.format(query=user_query, context=context)
    print("🧾 Final prompt to LLM:\n")
    print(prompt)
    print()

    # 6f) LLM answer (catch rate limits gracefully)
    try:
        response = llm.invoke(prompt)
        print("🧠 LLM ANSWER:")
        print(response.content)
        print()
    except Exception as e:
        print(f"⚠️ LLM call failed (possibly rate limit): {e}")
        print("➡️ Tip: retry after ~60s or reduce request rate.\n")
        return

    # 6g) Decision trace summary (why these items?)
    print("🧭 DECISION TRACE (why selected):")
    if not filtered:
        print("- No items passed filters; LLM asked to propose closest alternative.")
    else:
        for doc, score in filtered[:2]:
            m = doc.metadata
            reasons = []
            if "run" in m["desc"].lower() or m["category"].lower() == "shoes":
                reasons.append("matches running intent/category")
            if "camera" in m["desc"].lower():
                reasons.append("strong camera feature")
            if "noise-cancelling" in m["desc"].lower():
                reasons.append("noise-cancelling feature")
            if max_price is not None and m["price"] <= max_price:
                reasons.append(f"within budget (≤ {max_price})")
            if not reasons:
                reasons.append("high semantic similarity to query")
            score_str = "N/A" if (score != score) else f"{score:.4f}"
            print(f"- {m['name']} (score={score_str}) → " + ", ".join(reasons))
    print("=" * 80 + "\n")


# -----------------------------
# 7) Try a couple of queries
# -----------------------------
if __name__ == "__main__":
    run_query("Suggest a good smartphone under $950", k=3, max_price=950)
    run_query("I need comfortable shoes for daily running", k=3)
