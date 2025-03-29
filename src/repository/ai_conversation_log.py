from typing import Optional

from bson import ObjectId

from dtos.repository.order_by import OrderBy
from dtos.repository.paginator import Paginator
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

    def get_many_by_executor_id(
        self, executor_id: str, paginator_token: Optional[str] = None
    ) -> tuple[list[AiConversationLog], Paginator]:
        paginator = (
            Paginator.decode(paginator_token=paginator_token)
            if paginator_token is not None
            else Paginator(order_by=OrderBy.DESC, n=self._default_page_size)
        )

        query = {"executor_id": executor_id}
        query.update(paginator.condition)

        raw_documents = list(
            self._table.find(query).sort(paginator.sort).limit(paginator.n)
        )

        return (
            [
                AiConversationLog.model_validate(obj=raw_document)
                for raw_document in raw_documents
            ],
            paginator,
        )

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
