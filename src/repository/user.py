from typing import Optional

from models.user import User
from repository import Repository


class UserRepository(Repository[User]):
    @property
    def _table_name(self) -> str:
        return "users"

    def get_by_google_id(self, google_id: str) -> Optional[User]:
        raw_user = self._table.find_one({"google_userinfo.id": {"$eq": google_id}})
        if raw_user is None:
            return None
        return User.model_validate(obj=raw_user)

    def update(self, user: User):
        self._table.find_one_and_update(
            filter={"_id": user.id},
            update={
                "$set": user.model_dump(
                    by_alias=True,
                    exclude={"id"},
                ),
            },
        )
