from bson import ObjectId

from models.ai_chat_log import ModelAiChatLog
from repository import Repository


class AiChatLogRepository(Repository[ModelAiChatLog]):
    @property
    def _table_name(self) -> str:
        return "ai_chat_logs"

    def get_many_by_conversation_id_and_executor_id(
        self, conversation_id: str, executor_id: str
    ) -> list[ModelAiChatLog]:
        raw_documents = self._table.find(
            {"conversation_id": conversation_id, "executor_id": executor_id}
        )
        return [
            ModelAiChatLog.model_validate(obj=raw_document)
            for raw_document in raw_documents
        ]

    def get_many_by_ids(self, ids: list[str], executor_id: str) -> list[ModelAiChatLog]:
        raw_documents = self._table.find(
            {"_id": {"$in": [ObjectId(id) for id in ids]}, "executor_id": executor_id}
        )
        return [
            ModelAiChatLog.model_validate(obj=raw_document)
            for raw_document in raw_documents
        ]

    def update(self, ai_chat_log: ModelAiChatLog):
        self._table.find_one_and_update(
            filter={"_id": ObjectId(ai_chat_log.id)},
            update={
                "$set": ai_chat_log.model_dump(
                    by_alias=True,
                    exclude={"id"},
                ),
            },
        )
