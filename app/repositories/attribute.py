from app.models.models import AttributeModel, ValueModel
from app.utils.repository import SqlAlchemyRepository


class AttributeRepository(SqlAlchemyRepository):
    model = AttributeModel

class ValueRepository(SqlAlchemyRepository):
    model = ValueModel