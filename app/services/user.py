from app.utils.service import BaseService


class UserService(BaseService):
    base_repository: str = 'user'