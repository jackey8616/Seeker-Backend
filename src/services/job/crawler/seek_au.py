from dataclasses import dataclass
from json import dumps, loads
from re import findall, search
from typing import Optional

from bs4 import BeautifulSoup, Tag
from requests import get

from services.job.crawler import Crawler
from services.job.crawler.dtos import CrawledCompany, CrawledJob


@dataclass
class SeekAuCrawler(Crawler):
    def crawl(self) -> CrawledJob | ValueError | RuntimeError:
        try:
            url = self.url.geturl()
            response = get(
                url=url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                },
            )
            if response.status_code == 404:
                return ValueError(f"The job's link is missing with 404: {url}")

            response.raise_for_status()

            if not self.is_crawlable(data=response.text):
                return ValueError(f"The job is no longer advertised: {url}")

            company_link = self._extract_company_link(raw_html=response.text)
            if isinstance(company_link, ValueError):
                return company_link

            soup = BeautifulSoup(response.text, features="html.parser")
            title_el = soup.find(attrs={"data-automation": "job-detail-title"})
            if title_el is None:
                return ValueError(f"Title element is None: {url}")
            title = title_el.text
            company_name_el = soup.find(attrs={"data-automation": "advertiser-name"})
            if company_name_el is None:
                return ValueError(f"CompanyName element is None: {url}")
            company_name = company_name_el.text
            company = CrawledCompany(
                name=company_name,
                link=company_link,
            )
            location_el = soup.find(attrs={"data-automation": "job-detail-location"})
            if location_el is None:
                return ValueError(f"Location element is None: {url}")
            location = location_el.text
            work_type_el = soup.find(attrs={"data-automation": "job-detail-work-type"})
            if work_type_el is None:
                return ValueError(f"WorkType element is None: {url}")
            work_type = work_type_el.text
            salary_el = soup.find(attrs={"data-automation": "job-detail-salary"})
            expected_salary_el = soup.find(
                attrs={"data-automation": "job-detail-add-expected-salary"}
            )
            detail_salary_el = salary_el or expected_salary_el
            if detail_salary_el is None:
                return ValueError(f"Salary and ExpectedSalary element are None: {url}")
            salary = detail_salary_el.text
            details_el = soup.find(attrs={"data-automation": "jobAdDetails"})
            if details_el is None:
                return ValueError(f"Details element is None: {url}")
            assert isinstance(details_el, Tag)
            raw_details = details_el.decode_contents()
            details = details_el.text

            return CrawledJob(
                domain=self.url.hostname or "",
                url=url,
                title=title,
                location=location,
                company=company,
                work_type=work_type,
                salary=salary,
                description=details,
                raw_description=raw_details,
            )
        except Exception as e:
            return RuntimeError(
                f"Failed to crawl data from given link {self.url.geturl()}: {e}"
            )

    def is_crawlable(self, data: str) -> bool:
        return "This job is no longer advertised" not in data

    def _extract_company_link(self, raw_html: str) -> Optional[str] | ValueError:
        link = self.url.geturl()
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
            company_link = f"{self.url.scheme}://{self.url.hostname}/companies/{company_profile['companyNameSlug']}/"
        return company_link
