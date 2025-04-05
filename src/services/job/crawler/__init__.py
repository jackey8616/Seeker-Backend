from abc import ABC, abstractmethod
from dataclasses import dataclass
from urllib.parse import urlparse

from dtos.job.crawler_dtos import CrawledJob


@dataclass
class Crawler(ABC):
    link: str

    @property
    def url(self):
        return urlparse(url=self.link)

    @abstractmethod
    def crawl(self) -> CrawledJob | ValueError | RuntimeError:
        raise NotImplementedError()

    @abstractmethod
    def is_crawlable(self, data: str) -> bool:
        raise NotImplementedError()
