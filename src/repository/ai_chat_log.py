from bson import ObjectId

from models.ai.ai_chat_log import ModelAiChatLog
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
