from app.models.models import ImageModel
from app.utils.repository import SqlAlchemyRepository


class ImageRepository(SqlAlchemyRepository):
    model = ImageModel