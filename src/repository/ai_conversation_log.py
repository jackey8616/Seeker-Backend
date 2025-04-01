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

    def update(self, ai_conversation_log: ModelAiConversationLog):
        self._table.find_one_and_update(
            filter={"_id": ObjectId(ai_conversation_log.id)},
            update={
                "$set": ai_conversation_log.model_dump(
                    by_alias=True,
                    exclude={"id"},
                ),
            },
        )
