from pydantic import BaseModel


class CrawlJobRequestDto(BaseModel):
    url: str
