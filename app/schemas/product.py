from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.schemas.attribute import AttributeSchemaInDB, AttributeSchemaResponse

class ProductSchemaCreate(BaseModel):
    name: str
    category_id: int
    description: str
    price: int
    inventory: Optional[int] = None 

    class Config:
        from_attributes = True



class ImageSchemaCreate(BaseModel):
    url: str

class ImageSchemaInDB(ImageSchemaCreate):
    id: int

class InventorySchemaInDB(BaseModel):
    quantity: int

    class Config:
        from_attributes = True

class ProductSchemaInDB(BaseModel):
    id: int
    name: str
    category_id: int
    description: str
    price: int
    created_at: datetime
    updated_at: datetime
    images: List[ImageSchemaInDB] = []
    inventory: Optional[InventorySchemaInDB] = None  
    attributes: List[AttributeSchemaResponse] = []

    class Config:
        from_attributes = True

class ProductSchemaUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    price: Optional[int] = None
    inventory: Optional[int] = None  

    class Config:
        from_attributes = True

class ProductSchemaResponse(BaseModel):
    id: int
    name: str
    category_id: int
    description: str
    price: int
    images: List[ImageSchemaInDB] = []
    attributes: List[AttributeSchemaResponse] = []

    class Config:
        from_attributes = True
