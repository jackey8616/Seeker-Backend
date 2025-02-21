from typing import Optional
from urllib.parse import urlparse

from services.job.crawler import Crawler
from services.job.crawler.seek_au import SeekAuCrawler


class CrawlerFactory:
    @staticmethod
    def get_crawler(link: str) -> Optional[Crawler]:
        url = urlparse(link)
        match url.hostname:
            case "www.seek.com.au":
                return SeekAuCrawler(link=link)
            case _:
                return None
