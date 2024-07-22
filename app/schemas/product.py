from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    category_id: int
    description: str
    price: int
    inventory: Optional[int] = None 

    class Config:
        from_attributes = True



class ImageCreate(BaseModel):
    url: str

class ImageInDB(ImageCreate):
    id: int

class InventoryInDB(BaseModel):
    quantity: int

    class Config:
        from_attributes = True

class ProductInDB(BaseModel):
    id: int
    name: str
    category_id: int
    description: str
    price: int
    created_at: datetime
    updated_at: datetime
    images: List[ImageInDB] = []
    inventory: Optional[InventoryInDB] = None  

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    price: Optional[int] = None
    images: Optional[List[str]] = None 
    inventory: Optional[int] = None  

    class Config:
        from_attributes = True
