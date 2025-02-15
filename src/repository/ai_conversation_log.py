from typing import Optional

from bson import ObjectId

from models.ai_conversation_log import AiConversationLog
from repository import Repository


class AiConversationLogRepository(Repository[AiConversationLog]):
    @property
    def _table_name(self) -> str:
        return "ai_conversation_logs"

    def get_by_executor_id_and_id(
        self, id: str, executor_id: str
    ) -> Optional[AiConversationLog]:
        raw_document = self._table.find_one(
            {
                "_id": ObjectId(id),
                "executor_id": executor_id,
            }
        )
        if raw_document is None:
            return None
        return AiConversationLog.model_validate(obj=raw_document)

    def get_many_by_executor_id(self, executor_id: str) -> list[AiConversationLog]:
        raw_documents = self._table.find({"executor_id": executor_id})
        return [
            AiConversationLog.model_validate(obj=raw_document)
            for raw_document in raw_documents
        ]

    def update(self, ai_conversation_log: AiConversationLog):
        self._table.find_one_and_update(
            filter={"_id": ObjectId(ai_conversation_log.id)},
            update={
                "$set": ai_conversation_log.model_dump(
                    by_alias=True,
                    exclude={"id"},
                ),
            },
        )
