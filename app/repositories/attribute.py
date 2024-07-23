from app.models.models import AttributeModel
from app.utils.repository import SqlAlchemyRepository


class AttributeRepository(SqlAlchemyRepository):
    model = AttributeModel