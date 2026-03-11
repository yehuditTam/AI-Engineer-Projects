from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.cohere import Cohere
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Cohere Embeddings (multilingual, great for Hebrew)
embed_model = CohereEmbedding(
    cohere_api_key=COHERE_API_KEY,
    model_name="embed-multilingual-v3.0",
    input_type="search_document",
)

# Cohere LLM
llm = Cohere(
    api_key=COHERE_API_KEY,
    model="command-r-08-2024",
)

# Set global defaults
Settings.llm = llm
Settings.embed_model = embed_model

# ChromaDB setup (local, no internet blocking)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection("rag_docs")

# Vector store
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


def create_index(documents):
    """Create vector index with Cohere + ChromaDB"""
    return VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,
    )


def load_index():
    """Load existing index"""
    return VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model,
    )
