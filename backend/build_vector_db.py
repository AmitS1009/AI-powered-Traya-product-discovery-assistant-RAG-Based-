from app import database, models
from app.services import vector_store
from sqlalchemy.orm import Session

def build_vector_index():
    db = database.SessionLocal()
    products = db.query(models.Product).all()
    
    product_data = []
    for p in products:
        product_data.append({
            "id": p.id,
            "title": p.title,
            "description": p.description or "",
            "features": p.features or [],
            "price": p.price,
            "category": p.category,
            "url": p.url,
            "image_url": p.image_url
        })
    
    if product_data:
        vector_store.add_products_to_vector_db(product_data)
    else:
        print("No products found in DB to index.")
    
    db.close()

if __name__ == "__main__":
    build_vector_index()
