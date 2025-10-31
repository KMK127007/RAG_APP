# main.py
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Optional, List
from embed_model import Embedder
from vectorstore import QdrantStore
from llm import LLMWrapper
from settings import TOP_K, ALLOWED_TOPICS, SERPAPI_KEY
import re, requests, uuid

app = FastAPI(title="Math Routing Agent (RAG) - OpenSource models")

# init (lazy)
embed = Embedder()
store = QdrantStore()
llm = LLMWrapper()

# Simple guardrail functions
def input_guardrail(text: str) -> bool:
    # only allow math-related content roughly: check keywords or math tokens
    t = text.lower()
    # allow if math keywords present OR characters that indicate math
    math_tokens = ["solve","integrate","differentiate","derivative","integral","limit","sum","compute","prove","matrix","determinant","eigen","sin(","cos(","tan(","log(","∑","+","-", "*","/","^","x","y"]
    if any(tok in t for tok in math_tokens):
        return True
    # also allow if topic mentioned
    if any(topic in t for topic in ALLOWED_TOPICS):
        return True
    return False

def output_guardrail(text: str) -> bool:
    # Basic safety check: ensure no hallucinated non-math claims like medical/legal/personal
    forbidden = ["diagnose", "legal advice", "prescribe", "bank account", "password", "social security", "credit card"]
    if any(f in text.lower() for f in forbidden):
        return False
    return True

class AskRequest(BaseModel):
    question: str
    user_id: Optional[str] = None

class FeedbackRequest(BaseModel):
    question: str
    correct_answer: Optional[str] = None
    comment: Optional[str] = None
    user_id: Optional[str] = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: AskRequest):
    q = req.question.strip()
    # guardrails
    if not input_guardrail(q):
        raise HTTPException(status_code=400, detail="Query rejected by input guardrails: make sure it's a math/educational question.")

    # embed question
    vec = embed.encode(q)[0]
    # search in KB
    results = store.search(vec, top_k=TOP_K)
    # If high-similarity result found, return step-by-step
    if results and results[0][1] < 0.35:  # score: smaller is closer for cosine in Qdrant sometimes; adjust threshold as needed
        payload, score = results[0]
        # generate a professor-like step-by-step using steps as context
        context = payload.get("steps") or payload.get("answer")
        prompt = f"You are a helpful mathematics professor. Use the context to create a clear step-by-step solution for the following student question:\n\nStudent question: {q}\nContext: {context}\n\nProvide step-by-step explanation and final answer."
        out = llm.generate(prompt)
        if not output_guardrail(out):
            raise HTTPException(status_code=400, detail="Response blocked by output guardrails.")
        return {"source": "knowledge_base", "kb_match": payload, "answer": out}

    # else: fallback web search (SerpAPI example) or MCP web extraction pipeline
    web_text = web_search_extract(q)
    if web_text:
        prompt = f"You are a math professor. Use the web-extracted text to craft step-by-step solution for the question:\n\nQuestion: {q}\nWeb extraction: {web_text}\nProvide step-by-step solution and final answer."
        out = llm.generate(prompt)
        if not output_guardrail(out):
            raise HTTPException(status_code=400, detail="Response blocked by output guardrails.")
        return {"source": "web_search", "web_snippet": web_text, "answer": out}

    # If nothing found, politely say can't answer and ask for human feedback
    return {"source": "no_result", "answer": "I couldn't find a reliable source for this question. Please provide more context or wait for a human review."}

def web_search_extract(query):
    # Example using SerpAPI (replace with your preferred search)
    if not SERPAPI_KEY:
        return None
    try:
        params = {"engine": "google", "q": query, "api_key": SERPAPI_KEY, "num": 3}
        r = requests.get("https://serpapi.com/search", params=params, timeout=6)
        data = r.json()
        snippets = []
        for item in data.get("organic_results", [])[:3]:
            title = item.get("title")
            snippet = item.get("snippet") or item.get("rich_snippet", {}).get("top", "")
            url = item.get("link", "")
            snippets.append(f"{title}\n{snippet}\n{url}")
        return "\n\n".join(snippets[:3])
    except Exception:
        return None

@app.post("/feedback")
def feedback(fb: FeedbackRequest):
    # store the corrected Q/A in the KB for reindexing
    payload = {
        "question": fb.question,
        "answer": fb.correct_answer or "",
        "steps": fb.comment or ""
    }
    # compute vector and upsert
    vec = embed.encode(fb.question)[0]
    new_id = str(uuid.uuid4())
    store.upsert_items([new_id], [vec], [payload])
    return {"status":"ok", "message":"Feedback recorded and indexed into KB."}

@app.post("/ingest")
def ingest_manual(items: List[dict] = Body(...)):
    # Bulk ingest items = list of {"question","answer","steps"}
    texts = [it["question"] + " ||| " + it.get("answer","") for it in items]
    vecs = embed.encode(texts)
    ids = [it.get("id", str(uuid.uuid4())) for it in items]
    payloads = [{"question": it["question"], "answer": it.get("answer",""), "steps": it.get("steps","")} for it in items]
    store.create_collection(vector_size=vecs.shape[1])
    store.upsert_items(ids, vecs, payloads)
    return {"status":"ok", "ingested": len(items)}
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
