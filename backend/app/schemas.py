from pydantic import BaseModel
from typing import List, Optional, Any

class ProductBase(BaseModel):
    title: str
    price: str
    description: Optional[str] = None
    features: Optional[List[str]] = []
    image_url: Optional[str] = None
    category: Optional[str] = None
    url: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
