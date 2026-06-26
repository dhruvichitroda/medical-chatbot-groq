# 🏥 Medical Chatbot — AI-Powered RAG System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.3.26-green?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-Llama_3.1-orange?style=for-the-badge)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector_DB-purple?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-3.1.1-black?style=for-the-badge&logo=flask)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?style=for-the-badge&logo=docker)
![AWS](https://img.shields.io/badge/AWS-EC2_+_ECR-yellow?style=for-the-badge&logo=amazon-aws)

**An end-to-end AI Medical Chatbot using Retrieval-Augmented Generation (RAG)**

*Ask any medical question — get accurate answers from a real Medical Book!*

</div>

---

## 🎯 What This Project Does

This chatbot reads a **real Medical Book (PDF)**, stores its knowledge in a **Vector Database**, and answers user medical questions using **Llama 3.1 (open-source, FREE)** — all powered by the RAG architecture.

```
User asks: "What are symptoms of diabetes?"
     ↓
Pinecone finds: Top 3 most relevant passages from Medical Book
     ↓
Llama 3.1 reads: Those passages + user question
     ↓
Answer: "Symptoms include fatigue, hyperglycemia, damage to kidneys..."
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│              Flask Web App (chat.html)                   │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP POST /get
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   RAG PIPELINE                           │
│                                                          │
│  Question → Embedding → Pinecone Search → Top 3 Chunks  │
│                                    ↓                     │
│              Groq Llama 3.1 → Final Answer               │
└─────────────────────────────────────────────────────────┘
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
┌─────────────────┐     ┌─────────────────────┐
│    PINECONE      │     │    GROQ API          │
│  Vector Database │     │  Llama 3.1 8B Model  │
│  5859 chunks     │     │  FREE & Fast ⚡       │
│  384 dimensions  │     │                      │
└─────────────────┘     └─────────────────────┘
```

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🧠 **RAG Architecture** | Retrieves relevant medical context before generating answers |
| ⚡ **Groq + Llama 3.1** | Open-source LLM — replaces paid GPT-4o, cost = $0 |
| 🤗 **HuggingFace Embeddings** | `all-MiniLM-L6-v2` runs locally — no API cost |
| 🌲 **Pinecone Vector DB** | Stores 5859 medical text chunks for fast similarity search |
| 🌐 **Flask Web UI** | Clean chat interface with typing indicator & auto-scroll |
| 🐳 **Docker Ready** | Containerized for easy deployment |
| ☁️ **AWS CI/CD** | Automated deployment via GitHub Actions → ECR → EC2 |

---

## 💰 Cost Comparison

| Component | Original (OpenAI) | This Project (Groq) |
|---|---|---|
| LLM | GPT-4o 💲 Paid | Llama 3.1 ✅ FREE |
| Embeddings | OpenAI Ada 💲 Paid | all-MiniLM-L6-v2 ✅ FREE |
| Vector DB | Pinecone Free tier | Pinecone Free tier ✅ FREE |
| **Total Cost** | **~$10-20/month** | **$0.00/month** |

---

## 🛠️ Tech Stack

```
Language:      Python 3.10
Framework:     Flask 3.1.1
LLM:           Llama 3.1 8B (via Groq API) — FREE
Embeddings:    sentence-transformers/all-MiniLM-L6-v2 — FREE
Vector DB:     Pinecone (Serverless) — FREE tier
AI Framework:  LangChain 0.3.26
Frontend:      HTML, CSS, jQuery, Bootstrap
DevOps:        Docker, AWS EC2, AWS ECR, GitHub Actions
```

---

## 📁 Project Structure

```
medical-chatbot-groq/
│
├── 📂 data/
│   └── Medical_book.pdf          ← Medical knowledge base
│
├── 📂 src/
│   ├── __init__.py
│   ├── helper.py                 ← PDF loading, chunking, embeddings
│   └── prompt.py                 ← System prompt for Llama 3.1
│
├── 📂 templates/
│   └── chat.html                 ← Chat UI
│
├── 📂 static/
│   └── style.css                 ← Styling
│
├── 📂 research/
│   └── trials.ipynb              ← Experiments & testing notebook
│
├── 📂 .github/workflows/
│   └── cicd.yaml                 ← GitHub Actions CI/CD pipeline
│
├── app.py                        ← Main Flask application
├── store_index.py                ← One-time PDF → Pinecone upload
├── requirements.txt              ← Python dependencies
├── Dockerfile                    ← Container configuration
├── setup.py                      ← Package setup
└── .env.example                  ← Environment variables template
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10
- Anaconda
- Pinecone account (free) — https://app.pinecone.io
- Groq account (free) — https://console.groq.com

### Step 1 — Clone Repository
```bash
git clone https://github.com/dhruvichitroda/medical-chatbot-groq.git
cd medical-chatbot-groq
```

### Step 2 — Create Environment
```bash
conda create -n medibot python=3.10 -y
conda activate medibot
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Configure API Keys
```bash
cp .env.example .env
```
Edit `.env`:
```
PINECONE_API_KEY=your_pinecone_key_here
GROQ_API_KEY=your_groq_key_here
```

### Step 5 — Build Knowledge Base (Run ONCE)
```bash
python store_index.py
```
Output:
```
📄 Loading PDF files... Loaded 637 pages
✂️  Splitting into chunks... Created 5859 chunks
🤗 Loading HuggingFace embedding model (384 dimensions)
🌲 Connecting to Pinecone... Index created ✓
⬆️  Uploading 5859 chunks to Pinecone...
✅ Done! Knowledge base ready.
```

### Step 6 — Run Application
```bash
python app.py
```

### Step 7 — Open Browser
```
http://localhost:8080
```

---

## 🐳 Docker Deployment

```bash
# Build image
docker build -t medical-chatbot-groq .

# Run container
docker run -d -p 8080:8080 \
  -e PINECONE_API_KEY=your_key \
  -e GROQ_API_KEY=your_key \
  medical-chatbot-groq
```

---

## ☁️ AWS Deployment (CI/CD)

This project includes a complete **GitHub Actions CI/CD pipeline**:

```
Code Push to GitHub (main branch)
         ↓
GitHub Actions triggered
         ↓
Build Docker Image
         ↓
Push to AWS ECR (Elastic Container Registry)
         ↓
Pull & Run on AWS EC2
         ↓
Live on Internet! 🌐
```

### GitHub Secrets Required
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION
ECR_REPO
PINECONE_API_KEY
GROQ_API_KEY
```

---

## 🔄 How RAG Works — Deep Dive

```
OFFLINE (store_index.py — run once):
Medical PDF → Extract Text → Split into 500-char chunks
           → Generate Embeddings (384 numbers per chunk)
           → Store in Pinecone Vector DB

ONLINE (app.py — runs on every question):
User Question → Generate Embedding
             → Search Pinecone (find top 3 similar chunks)
             → Build Prompt: System + Context + Question
             → Send to Groq Llama 3.1
             → Return Answer to User
```

---

## 🔄 Switch LLM Models

In `app.py`, easily switch Groq models:

```python
# Fast (default)
chatModel = ChatGroq(model="llama-3.1-8b-instant")

# Best quality
chatModel = ChatGroq(model="llama-3.3-70b-versatile")

# Large context window
chatModel = ChatGroq(model="mixtral-8x7b-32768")
```

---

## 📊 Performance Stats

```
PDF Pages Loaded:      637 pages
Text Chunks Created:   5859 chunks
Embedding Dimensions:  384
Similarity Metric:     Cosine
Chunks Retrieved/Query: 3
Average Response Time:  ~2-3 seconds
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Dhruvi Chitroda**

[![GitHub](https://img.shields.io/badge/GitHub-dhruvichitroda-black?style=flat&logo=github)](https://github.com/dhruvichitroda)

---

<div align="center">

⭐ **If this project helped you, please give it a star!** ⭐

*Built with ❤️ using LangChain + Groq + Pinecone*

</div>
