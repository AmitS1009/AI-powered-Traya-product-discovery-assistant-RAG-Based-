from app.services import vector_store
import os

# Placeholder for LLM integration
# If you have an API key, you can use it here.
# For now, we'll do a simple retrieval-based response.

def generate_response(query: str):
    # 1. Retrieve relevant products
    results = vector_store.query_products(query, n_results=3)
    
    if not results or not results['documents']:
        return {
            "response": "I couldn't find any products matching your request.",
            "products": []
        }
    
    # Extract product info
    retrieved_products = []
    ids = results['ids'][0]
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]
    
    for i in range(len(ids)):
        retrieved_products.append({
            "id": ids[i],
            "text": documents[i],
            "metadata": metadatas[i]
        })
    
    # 2. Generate answer using LLM (Mocked for now if no key)
    # In a real scenario, you'd pass 'retrieved_products' and 'query' to an LLM.
    
    product_names = [p['metadata']['title'] for p in retrieved_products]
    
    response_text = f"Based on your request '{query}', here are some recommendations:\n\n"
    for p in retrieved_products:
        title = p['metadata']['title']
        price = p['metadata']['price']
        response_text += f"- **{title}** ({price})\n  {p['text'][:150]}...\n\n"
        
    return {
        "response": response_text,
        "products": retrieved_products
    }
