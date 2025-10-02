from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import os

def load_pdf(file_path):
    """
    Load a PDF file using LangChain's PyPDFLoader.
    
    Args:
        file_path (str): Path to the PDF file.
    
    Returns:
        list: List of Document objects, each representing a page.
    """
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    return pages

def chunk_resume_documents(pages, chunk_size=1000, chunk_overlap=200):
    """
    Chunk the resume documents using RecursiveCharacterTextSplitter.
    
    Args:
        pages (list): List of Document objects.
        chunk_size (int): Maximum size of each chunk.
        chunk_overlap (int): Overlap between chunks.
    
    Returns:
        list: List of chunked Document objects.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],  # Prioritize paragraphs, then lines, etc.
    )
    chunks = text_splitter.split_documents(pages)
    return chunks

def embed_chunks(chunks):
    """
    Embed the chunks using Hugging Face's sentence-transformers model.
    
    Args:
        chunks (list): List of chunked Document objects.
    
    Returns:
        list: List of embedding vectors.
    """
    # Initialize Hugging Face embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Extract text content from chunks
    texts = [chunk.page_content for chunk in chunks]
    
    # Generate embeddings
    vectors = embeddings.embed_documents(texts)
    return vectors

def store_embeddings_in_chroma(chunks, embeddings, persist_directory="docs/chroma/"):
    """
    Store the embeddings and documents in ChromaDB.
    
    Args:
        chunks (list): List of chunked Document objects.
        embeddings (list): List of embedding vectors.
        persist_directory (str): Directory to persist the ChromaDB database.
    """
    # Remove old database files if any
    if os.path.exists(persist_directory):
        os.system(f"rm -rf {persist_directory}")
    
    # Store in ChromaDB
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
        persist_directory=persist_directory
    )
    print(f"Number of vectors stored: {vectordb._collection.count()}")
    return vectordb

# Example usage:
pages = load_pdf("../data/Li_Rongcheng_Resume_MLE_Sep25.pdf")
print(f"Number of pages: {len(pages)}")
if pages:
    chunks = chunk_resume_documents(pages)
    print(f"Number of chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks[:5]):  # Print first 5 chunks as example
        print(f"\n--- Chunk {i+1} ---\n")
        print(chunk.page_content)
    
    # Generate embeddings for all chunks
    embeddings = embed_chunks(chunks)
    print(f"Generated {len(embeddings)} embeddings.")
    
    # Store embeddings in ChromaDB
    persist_directory = "docs/chroma/"
    vectordb = store_embeddings_in_chroma(chunks, embeddings, persist_directory)