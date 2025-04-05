from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

from kink import di

from models.ai.ai_chat_log import ModelAiChatLog
from models.ai.ai_conversation_log import ModelAiConversationLog
from models.user.execution_count import ModelExecutionCount
from models.user.user import ModelUser
from repository.ai_chat_log import AiChatLogRepository
from repository.ai_conversation_log import AiConversationLogRepository
from repository.user import UserRepository
from services.google.vertex import GoogleVertexService
from services.quota.examinator.ai_quota import AiQuotaStrategyExaminator


@dataclass
class AiService:
    _maximum_ai_chat_record_limit: int = field(
        default_factory=lambda: di["MAXIMUM_AI_CHAT_RECORD_LIMIT"]
    )
    _user_repository: UserRepository = field(default_factory=lambda: UserRepository())
    _chat_log_repository: AiChatLogRepository = field(
        default_factory=lambda: AiChatLogRepository()
    )
    _conversation_log_repository: AiConversationLogRepository = field(
        default_factory=lambda: AiConversationLogRepository()
    )

    def start_chat(
        self,
        executor_id: str,
        model_name: str,
        system_instructions: list[str],
    ) -> str:
        executor = self._user_repository.get_by_id(id=executor_id)
        if executor is None:
            raise ValueError("Executor not found")

        strategy_examinator = AiQuotaStrategyExaminator(executor=executor)
        if strategy_examinator.is_exceed():
            raise strategy_examinator.form_quota_error()

        conversation_log = self._conversation_log_repository.insert_one(
            obj=ModelAiConversationLog(
                executor_id=executor_id,
                model_name=model_name,
                system_instruction=system_instructions,
                chat_ids=[],
                total_input_token=0,
                total_output_token=0,
                created_at=datetime.now(tz=timezone.utc),
            )
        )
        assert conversation_log.id is not None

        GoogleVertexService().start_chat(
            model_name=model_name,
            system_instructions=system_instructions,
        )

        return conversation_log.id

    def chat(
        self,
        executor_id: str,
        id: str,
        content: str,
        model_name: Optional[str] = None,
        system_instructions: Optional[list[str]] = None,
        with_history: bool = True,
    ) -> ModelAiChatLog:
        executor = self._user_repository.get_by_id(id=executor_id)
        if executor is None:
            raise ValueError("Executor not found")

        strategy_examinator = AiQuotaStrategyExaminator(executor=executor)
        if strategy_examinator.is_exceed():
            raise strategy_examinator.form_quota_error()

        conversation_log = self._conversation_log_repository.get_by_executor_id_and_id(
            executor_id=executor_id, id=id
        )
        if conversation_log is None:
            raise ValueError("Conversation not exists")
        assert conversation_log.id is not None

        if model_name is not None:
            conversation_log.model_name = model_name
        if system_instructions is not None:
            conversation_log.system_instruction = system_instructions

        conversation_chats = (
            (
                self._chat_log_repository.get_many_by_conversation_id_and_executor_id(
                    conversation_id=conversation_log.id, executor_id=executor_id
                )
            )
            if with_history is True
            else None
        )

        raw_log = GoogleVertexService().chat(
            executor_id=executor_id,
            content=content,
            conversation_log=conversation_log,
            chat_history=conversation_chats,
        )
        chat_log = self._chat_log_repository.insert_one(obj=raw_log)
        self.bump_execution_count(executor=executor)
        assert chat_log.id is not None
        conversation_log.chat_ids.append(chat_log.id)
        conversation_log.total_input_token += chat_log.input_token
        conversation_log.total_output_token += chat_log.output_token
        conversation_log.updated_at = datetime.now(tz=timezone.utc)
        self._conversation_log_repository.update(conversation_log)
        return chat_log

    def evaluate(self, chat_log_id: str, metrics: dict[str, Any]) -> ModelAiChatLog:
        chat_log = self._chat_log_repository.get_by_id(id=chat_log_id)
        if chat_log is None:
            raise ValueError("Chat not exists")
        assert chat_log.id is not None

        chat_log.metrics = metrics
        self._chat_log_repository.update(chat_log)
        return chat_log

    def bump_execution_count(self, executor: ModelUser):
        execution_count = (
            executor.execution_count
            if executor.execution_count
            else ModelExecutionCount()
        )
        strategy_examinator = AiQuotaStrategyExaminator(executor=executor)

        current_time = datetime.now(tz=timezone.utc)
        execution_count.nearest_execution_datetimes.append(current_time)
        execution_count.nearest_execution_datetimes.sort()
        if (
            len(execution_count.nearest_execution_datetimes)
            > self._maximum_ai_chat_record_limit
        ):
            execution_count.nearest_execution_datetimes = (
                execution_count.nearest_execution_datetimes[
                    -1 * self._maximum_ai_chat_record_limit :
                ]
            )
        execution_count.last_execution_datetime = datetime.now(tz=timezone.utc)
        execution_count.total_count += 1
        execution_count.remaining_quotas["ai"] = strategy_examinator.get_quotas()

        executor.execution_count = execution_count
        self._user_repository.update(executor)
