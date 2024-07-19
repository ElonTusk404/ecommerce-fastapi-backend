from typing import Annotated, List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from app.models.category import CategoryModel
from app.models.user import UserModel
from app.schemas.product import ProductCreate, ProductInDB, ProductUpdate
from app.services.product import ProductService
from app.utils.unit_of_work import UnitOfWork
from app.services.image import ImageService
from app.services.security import upload_to_cloud
from app.services.security import get_current_user, get_current_admin_user


product_router = APIRouter(prefix='/api/v1/product', tags=['Product\'s Admin'])

@product_router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProductInDB)
async def add_product(
    new_product_data: ProductCreate,
    admin_user: Annotated[UserModel, Depends(get_current_admin_user)],
    uow: UnitOfWork = Depends(UnitOfWork)
):
    return await ProductService.add_one_and_get_obj(uow=uow, **new_product_data.model_dump(exclude_unset=True))

@product_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ProductInDB)
async def get_product(
    id: int,
    admin_user: Annotated[UserModel, Depends(get_current_admin_user)],
    uow: UnitOfWork = Depends(UnitOfWork)
):
    product = await ProductService.get_product_with_images(uow=uow, id=id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return product

@product_router.put('/{id}', status_code=status.HTTP_200_OK, response_model=ProductInDB)
async def update_product(
    id: int, 
    product_info: ProductUpdate,
    admin_user: Annotated[UserModel, Depends(get_current_admin_user)],
    uow: UnitOfWork = Depends(UnitOfWork)
):
    exists_product = await ProductService.get_by_query_one_or_none(uow=uow, id = id)
    if not exists_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await ProductService.update_one_by_id(uow=uow, _id=id, **product_info.model_dump(exclude_unset=True))
@product_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    id: int,
    admin_user: Annotated[UserModel, Depends(get_current_admin_user)],
    uow: UnitOfWork = Depends(UnitOfWork)
):
    exists_product = await ProductService.get_by_query_one_or_none(uow=uow, id = id)
    if not exists_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await ProductService.delete_by_query(uow=uow, id=id)

@product_router.post('/images/{id}', status_code=status.HTTP_200_OK)
async def add_images_to_product(
    id: int,
    admin_user: Annotated[UserModel, Depends(get_current_admin_user)],
    images: list[UploadFile] = File(...),
    uow: UnitOfWork = Depends(UnitOfWork)
):
    exists_product = await ProductService.get_by_query_one_or_none(uow=uow, id = id)
    if not exists_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    accepted_image_types = ["image/jpeg", "image/png"]
    for image in images:
        if image.content_type not in accepted_image_types:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: {image.content_type}. Only JPEG, PNG are accepted."
        )
        image_url = await upload_to_cloud(await image.read())
        await ImageService.add_one(uow=uow, product_id=id, url=image_url)



    
