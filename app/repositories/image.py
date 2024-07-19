from app.models.image import ImageModel
from app.utils.repository import SqlAlchemyRepository


class ImageRepository(SqlAlchemyRepository):
    model = ImageModel