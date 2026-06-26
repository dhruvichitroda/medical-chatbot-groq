"""
store_index.py — Run this ONCE to upload your PDF knowledge base to Pinecone.

Steps:
  1. Place your PDF files in the data/ folder
  2. Set PINECONE_API_KEY in your .env file
  3. Run: python store_index.py
  4. After it finishes, run: python app.py

NOTE: You do NOT need OPENAI_API_KEY or GROQ_API_KEY for this step.
      Embeddings are generated locally (FREE) using all-MiniLM-L6-v2.
"""

from dotenv import load_dotenv
import os
from src.helper import (
    load_pdf_file,
    filter_to_minimal_docs,
    text_split,
    download_hugging_face_embeddings
)
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

# ── Load environment variables ──────────────────────────────────────────────
load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# ── Step 1: Load PDFs from data/ folder ─────────────────────────────────────
print("📄 Loading PDF files...")
extracted_data = load_pdf_file(data='data/')
print(f"   Loaded {len(extracted_data)} pages from PDFs")

# ── Step 2: Filter metadata ──────────────────────────────────────────────────
print("🧹 Filtering documents...")
filter_data = filter_to_minimal_docs(extracted_data)

# ── Step 3: Split into chunks ────────────────────────────────────────────────
print("✂️  Splitting into chunks...")
text_chunks = text_split(filter_data)
print(f"   Created {len(text_chunks)} text chunks")

# ── Step 4: Load open source embedding model ─────────────────────────────────
print("🤗 Loading HuggingFace embedding model (all-MiniLM-L6-v2)...")
embeddings = download_hugging_face_embeddings()
print("   Embedding model ready (384 dimensions)")

# ── Step 5: Connect to Pinecone ──────────────────────────────────────────────
print("🌲 Connecting to Pinecone...")
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medical-chatbot"

# Create index if it doesn't exist
if not pc.has_index(index_name):
    print(f"   Creating new Pinecone index: '{index_name}'")
    pc.create_index(
        name=index_name,
        dimension=384,          # Must match all-MiniLM-L6-v2 output
        metric="cosine",        # Cosine similarity for text search
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ),
    )
    print("   Index created ✓")
else:
    print(f"   Index '{index_name}' already exists — uploading new data")

# ── Step 6: Upload embeddings to Pinecone ───────────────────────────────────
print(f"⬆️  Uploading {len(text_chunks)} chunks to Pinecone...")
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings,
)

print("\n✅ Done! Your medical knowledge base is ready in Pinecone.")
print("   Now run: python app.py")
