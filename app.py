from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq                              # ✅ GROQ - replaces ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os


app = Flask(__name__)

# ─────────────────────────────────────────────
# 1. LOAD ENVIRONMENT VARIABLES
# ─────────────────────────────────────────────
load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GROQ_API_KEY     = os.environ.get('GROQ_API_KEY')       # ✅ Groq key (was OPENAI_API_KEY)

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"]     = GROQ_API_KEY


# ─────────────────────────────────────────────
# 2. LOAD OPEN SOURCE EMBEDDING MODEL
# (all-MiniLM-L6-v2 — runs locally, FREE)
# ─────────────────────────────────────────────
embeddings = download_hugging_face_embeddings()


# ─────────────────────────────────────────────
# 3. CONNECT TO EXISTING PINECONE INDEX
# (Data was already uploaded by store_index.py)
# ─────────────────────────────────────────────
index_name = "medical-chatbot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)


# ─────────────────────────────────────────────
# 4. CREATE RETRIEVER
# Fetches top 3 most relevant chunks per query
# ─────────────────────────────────────────────
retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)


# ─────────────────────────────────────────────
# 5. LOAD GROQ LLM  ✅ OPEN SOURCE + FREE
#
# Available Groq models (all free tier):
#   - llama-3.1-8b-instant    → fastest, good quality
#   - llama-3.3-70b-versatile → best quality, slightly slower
#   - mixtral-8x7b-32768      → large context window
#   - gemma2-9b-it            → Google's Gemma 2
# ─────────────────────────────────────────────
chatModel = ChatGroq(
    model="llama-3.1-8b-instant",   # Fast + free
    groq_api_key=GROQ_API_KEY,
    temperature=0.2,                  # Low temp = more factual medical answers
    max_tokens=512                    # Enough for concise medical answers
)


# ─────────────────────────────────────────────
# 6. BUILD PROMPT TEMPLATE
# ─────────────────────────────────────────────
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),   # Medical assistant instructions + {context}
        ("human", "{input}"),        # User's actual question
    ]
)


# ─────────────────────────────────────────────
# 7. BUILD RAG CHAIN
# retriever → context → prompt → Groq → answer
# ─────────────────────────────────────────────
question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


# ─────────────────────────────────────────────
# 8. FLASK ROUTES
# ─────────────────────────────────────────────
@app.route("/")
def index():
    """Serves the chat UI (templates/chat.html)"""
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    """
    Receives user message → runs RAG chain → returns answer.
    Called by jQuery AJAX in chat.html on every message submit.
    """
    msg = request.form["msg"]

    print(f"\n[USER] {msg}")

    try:
        response = rag_chain.invoke({"input": msg})
        answer = response["answer"]
        print(f"[GROQ] {answer}\n")
        return str(answer)

    except Exception as e:
        print(f"[ERROR] {e}")
        return "Sorry, I encountered an error. Please try again.", 500


# ─────────────────────────────────────────────
# 9. RUN APP
# ─────────────────────────────────────────────
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
