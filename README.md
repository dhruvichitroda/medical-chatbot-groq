# 🏥 Medical Chatbot — Powered by Groq + Llama 3.1 (FREE)

> RAG-based medical chatbot using LangChain, Pinecone, Flask, and Groq (open source LLM — no OpenAI needed!)

---

## 🔧 Tech Stack

| Component | Technology | Cost |
|---|---|---|
| LLM | Llama 3.1 8B via Groq | ✅ FREE |
| Embeddings | all-MiniLM-L6-v2 (HuggingFace) | ✅ FREE |
| Vector DB | Pinecone (Serverless) | ✅ Free tier |
| Web Framework | Flask | ✅ FREE |
| Deployment | AWS EC2 + ECR | 💲 AWS costs |

---

## 🚀 Setup Instructions

### Step 1 — Clone the repo
```bash
git clone <your-repo-url>
cd medical-chatbot-groq
```

### Step 2 — Create conda environment
```bash
conda create -n medibot python=3.10 -y
conda activate medibot
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Get your FREE API keys

**Groq API Key (FREE):**
1. Go to https://console.groq.com
2. Sign up / Log in
3. Go to API Keys → Create API Key
4. Copy the key

**Pinecone API Key (Free tier):**
1. Go to https://app.pinecone.io
2. Sign up / Log in
3. Go to API Keys → Copy default key

### Step 5 — Create .env file
```bash
cp .env.example .env
```
Edit `.env`:
```
PINECONE_API_KEY=your_pinecone_key_here
GROQ_API_KEY=your_groq_key_here
```

### Step 6 — Add your PDF files
```bash
# Place your medical PDF books inside:
data/Medical_book.pdf
```

### Step 7 — Build the knowledge base (run ONCE)
```bash
python store_index.py
```

### Step 8 — Run the app
```bash
python app.py
```

### Step 9 — Open the chatbot
```
http://localhost:8080
```

---

## 🔄 Switching Groq Models

In `app.py`, change the model name:

```python
# Fastest (default)
chatModel = ChatGroq(model="llama-3.1-8b-instant", ...)

# Best quality
chatModel = ChatGroq(model="llama-3.3-70b-versatile", ...)

# Large context
chatModel = ChatGroq(model="mixtral-8x7b-32768", ...)

# Google Gemma
chatModel = ChatGroq(model="gemma2-9b-it", ...)
```

---

## 🐳 Docker

```bash
# Build image
docker build -t medical-chatbot .

# Run container
docker run -p 8080:8080 \
  -e PINECONE_API_KEY=your_key \
  -e GROQ_API_KEY=your_key \
  medical-chatbot
```

---

## 📁 Project Structure

```
medical-chatbot-groq/
├── data/                  ← Put your PDF files here
├── src/
│   ├── __init__.py
│   ├── helper.py          ← PDF loading, chunking, embeddings
│   └── prompt.py          ← System prompt for Llama
├── templates/
│   └── chat.html          ← Chat UI
├── static/
│   └── style.css          ← Styling
├── app.py                 ← Flask app (main)
├── store_index.py         ← One-time PDF → Pinecone upload
├── requirements.txt
├── setup.py
├── Dockerfile
└── .env                   ← Your API keys (never commit!)
```
