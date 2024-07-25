from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CategorySchemaBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class CategorySchemaCreate(CategorySchemaBase):
    pass

class CategorySchemaUpdate(CategorySchemaBase):
    pass

class CategorySchemaInDBBase(CategorySchemaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CategorySchema(CategorySchemaInDBBase):
    pass

class CategorySchemaInDB(CategorySchemaInDBBase):
    pass

class CategoryResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None

    class Config:
        from_attributes = True
