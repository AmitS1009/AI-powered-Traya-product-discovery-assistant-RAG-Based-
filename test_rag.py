import sys
import os
print("Starting test...")
sys.path.append(os.path.join(os.getcwd(), 'backend'))

print("Importing chromadb...")
import chromadb
print("Imported chromadb.")

print("Importing embedding functions...")
from chromadb.utils import embedding_functions
print("Imported embedding functions.")

print("Importing vector_store...")
try:
    from app.services import vector_store
    print("Imported vector_store.")
except Exception as e:
    print(f"Failed to import vector_store: {e}")
    sys.exit(1)

print("Querying products...")
try:
    results = vector_store.query_products("dandruff")
    print("Query successful.")
    print(results)
except Exception as e:
    print(f"Query failed: {e}")
