from dataclasses import dataclass

from dtos.responses.job import JobDto
from models.ai_chat_log import AiChatLog
from services.job.models import Job


@dataclass
class JobDtoTransformer:
    job: Job
    chat_logs: list[AiChatLog]

    def transform(self) -> JobDto:
        chat_log_maps = {chat_log.id: chat_log for chat_log in self.chat_logs}
        chat_logs = [
            chat_log_maps[chat_log_id] for chat_log_id in self.job.chat_log_ids
        ]
        return JobDto(
            domain=self.job.domain,
            url=self.job.url,
            title=self.job.title,
            location=self.job.location,
            company=self.job.company,
            salary=self.job.salary,
            work_type=self.job.work_type,
            description=self.job.description,
            description_hash=self.job.description_hash,
            updated_at=self.job.updated_at,
            created_at=self.job.created_at,
            chat_logs=chat_logs,
        )
