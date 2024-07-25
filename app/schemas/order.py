from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

from app.schemas.product import ProductSchemaInDB, ProductSchemaResponse

class OrderSchemaStatusEnum(str, Enum):
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"
    canceled = "canceled"



class OrderSchemaCreate(BaseModel):
    phone_number: str
    country: str
    city: str
    address: str

    class Config:
        from_attributes = True

class OrderSchemaUpdate(BaseModel):
    status: Optional[OrderSchemaStatusEnum] = None
    phone_number: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True

class OrderSchemaItemInDB(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: int
    product: Optional[ProductSchemaResponse]

    class Config:
        from_attributes = True

class OrderSchemaItemResponse(BaseModel):
    quantity: int
    price: int
    product: Optional[ProductSchemaResponse]

    class Config:
        from_attributes = True

class OrderSchemaResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    status: OrderSchemaStatusEnum
    total_amount: int
    phone_number: str
    country: str
    city: str
    address: str
    order_items: List[OrderSchemaItemResponse] = []

    class Config:
        from_attributes = True


