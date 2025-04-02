from pydantic import BaseModel


class JobFittingAiByUrlRequestDto(BaseModel):
    url: str
    restriction: str
    resume: str
