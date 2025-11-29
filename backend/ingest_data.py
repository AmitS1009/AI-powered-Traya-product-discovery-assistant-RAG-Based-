import json
import os
from sqlalchemy.orm import Session
from app import models, database

def ingest_data():
    db = database.SessionLocal()
    
    data_path = os.path.join(os.path.dirname(__file__), "../data/products.json")
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    print(f"Found {len(products)} products to ingest.")
    
    count = 0
    for p_data in products:
        # Check if exists
        exists = db.query(models.Product).filter(models.Product.url == p_data["url"]).first()
        if not exists:
            product = models.Product(
                title=p_data["title"],
                price=p_data["price"],
                description=p_data["description"],
                features=p_data["features"],
                image_url=p_data["image_url"],
                category=p_data["category"],
                url=p_data["url"]
            )
            db.add(product)
            count += 1
    
    db.commit()
    print(f"Ingested {count} new products.")
    db.close()

if __name__ == "__main__":
    # Create tables if they don't exist
    models.Base.metadata.create_all(bind=database.engine)
    ingest_data()
