from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from kink import di
from vertexai import init
from vertexai.generative_models import Content, GenerativeModel, Part

from models.ai.ai_chat_log import ModelAiChatLog
from models.ai.ai_conversation_log import ModelAiConversationLog


@dataclass
class GoogleVertexService:
    def __post_init__(self):
        init(project=di["GOOGLE_GCP_PROJECT_ID"], location=di["GOOGLE_GCP_REGION"])

    def start_chat(
        self,
        model_name: str,
        system_instructions: list[str],
    ) -> None:
        model = GenerativeModel(
            model_name=model_name,
            system_instruction=[
                Part.from_text(instruction) for instruction in system_instructions
            ],
        )
        model.start_chat()

    def chat(
        self,
        executor_id: str,
        content: str,
        conversation_log: ModelAiConversationLog,
        chat_history: Optional[list[ModelAiChatLog]] = None,
    ) -> ModelAiChatLog:
        assert conversation_log.id is not None
        model = GenerativeModel(
            model_name=conversation_log.model_name,
            system_instruction=[
                Part.from_text(instruction)
                for instruction in conversation_log.system_instruction
            ],
        )
        history = []
        if chat_history is not None:
            for chat in chat_history:
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
        return ModelAiChatLog(
            executor_id=executor_id,
            conversation_id=conversation_log.id,
            input=content,
            output=candidates.pop().content.parts.pop().text,
            input_token=usage_metadata.prompt_token_count,
            output_token=usage_metadata.candidates_token_count,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )
