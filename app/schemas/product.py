from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.schemas.attribute import AttributeSchemaInDB, AttributeSchemaResponse

from pydantic import BaseModel, Field
from typing import Optional

class ProductSchemaCreate(BaseModel):
    name: str = Field(..., description="Name of the product", min_length=8, max_length=64)
    category_id: int = Field(..., description="Category ID of the product")
    description: str = Field(..., description="Description of the product", min_length=64, max_length=512)
    price: int = Field(..., description="Price of the product", gt=0, le=512)
    inventory: Optional[int] = Field(None, description="Quantity of the product in inventory", gt=0, le=512)

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
    name: Optional[str] = Field(None, description="Name of the product", min_length=8, max_length=64)
    category_id: Optional[int] = Field(None, description="Category ID of the product")
    description: Optional[str] = Field(None, description="Description of the product", min_length=64, max_length=512)
    price: Optional[int] = Field(None, description="Price of the product", gt=0, le=512)
    inventory: Optional[int] = Field(None, description="Quantity of the product in inventory", gt=0, le=512)

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
