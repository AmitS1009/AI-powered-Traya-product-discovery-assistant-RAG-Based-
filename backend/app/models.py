from sqlalchemy import Column, Integer, String, Float, Text, ARRAY, JSON
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(String) # Keeping as string for now to handle currency symbols
    description = Column(Text)
    features = Column(JSON) # Store list of features as JSON
    image_url = Column(String)
    category = Column(String, index=True)
    url = Column(String, unique=True)
