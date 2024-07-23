from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

from app.schemas.product import ProductInDB

class OrderSchemaStatusEnum(str, Enum):
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"
    canceled = "canceled"

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

    class Config:
        from_attributes = True

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
    product: Optional[ProductInDB]

    class Config:
        from_attributes = True
