from pytest import fixture
from pytest_mock import MockerFixture

from repository.user import UserRepository
from services.user import UserService
from tests.unit import UnitTestCase


class UnitTestUserService(UnitTestCase):
    @fixture
    def mock_user_repository(self, mocker: MockerFixture) -> UserRepository:
        return mocker.Mock(spec=UserRepository)

    @fixture
    def user_service(self, mock_user_repository: UserRepository) -> UserService:
        return UserService(_user_repository=mock_user_repository)
