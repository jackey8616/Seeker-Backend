from typing import Optional

from bson import ObjectId

from models.user import User
from repository import Repository


class UserRepository(Repository):
    @property
    def _table_name(self) -> str:
        return "users"

    def get_by_id(self, id: str) -> Optional[User]:
        raw_user = self._table.find_one({"_id": ObjectId(id)})
        if raw_user is None:
            return None
        return User.model_validate(obj=raw_user)

    def get_by_google_id(self, google_id: str) -> Optional[User]:
        raw_user = self._table.find_one({"google_userinfo.id": {"$eq": google_id}})
        if raw_user is None:
            return None
        return User.model_validate(obj=raw_user)

    def insert_one(self, user: User) -> User:
        result = self._table.insert_one(user.model_dump())
        inserted_user = self.get_by_id(id=result.inserted_id)
        if inserted_user is None:
            raise ValueError("Insert failed")
        return inserted_user
