🧠 Generative AI Math Assistant (RAG-Based App)

🚀 Overview

This project is an AI-powered math question-answering system built using Retrieval-Augmented Generation (RAG).
It combines FastAPI, Qdrant Vector Database, and Open Source LLMs to create an intelligent agent that can solve mathematical queries, learn from feedback, and improve over time.

Developed as part of my AI Engineer assignment for AI Planet, this project demonstrates my practical skills in:

Generative AI

Prompt engineering

Vector databases

Backend + Frontend integration



---

🧩 Project Structure

RAG_APP/
│
├── backend/
│   ├── main.py                # FastAPI backend
│   ├── ingest.py              # Script to ingest KB into Qdrant
│   ├── vectorstore.py         # Handles embeddings + search
│   ├── embed_model.py         # Embedding model logic
│   ├── requirements.txt       # Backend dependencies
│   └── math_kb.json           # Sample knowledge base (math problems)
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/                   # React/Vite frontend files
│
└── README.md


---

⚙ Tech Stack

🧭 Backend

FastAPI (Python)

Qdrant (Vector Database for semantic search)

SentenceTransformers (all-MiniLM-L6-v2) for embeddings

MPT-7B-Instruct (open-source LLM)

Docker (for running Qdrant)


💻 Frontend

Vite + React

Axios for backend communication

Tailwind CSS for minimal styling



---

🧪 Setup & Run Instructions

1️⃣ Start Qdrant Vector DB (Docker)

docker run -d --name qdrant -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant

2️⃣ Setup Backend

cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

3️⃣ Ingest Knowledge Base

python ingest.py

✅ You should see a log like Ingested X items into Qdrant.

4️⃣ Start Backend Server

uvicorn main:app --reload --port 8000

Access API Docs here 👉 http://localhost:8000/docs

5️⃣ Setup Frontend

cd ../frontend
npm install
npm run start

Open UI at 👉 http://localhost:5173


---

🧠 Key Features

✅ RAG Pipeline for math question answering
✅ Dynamic knowledge ingestion (math_kb.json)
✅ Feedback system to learn new Q&A pairs
✅ REST API with /ask and /feedback endpoints
✅ Interactive web interface
✅ Open-source models only — no paid APIs


---

📊 Demo Workflow

1. Ask: “Solve 2x + 3 = 7”


2. Model fetches relevant context from Qdrant


3. LLM generates structured solution


4. If not found, fallback message is shown


5. User can add correct answer using /feedback


6. Re-run /ask → retrieves updated answer




---

⚡ Troubleshooting

If you see:

> ❌ “Collection math_kb doesn’t exist!”



Run:

python ingest.py

If frontend shows:

> ⚠ “Network Error”



Make sure:

Backend (http://localhost:8000) is running

CORS is enabled in main.py



---

🧑‍💻 About the Developer

Murali Krishna K.
🎓 B.Tech, Electronics & Computer Engineering
🏫 Sreenidhi Institute of Science and Technology
💡 Interests: Generative AI, LLMs, AI Applications in EdTech


---

🏁 Future Enhancements

Auto-updating KB from feedback

Support for image-based math (OCR + LLM)

Model fine-tuning for step-wise reasoning
