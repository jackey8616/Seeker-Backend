from dataclasses import dataclass

from responses.api_response import ApiResponseDto


@dataclass
class JobFittingAiByUrlResponseDto(ApiResponseDto):
    job_id: str
    chat_log_id: str
    link: str
    ai_response: str

    @property
    def data(self):
        return {
            "job_id": self.job_id,
            "chat_log_id": self.chat_log_id,
            "link": self.link,
            "ai_response": self.ai_response,
        }
