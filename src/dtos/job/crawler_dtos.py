from typing import Optional

from pydantic import BaseModel


class CrawledCompany(BaseModel):
    name: str
    link: Optional[str]


class CrawledJob(BaseModel):
    domain: str
    url: str
    title: str
    location: str
    company: CrawledCompany
    work_type: str
    salary: str
    description: str
    raw_description: str
