from dataclasses import dataclass
from json import dumps, loads
from re import findall, search
from typing import Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from pydantic import BaseModel
from requests import get

from services.pipeline.step import FinalStep, NextStep, Step, StepDataType


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
        title_el = soup.find(attrs={"data-automation": "job-detail-title"})
        if title_el is None:
            raise ValueError("Title element is None")
        title = title_el.text
        company_name_el = soup.find(attrs={"data-automation": "advertiser-name"})
        if company_name_el is None:
            raise ValueError("CompanyName element is None")
        company_name = company_name_el.text
        company = CrawlDetailCompany(
            name=company_name,
            link=company_link,
        )
        location_el = soup.find(attrs={"data-automation": "job-detail-location"})
        if location_el is None:
            raise ValueError("Location element is None")
        location = location_el.text
        work_type_el = soup.find(attrs={"data-automation": "job-detail-work-type"})
        if work_type_el is None:
            raise ValueError("WorkType element is None")
        work_type = work_type_el.text
        salary_el = soup.find(attrs={"data-automation": "job-detail-salary"})
        expected_salary_el = soup.find(
            attrs={"data-automation": "job-detail-add-expected-salary"}
        )
        detail_salary_el = salary_el or expected_salary_el
        if detail_salary_el is None:
            raise ValueError("Salary and ExpectedSalary element are None")
        salary = detail_salary_el.text
        details_el = soup.find(attrs={"data-automation": "jobAdDetails"})
        if details_el is None:
            raise ValueError("Details element is None")
        details = details_el.text

        return CrawlDetail(
            link=link,
            title=title,
            company=company,
            location=location,
            work_type=work_type,
            salary=salary,
            details=details,
        )

    def _extract_company_link(
        self, raw_html: str, link: str
    ) -> Optional[str] | Exception:
        url = urlparse(link)
        app_config = search(r"window\.SEEK_APP_CONFIG = (.*?)\n", raw_html)
        if app_config is None:
            return ValueError(
                f"Unable to crawl data from given link {link}: missing SEEK_APP_CONFIG"
            )
        config_data = loads(app_config.group(1)[:-1])
        source_zone = config_data["zone"]

        searched_data = search(r"window\.SEEK_APOLLO_DATA = (.*?)\n", raw_html)
        if searched_data is None:
            return ValueError(
                f"Unable to crawl data from given link {link}: missing SEEK_APOLLO_DATA"
            )

        data = loads(searched_data.group(1)[:-1])

        job_id = findall(r"\d+", link).pop()
        job_index = dumps({"id": job_id}).replace(" ", "")

        root = data["ROOT_QUERY"]
        job_detail = root[f"jobDetails:{job_index}"]
        zone = {"zone": source_zone}
        zone_index = dumps(zone).replace(" ", "")

        company_profile_name = job_detail[f"companyProfile({zone_index})"]
        company_link = None
        if company_profile_name is not None:
            company_profile = data[company_profile_name["__ref"]]
            company_link = f"{url.scheme}://{url.hostname}/companies/{company_profile['companyNameSlug']}/"
        return company_link
