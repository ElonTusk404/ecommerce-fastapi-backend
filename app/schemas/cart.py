from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.schemas.product import ProductInDB

class CartSchemaCreate(BaseModel):
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

class CartSchemaUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None

    class Config:
        from_attributes = True

class CartSchemaInDB(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    created_at: datetime
    updated_at: datetime
    product: Optional[ProductInDB]

    class Config:
        from_attributes = True