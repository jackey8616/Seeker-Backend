from abc import ABC, abstractmethod
from dataclasses import dataclass
from urllib.parse import urlparse

from services.job.crawler.dtos import CrawledJob


@dataclass
class Crawler(ABC):
    link: str

    @property
    def url(self):
        return urlparse(url=self.link)

    @abstractmethod
    def crawl(self) -> CrawledJob | ValueError:
        raise NotImplementedError()
