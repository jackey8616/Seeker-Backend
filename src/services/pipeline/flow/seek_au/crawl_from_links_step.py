from dataclasses import dataclass
from json import dumps, loads
from re import findall, search
from typing import Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString, PageElement
from pydantic import BaseModel
from requests import get

from services.pipeline.step import FinalStep, NextStep, Step, StepDataType

type OneElement = PageElement | Tag | NavigableString


class CrawlDetailCompany(BaseModel):
    name: str
    link: Optional[str]


class CrawlDetail(BaseModel):
    link: str
    title: str
    company: CrawlDetailCompany
    location: str
    work_type: str
    salary: str
    details: str


class CrawlFromLinksDataType(StepDataType):
    links: list[str]


@dataclass
class CrawlFromLinksStep(Step[CrawlFromLinksDataType]):
    def perform(self, data: CrawlFromLinksDataType, next: NextStep, final: FinalStep):
        links = data.links

        crawled_details: list[CrawlDetail] = [
            self._crawl_from_link(link=link) for link in links
        ]

        pass_data = data.model_dump() | {
            "crawled_details": crawled_details,
        }
        return next(pass_data)

    def _crawl_from_link(self, link: str) -> CrawlDetail:
        response = get(url=link)
        response.raise_for_status()

        company_link = self._extract_company_link(raw_html=response.text, link=link)
        if isinstance(company_link, Exception):
            raise company_link

        soup = BeautifulSoup(response.text, features="html.parser")
        title = self._soup_get(
            soup=soup, attrs={"data-automation": "job-detail-title"}
        ).text
        company = CrawlDetailCompany(
            name=self._soup_get(
                soup=soup, attrs={"data-automation": "advertiser-name"}
            ).text,
            link=company_link,
        )
        location = self._soup_get(
            soup=soup, attrs={"data-automation": "job-detail-location"}
        ).text
        work_type = self._soup_get(
            soup=soup, attrs={"data-automation": "job-detail-work-type"}
        ).text
        salary = self._soup_get(
            soup=soup, attrs={"data-automation": "job-detail-salary"}
        ).text
        details = self._soup_get(
            soup=soup, attrs={"data-automation": "jobAdDetails"}
        ).text

        return CrawlDetail(
            link=link,
            title=title,
            company=company,
            location=location,
            work_type=work_type,
            salary=salary,
            details=details,
        )

    def _soup_get(self, soup: BeautifulSoup, attrs: dict) -> OneElement:
        el = soup.find(attrs=attrs)
        assert el is not None

        return el

    def _extract_company_link(
        self, raw_html: str, link: str
    ) -> Optional[str] | Exception:
        url = urlparse(link)
        searched_data = search(r"window\.SEEK_APOLLO_DATA = (.*?)\n", raw_html)
        if searched_data is None:
            return ValueError(f"Unable to crawl data from given link {link}")

        data = loads(searched_data.group(1)[:-1])

        job_id = findall(r"\d+", link).pop()
        job_index = dumps({"id": job_id}).replace(" ", "")

        root = data["ROOT_QUERY"]
        job_detail = root[f"jobDetails:{job_index}"]
        job = job_detail["job"]
        zone = {"zone": job["sourceZone"]}
        zone_index = dumps(zone).replace(" ", "")

        company_profile_name = job_detail[f"companyProfile({zone_index})"]
        company_link = None
        if company_profile_name is not None:
            company_profile = data[company_profile_name["__ref"]]
            company_link = f"{url.scheme}://{url.hostname}/companies/{company_profile['companyNameSlug']}/"
        return company_link
