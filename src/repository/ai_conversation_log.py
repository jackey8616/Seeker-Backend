from typing import Optional

from bson import ObjectId

from models.ai.ai_conversation_log import ModelAiConversationLog
from repository import Repository


class AiConversationLogRepository(Repository[ModelAiConversationLog]):
    @property
    def _table_name(self) -> str:
        return "ai_conversation_logs"

    def get_by_executor_id_and_id(
        self, id: str, executor_id: str
    ) -> Optional[ModelAiConversationLog]:
        raw_document = self._table.find_one(
            {
                "_id": ObjectId(id),
                "executor_id": executor_id,
            }
        )
        if raw_document is None:
            return None
        return ModelAiConversationLog.model_validate(obj=raw_document)
