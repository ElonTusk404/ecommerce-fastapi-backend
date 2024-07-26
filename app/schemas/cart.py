from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.schemas.product import ProductSchemaInDB, ProductSchemaResponse

class CartSchemaCreate(BaseModel):
    product_id: int = Field(..., description="ID of the product")
    quantity: int = Field(..., description="Quantity of the product", gt=0)

    class Config:
        from_attributes = True

class CartSchemaUpdate(BaseModel):
    product_id: Optional[int] = Field(None, description="ID of the product")
    quantity: Optional[int] = Field(None, description="Quantity of the product", gt=0)

    class Config:
        from_attributes = True

class CartSchemaInDB(BaseModel):
    id: int = Field(..., description="ID of the cart item")
    user_id: int = Field(..., description="ID of the user")
    product_id: int = Field(..., description="ID of the product")
    quantity: int = Field(..., description="Quantity of the product", gt=0)
    created_at: datetime = Field(..., description="Timestamp when the cart item was created")
    updated_at: datetime = Field(..., description="Timestamp when the cart item was last updated")
    product: Optional['ProductSchemaResponse'] = Field(None, description="Product details associated with the cart item")

    class Config:
        from_attributes = True

class CartSchemaResponse(BaseModel):
    id: int = Field(..., description="ID of the cart item")
    product_id: int = Field(..., description="ID of the product")
    quantity: int = Field(..., description="Quantity of the product")
    product: Optional['ProductSchemaResponse'] = Field(None, description="Product details associated with the cart item")

    class Config:
        from_attributes = True
