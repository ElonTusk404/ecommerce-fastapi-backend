from pydantic import BaseModel, Field, EmailStr

class UserSchemaCreate(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=32)

    class Config:
        from_attributes = True

class UserSchemaUpdate(BaseModel):
    first_name: str = Field(None, max_length=50)
    last_name: str = Field(None, max_length=50)
    email: EmailStr = None
    password: str = Field(None, min_length=8, max_length=32)

    class Config:
        from_attributes = True

class UserSchemaResponse(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True
