from datetime import datetime, timedelta, timezone

from dtos.google.oauth_dtos import GoogleUserInfo
from models.user.execution_count import ModelExecutionCount
from models.user.user import ModelUser
from repository.user import UserRepository
from services.user import UserService
from tests.unit.services.user.user_service import UnitTestUserService


class TestGetUserInfo(UnitTestUserService):
    def test_not_found(
        self, mock_user_repository: UserRepository, user_service: UserService
    ):
        mock_user_repository.get_by_id.return_value = None
        user_info = user_service.get_user_info(user_id="1")
        assert user_info is None

    def test_none_execution_count(
        self, mock_user_repository: UserRepository, user_service: UserService
    ):
        mock_user_repository.get_by_id.return_value = ModelUser(
            _id="1",
            google_userinfo=GoogleUserInfo(
                id="1",
                name="John Doe",
                family_name="Doe",
                given_name="John",
                picture="https://example.com/picture.jpg",
            ),
            google_credentials=None,
            execution_count=None,
        )
        user_info = user_service.get_user_info(user_id="1")
        assert user_info is not None
        assert user_info.name == "John Doe"
        assert user_info.avatar_url == "https://example.com/picture.jpg"
        assert user_info.execution_count is None

    def test_get_with_execution_count(
        self, mock_user_repository: UserRepository, user_service: UserService
    ):
        execution_datetime = datetime.now(timezone.utc) + timedelta(days=1)
        model_user = ModelUser(
            _id="1",
            google_userinfo=GoogleUserInfo(
                id="1",
                name="John Doe",
                family_name="Doe",
                given_name="John",
                picture="https://example.com/picture.jpg",
            ),
            execution_count=ModelExecutionCount(
                total_count=1,
                nearest_execution_datetimes=[execution_datetime],
                remaining_quotas={"ai": []},
            ),
        )
        mock_user_repository.get_by_id.return_value = model_user
        user_info = user_service.get_user_info(user_id="1")
        assert user_info is not None
        assert user_info.name == "John Doe"
        assert user_info.avatar_url == "https://example.com/picture.jpg"
        assert user_info.execution_count is not None
        assert user_info.execution_count.total_count == 1
        assert user_info.execution_count.nearest_execution_datetimes == [
            execution_datetime
        ]
        assert user_info.execution_count.remaining_quotas["ai"] is not None
        assert len(user_info.execution_count.remaining_quotas["ai"]) > 0

    def test_get_with_not_exist_strategy(
        self, mock_user_repository: UserRepository, user_service: UserService
    ):
        execution_datetime = datetime.now(timezone.utc) + timedelta(days=1)
        model_user = ModelUser(
            _id="1",
            google_userinfo=GoogleUserInfo(
                id="1",
                name="John Doe",
                family_name="Doe",
                given_name="John",
                picture="https://example.com/picture.jpg",
            ),
            execution_count=ModelExecutionCount(
                total_count=1,
                nearest_execution_datetimes=[execution_datetime],
                remaining_quotas={"not_exists": []},
            ),
        )
        mock_user_repository.get_by_id.return_value = model_user
        user_info = user_service.get_user_info(user_id="1")
        assert user_info is not None
        assert user_info.name == "John Doe"
        assert user_info.avatar_url == "https://example.com/picture.jpg"
        assert user_info.execution_count is not None
        assert user_info.execution_count.total_count == 1
        assert user_info.execution_count.nearest_execution_datetimes == [
            execution_datetime
        ]
        assert "not_exists" not in user_info.execution_count.remaining_quotas
