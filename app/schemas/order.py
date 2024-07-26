from pydantic import BaseModel, Field
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
    phone_number: str = Field(..., description="Phone number of the customer", min_length=10, max_length=15)
    country: str = Field(..., description="Country of the customer", min_length=2, max_length=56)
    city: str = Field(..., description="City of the customer", min_length=1, max_length=85)
    address: str = Field(..., description="Address of the customer", min_length=5, max_length=100)

    class Config:
        from_attributes = True

class OrderSchemaUpdate(BaseModel):
    status: Optional[OrderSchemaStatusEnum] = Field(None, description="Status of the order")
    phone_number: Optional[str] = Field(None, description="Phone number of the customer", min_length=10, max_length=15)
    country: Optional[str] = Field(None, description="Country of the customer", min_length=2, max_length=56)
    city: Optional[str] = Field(None, description="City of the customer", min_length=1, max_length=85)
    address: Optional[str] = Field(None, description="Address of the customer", min_length=5, max_length=100)

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


