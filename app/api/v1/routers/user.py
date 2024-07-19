from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserModel
from app.schemas.user import UserSchema
from app.services.user import UserService
from app.utils.unit_of_work import UnitOfWork
from fastapi.security import OAuth2PasswordRequestForm
from app.services.security import create_access_token, authenticate_user, get_current_user, get_password_hash

user_router = APIRouter(prefix='/api/v1', tags=['Reg&Login&Me'])


@user_router.post('/register')
async def register_user(user_data: UserSchema, uow: UnitOfWork = Depends(UnitOfWork)):
    user: UserModel | None = await UserService.get_by_query_one_or_none(uow=uow, email=user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    user_data.password = get_password_hash(user_data.password)

    user_data = user_data.model_dump(exclude_unset=True)
    new_user : UserModel = await UserService.add_one_and_get_obj(uow=uow, **user_data)
    return new_user

@user_router.post('/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], uow: UnitOfWork = Depends(UnitOfWork)):
    user = await authenticate_user(form_data.username, password=form_data.password, uow=uow)
    if not user:
        raise HTTPException(status_code=303, detail='no user')
    return await create_access_token(data={'sub': form_data.username})

@user_router.post('/me', status_code=status.HTTP_200_OK)
async def me(current_user: Annotated[UserModel, Depends(get_current_user)]):
    return current_user