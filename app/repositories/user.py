from app.models.user import UserModel
from app.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = UserModel

