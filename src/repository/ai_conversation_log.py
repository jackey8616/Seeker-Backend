from bson import ObjectId

from models.ai_conversation_log import AiConversationLog
from repository import Repository


class AiConversationLogRepository(Repository[AiConversationLog]):
    @property
    def _table_name(self) -> str:
        return "ai_conversation_logs"

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
