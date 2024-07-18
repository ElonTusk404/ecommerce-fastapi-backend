from pydantic import BaseModel, Field, EmailStr

class UserSchema(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)
    class Config:
       from_attributes=True
