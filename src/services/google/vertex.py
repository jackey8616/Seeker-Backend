from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from kink import di
from vertexai import init
from vertexai.generative_models import Content, GenerativeModel, Part

from dtos.google.vertex import AiChatLog
from models.ai_conversation_log import AiConversationLog
from repository.ai_conversation_log import AiConversationLogRepository


@dataclass
class GoogleVertexService:
    _log_repository: AiConversationLogRepository = field(
        default_factory=lambda: AiConversationLogRepository()
    )

    def __post_init__(self):
        init(project=di["GOOGLE_GCP_PROJECT_ID"], location=di["GOOGLE_GCP_REGION"])

    def start_chat(
        self,
        executor_id: str,
        model_name: str,
        system_instructions: list[str],
    ) -> str:
        model = GenerativeModel(
            model_name=model_name,
            system_instruction=[
                Part.from_text(instruction) for instruction in system_instructions
            ],
        )
        model.start_chat()
        conversation_log = self._log_repository.insert_one(
            obj=AiConversationLog(
                executor_id=executor_id,
                model_name=model_name,
                system_instruction=system_instructions,
                chats=[],
                total_input_token=0,
                total_output_token=0,
                created_at=datetime.now(tz=timezone.utc),
            )
        )
        assert conversation_log.id is not None
        return conversation_log.id

    def chat(
        self,
        executor_id: str,
        id: str,
        content: str,
        model_name: Optional[str] = None,
        system_instructions: Optional[list[str]] = None,
        with_history: bool = True,
    ) -> AiChatLog:
        conversation_log = self._log_repository.get_by_executor_id_and_id(
            executor_id=executor_id, id=id
        )
        if conversation_log is None:
            raise ValueError("Conversation not exists")

        if model_name is not None:
            conversation_log.model_name = model_name
        if system_instructions is not None:
            conversation_log.system_instruction = system_instructions

        model = GenerativeModel(
            model_name=conversation_log.model_name,
            system_instruction=[
                Part.from_text(instruction)
                for instruction in conversation_log.system_instruction
            ],
        )
        history = []
        if with_history is True:
            for chat in conversation_log.chats:
                history.append(
                    Content.from_dict(
                        {
                            "role": "user",
                            "parts": [Part.from_text(chat.input).to_dict()],
                        }
                    )
                )
                history.append(
                    Content.from_dict(
                        {
                            "role": "model",
                            "parts": [Part.from_text(chat.output).to_dict()],
                        }
                    )
                )
        chat_instance = model.start_chat(history=history)

        start_datetime = datetime.now(tz=timezone.utc)
        response = chat_instance.send_message(content=Part.from_text(text=content))
        candidates = response.candidates
        usage_metadata = response.usage_metadata
        end_datetime = datetime.now(tz=timezone.utc)
        chat_log = AiChatLog(
            input=content,
            output=candidates.pop().content.parts.pop().text,
            input_token=usage_metadata.prompt_token_count,
            output_token=usage_metadata.candidates_token_count,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )
        conversation_log.chats.append(chat_log)
        conversation_log.total_input_token += chat_log.input_token
        conversation_log.total_output_token += chat_log.output_token
        conversation_log.updated_at = datetime.now(tz=timezone.utc)
        self._log_repository.update(conversation_log)
        return chat_log
