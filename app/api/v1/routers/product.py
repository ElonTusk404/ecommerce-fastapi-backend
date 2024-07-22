from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from typing import Annotated, List
from app.models.models import ProductModel
from app.models.user import UserModel
from app.schemas.product import ImageInDB, ProductCreate, ProductInDB
from app.services.category import CategoryService
from app.services.product import ProductService
from app.services.inventory import InventoryService
from app.services.image import ImageService
from app.services.security import upload_to_cloud
from app.services.security import get_current_user, get_current_admin_user
from app.utils.unit_of_work import UnitOfWork

product_router = APIRouter(prefix='/api/v1/product', tags=['Product\'s Admin'])

@product_router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProductInDB)
async def add_product(
    admin_user: Annotated[UserModel, Depends(get_current_admin_user)],
    new_product_data: ProductCreate = Depends(),
    images: List[UploadFile] = File(...),
    uow: UnitOfWork = Depends(UnitOfWork)
):
    category = await CategoryService.get_by_query_one_or_none(uow=uow, id=new_product_data.category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Category with id {new_product_data.category_id} not found')
    product = await ProductService.add_one_and_get_obj(
        uow=uow,
        name=new_product_data.name,
        description=new_product_data.description,
        category_id=new_product_data.category_id,
        price=new_product_data.price,
    )

    if images:
        for image in images:
            if image.content_type not in ["image/jpeg", "image/png"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid file type: {image.content_type}. Only JPEG, PNG are accepted."
                )
            image_content = await image.read()
            image_url = await upload_to_cloud(image_content)
            await ImageService.add_one(uow=uow, product_id=product.id, url=image_url)

    if new_product_data.inventory is not None:
        await InventoryService.add_one_and_get_obj(uow=uow, product_id=product.id, quantity=new_product_data.inventory)

    product_info = await ProductService.get_full_product_info(uow=uow, id=product.id)

    return product_info

@product_router.get('/{product_id}', response_model=ProductInDB)
async def get_product(
    product_id: int,
    user: Annotated[UserModel, Depends(get_current_user)],
    uow: UnitOfWork = Depends(UnitOfWork)
):
    product = await ProductService.get_full_product_info(uow=uow, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found."
        )
    return product
@product_router.get('/images/{product_id}', status_code=status.HTTP_200_OK, response_model=List[ImageInDB])
async def get_product_images(
    product_id: int,
    user: Annotated[UserModel, Depends(get_current_user)],
    uow: UnitOfWork = Depends(UnitOfWork)
):
    images = await ImageService.get_by_query_all(uow=uow, product_id=product_id)
    if not images:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return images