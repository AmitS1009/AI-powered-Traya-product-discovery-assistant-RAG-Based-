import chromadb
from chromadb.utils import embedding_functions
import os

# Persistent client
CHROMA_DB_PATH = os.path.join(os.path.dirname(__file__), "../../chroma_db")
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Use a default embedding function (SentenceTransformers)
# Note: This downloads the model locally.
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection = client.get_or_create_collection(name="products", embedding_function=sentence_transformer_ef)

def add_products_to_vector_db(products):
    ids = [str(p["id"]) for p in products]
    documents = [f"{p['title']}. {p['description']}. Features: {', '.join(p['features'])}" for p in products]
    metadatas = [{"title": p["title"], "price": p["price"], "category": p["category"], "url": p["url"], "image_url": p["image_url"]} for p in products]
    
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    print(f"Upserted {len(products)} documents to ChromaDB.")

def query_products(query_text, n_results=5):
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results
