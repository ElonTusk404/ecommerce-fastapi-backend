from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    category_id: int
    description: str
    price: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    price: Optional[int] = None

class ProductInDBBase(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Product(ProductInDBBase):
    images: List[str] = []  # предполагается, что у вас есть список URL изображений
    inventory: Optional[dict] = None  # Замените на соответствующий тип для инвентаря
    values: List[dict] = []  # Замените на соответствующий тип для значений

class ProductInDB(ProductInDBBase):
    pass
