from dataclasses import dataclass

from models.ai.ai_chat_log import ModelAiChatLog
from models.job.job import ModelJob
from services.job.dtos.job_dto import JobDto


@dataclass
class JobDtoTransformer:
    job: ModelJob
    chat_logs: list[ModelAiChatLog]

    def transform(self) -> JobDto:
        chat_log_maps = {chat_log.id: chat_log for chat_log in self.chat_logs}
        chat_logs = [
            chat_log_maps[chat_log_id] for chat_log_id in self.job.chat_log_ids
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
            chat_logs=chat_logs,
        )
