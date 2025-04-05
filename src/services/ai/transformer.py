from dataclasses import dataclass

from dtos.ai.ai_chat_log_dto import AiChatLogDto
from models.ai.ai_chat_log import ModelAiChatLog


@dataclass
class AiChatLogDtoTransformer:
    chat_log: ModelAiChatLog

    def transform(self) -> AiChatLogDto:
        assert self.chat_log.id is not None
        return AiChatLogDto(
            id=self.chat_log.id,
            executor_id=self.chat_log.executor_id,
            conversation_id=self.chat_log.conversation_id,
            input=self.chat_log.input,
            output=self.chat_log.output,
            input_token=self.chat_log.input_token,
            output_token=self.chat_log.output_token,
            start_datetime=self.chat_log.start_datetime,
            end_datetime=self.chat_log.end_datetime,
            metrics=self.chat_log.metrics,
        )
