from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserModel
from app.schemas.user import UserSchemaCreate, UserSchemaResponse
from app.services.user import UserService
from app.utils.unit_of_work import UnitOfWork
from fastapi.security import OAuth2PasswordRequestForm
from app.services.security import create_access_token, authenticate_user, get_current_user, get_password_hash

user_router = APIRouter(prefix='/api/v1/users', tags=['Reg&Login&Me'])


@user_router.post('/register', status_code=status.HTTP_201_CREATED, response_model = UserSchemaResponse)
async def register_user(user_data: UserSchemaCreate, uow: UnitOfWork = Depends(UnitOfWork)):

    """
    Registers a new user.

    This endpoint allows users to register by providing their personal details and password.
    The password will be hashed before storing the user data. If a user with the given email
    already exists, a conflict status (409) will be raised.

    :`UserSchemaCreate`: A schema containing the user data required for registration.\n
        - first_name (str): The user's first name, limited to 50 characters.
        - last_name (str): The user's last name, limited to 50 characters.
        - email (EmailStr): The user's email address.
        - password (str): The user's password, with a minimum length of 8 characters and a maximum length of 32 characters.\n
    :return: Status `201` with `UserSchemaResponse` object containing:\n
        - id (int): The unique identifier of the newly created user.
        - first_name (str): The user's first name.
        - last_name (str): The user's last name.
        - email (EmailStr): The user's email address.\n
    :raises HTTPException: If a user with the given email already exists, a conflict status `409` will be raised.
    """
    
    user: UserModel | None = await UserService.get_by_query_one_or_none(uow=uow, email=user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    user_data.password = get_password_hash(user_data.password)

    user_data = user_data.model_dump(exclude_unset=True)
    new_user : UserModel = await UserService.add_one_and_get_obj(uow=uow, **user_data)
    return new_user

@user_router.post('/login', status_code=status.HTTP_200_OK)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], uow: UnitOfWork = Depends(UnitOfWork)):
    
    """
    Authenticates a user and provides an access token.

    :param form_data: A form containing the username and password for authentication.\n
        - email (str): The user's email.
        - password (str): The user's password.
    :return: status code `201` with JSON object containing:\n
        - access_token (str): The JWT token for accessing protected resources.
        - token_type (str): The type of the token, typically "bearer".
    :raises HTTPException: If authentication fails, a status `404` with a detail message 'no user' will be raised.
    """
    
    user = await authenticate_user(form_data.username, password=form_data.password, uow=uow)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no user')
    return await create_access_token(data={'sub': form_data.username})

@user_router.post('/me', status_code=status.HTTP_200_OK, response_model=UserSchemaResponse)
async def me(current_user: Annotated[UserModel, Depends(get_current_user)]):
    return current_user