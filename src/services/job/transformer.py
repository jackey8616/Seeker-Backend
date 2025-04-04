from dataclasses import dataclass

from dtos.job.job_dtos import JobDto
from models.ai.ai_chat_log import ModelAiChatLog
from models.job.job import ModelJob
from services.ai.transformer import AiChatLogDtoTransformer


@dataclass
class JobDtoTransformer:
    job: ModelJob
    chat_logs: list[ModelAiChatLog]

    def transform(self) -> JobDto:
        chat_log_dtos = [
            AiChatLogDtoTransformer(chat_log=chat_log).transform()
            for chat_log in self.chat_logs
        ]

        assert self.job.id is not None
        return JobDto(
            id=self.job.id,
            domain=self.job.domain,
            url=self.job.url,
            title=self.job.title,
            location=self.job.location,
            company=self.job.company,
            salary=self.job.salary,
            work_type=self.job.work_type,
            description=self.job.description,
            raw_description=self.job.raw_description,
            description_hash=self.job.description_hash,
            updated_at=self.job.updated_at,
            created_at=self.job.created_at,
            chat_logs=chat_log_dtos,
        )
