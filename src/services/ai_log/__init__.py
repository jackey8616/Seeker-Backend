from dataclasses import dataclass, field
from typing import Optional

from dtos.ai_log.ai_conversation_log import AiConversationLog as DtoAiConversationLog
from dtos.repository.cursor import Cursor
from models.ai_conversation_log import AiConversationLog as ModelAiConversationLog
from repository.ai_chat_log import AiChatLogRepository
from repository.ai_conversation_log import AiConversationLogRepository


@dataclass
class AiLogService:
    _ai_chat_repository: AiChatLogRepository = field(
        default_factory=lambda: AiChatLogRepository()
    )
    _ai_conversation_log_repository: AiConversationLogRepository = field(
        default_factory=lambda: AiConversationLogRepository()
    )

    def get_many_conversation_log_by_executor_id(
        self, executor_id: str, paginator_token: Optional[str] = None
    ) -> tuple[list[DtoAiConversationLog], Cursor]:
        conversation_logs, paginator = self._ai_conversation_log_repository.get_many(
            query={"executor_id": executor_id},
            paginator_token=paginator_token,
        )

        dto_logs: list[DtoAiConversationLog] = []
        for conversation_log in conversation_logs:
            assert conversation_log.id is not None

            chat_logs = (
                self._ai_chat_repository.get_many_by_conversation_id_and_executor_id(
                    conversation_id=conversation_log.id, executor_id=executor_id
                )
            )
            dto_logs.append(
                DtoAiConversationLog(
                    _id=conversation_log.id,
                    executor_id=conversation_log.executor_id,
                    model_name=conversation_log.model_name,
                    system_instruction=conversation_log.system_instruction,
                    chats=chat_logs,
                    total_input_token=conversation_log.total_input_token,
                    total_output_token=conversation_log.total_output_token,
                    created_at=conversation_log.created_at,
                    updated_at=conversation_log.updated_at,
                )
            )

        cursor = Cursor.from_paginator(
            paginator=paginator, sorted_results=conversation_logs
        )
        return (dto_logs, cursor)

    def get_conversation_log_by_executor_id_and_id(
        self, id: str, executor_id: str
    ) -> Optional[DtoAiConversationLog]:
        conversation_log: Optional[ModelAiConversationLog] = (
            self._ai_conversation_log_repository.get_by_executor_id_and_id(
                id=id, executor_id=executor_id
            )
        )
        if conversation_log is None:
            return None
        assert conversation_log.id is not None

        chat_logs = (
            self._ai_chat_repository.get_many_by_conversation_id_and_executor_id(
                conversation_id=id, executor_id=executor_id
            )
        )
        return DtoAiConversationLog(
            _id=id,
            executor_id=conversation_log.executor_id,
            model_name=conversation_log.model_name,
            system_instruction=conversation_log.system_instruction,
            chats=chat_logs,
            total_input_token=conversation_log.total_input_token,
            total_output_token=conversation_log.total_output_token,
            created_at=conversation_log.created_at,
            updated_at=conversation_log.updated_at,
        )
