from models import MongoDocument
from services.job.dtos import Company


class Job(MongoDocument):
    domain: str
    url: str
    title: str
    location: str
    company: Company
    salary: str
    work_type: str
    description: str
    description_hash: str
