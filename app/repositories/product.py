from app.models.product import ProductModel
from app.utils.repository import SqlAlchemyRepository


class ProductRepository(SqlAlchemyRepository):
    model = ProductModel

    