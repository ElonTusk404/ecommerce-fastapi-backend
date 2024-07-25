from datetime import datetime
from pydantic import BaseModel



class AttributeSchemaBase(BaseModel):
    product_id: int
    name: str
    value: str

class AttributeSchemaCreate(AttributeSchemaBase):
    pass

class AttributeSchemaUpdate(BaseModel):
    name: str
    value: str

class AttributeSchemaInDBBase(AttributeSchemaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AttributeSchema(AttributeSchemaInDBBase):
    pass

class AttributeSchemaInDB(AttributeSchemaInDBBase):
    pass
class AttributeSchemaResponse(BaseModel):
    id: int
    name: str
    value: str

