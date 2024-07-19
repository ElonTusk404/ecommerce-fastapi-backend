import datetime
import uuid
import httpx
import jwt
from app.models.user import UserModel
from app.services.user import UserService
import fastapi.security as security
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from config import settings
from app.utils.unit_of_work import UnitOfWork



oauth2_schema = security.OAuth2PasswordBearer("/api/v1/login")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)




async def authenticate_user(email:str, password: str, uow: UnitOfWork = Depends(UnitOfWork)):
    user: UserModel | None = await UserService.get_by_query_one_or_none(uow=uow, email=email)
    if not (user and verify_password(password, user.password)):
        return None
    
    return user



async def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=12)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm="HS256"
    )
    return {"access_token": encoded_jwt, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_schema), uow: UnitOfWork = Depends(UnitOfWork)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user = await UserService.get_by_query_one_or_none(uow = uow, email=payload.get("sub"))
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Could not decode token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

async def get_current_admin_user(token: str = Depends(oauth2_schema), uow: UnitOfWork = Depends(UnitOfWork)):
    user = await get_current_user(token, uow)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Operation forbidden: admin access required")
    return user

async def upload_to_cloud(image):
    async with httpx.AsyncClient() as client:

        timeout = httpx.Timeout(60.0, read=None)

        response = await client.post("https://sd.cuilutech.com/r2/uploadfile", files={'file': (str(uuid.uuid4()), image)}, timeout=timeout)
        response_data = response.json()
        return response_data["data"]
    