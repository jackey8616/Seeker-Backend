from dataclasses import dataclass
from typing import ClassVar, Mapping, Optional, Type
from urllib.parse import urlparse

from services.job.crawler import Crawler
from services.job.crawler.seek_au import SeekAuCrawler


@dataclass
class CrawlerFactory:
    mapping: ClassVar[Mapping[str, Type[Crawler]]] = {
        "www.seek.com.au": SeekAuCrawler,
    }

    @staticmethod
    def get_crawler(link: str) -> Optional[Crawler]:
        url = urlparse(link)
        if url.hostname is None:
            return None

        crawler_clazz = CrawlerFactory.mapping[url.hostname]
        return None if crawler_clazz is None else crawler_clazz(link=link)
