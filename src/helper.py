from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List
from langchain.schema import Document


# Extract Data From the PDF File
def load_pdf_file(data):
    """
    Loads all PDF files from a given directory.

    Args:
        data (str): Path to the folder containing PDF files (e.g., 'data/')

    Returns:
        list[Document]: List of LangChain Document objects, one per PDF page
    """
    loader = DirectoryLoader(
        data,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )
    documents = loader.load()
    return documents


def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """
    Cleans document metadata — keeps only 'source' field.
    Removes noisy metadata that Pinecone doesn't need.

    Args:
        docs (List[Document]): Raw documents from PDF loader

    Returns:
        List[Document]: Cleaned documents with minimal metadata
    """
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )
    return minimal_docs


# Split the Data into Text Chunks
def text_split(extracted_data):
    """
    Splits large documents into smaller overlapping chunks.

    Args:
        extracted_data (list[Document]): Full documents

    Returns:
        list[Document]: Smaller chunks ready for embedding
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,    # Each chunk = max 500 characters
        chunk_overlap=20   # 20 chars overlap between chunks for context continuity
    )
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks


# Download the Embeddings from HuggingFace (OPEN SOURCE - FREE)
def download_hugging_face_embeddings():
    """
    Loads the all-MiniLM-L6-v2 embedding model from HuggingFace.
    - Produces 384-dimensional vectors
    - Runs LOCALLY on your CPU (no API call needed)
    - Downloads once, then cached in ~/.cache/huggingface/

    Returns:
        HuggingFaceEmbeddings: Embedding model object
    """
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2'
    )
    return embeddings
