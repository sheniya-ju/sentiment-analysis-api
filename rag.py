import chromadb
from chromadb.utils import embedding_functions
from langchain_community.llms import Ollama
import os

# Setup ChromaDB client
chroma_client = chromadb.Client()

# Use sentence transformers for embeddings
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Create or get collection
collection = chroma_client.get_or_create_collection(
    name="documents",
    embedding_function=embedding_fn
)

# Setup Ollama LLM
llm = Ollama(model="llama3.2:1b")

def add_document(filename, content):
    # Split content into chunks of 500 characters
    chunks = []
    chunk_size = 500
    for i in range(0, len(content), chunk_size):
        chunks.append(content[i:i+chunk_size])

    # Store each chunk in ChromaDB
    for idx, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"{filename}_{idx}"]
        )

    return len(chunks)

def answer_question(question):
    # Search ChromaDB for relevant chunks
    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    if not results["documents"][0]:
        return "No documents found. Please upload a document first."

    # Build context from retrieved chunks
    context = "\n\n".join(results["documents"][0])

    # Send context + question to Ollama
    prompt = f"""Use the following context to answer the question.
If the answer is not in the context, say 'I don't know based on the provided document.'

Context:
{context}

Question: {question}

Answer:"""

    response = llm.invoke(prompt)
    return response