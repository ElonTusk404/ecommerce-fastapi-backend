from app.utils.service import BaseService


class AttributeService(BaseService):
    base_repository: str = 'attribute'

class ValueService(BaseService):
    base_repository: str = 'value'