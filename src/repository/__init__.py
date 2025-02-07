from kink import di
from pymongo import MongoClient
from pymongo.collection import Collection


class Repository:
    @property
    def _table_name(self) -> str:
        raise NotImplementedError()

    @property
    def _client(self):
        return MongoClient(di["MONGODB_ENDPOINT"])

    @property
    def _table(self) -> Collection:
        return self._client.get_database(name=di["MONGODB_DATABASE"]).get_collection(
            name=self._table_name
        )
