from dataclasses import dataclass
from json import loads

from bs4 import BeautifulSoup
from requests import get

from dtos.job.crawler_dtos import CrawledCompany, CrawledJob
from services.job.crawler import Crawler


@dataclass
class CakeMeCrawler(Crawler):
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

            soup = BeautifulSoup(response.text, features="html.parser")
            ssr_data = soup.find(attrs={"id": "__NEXT_DATA__"})
            if ssr_data is None:
                return ValueError(f"SSR data element is None: {url}")
            ssr_data = loads(ssr_data.text)
            job_metadata = ssr_data["props"]["pageProps"]["ssr"]["jobMetaData"]
            page_data = job_metadata["page"]
            job_data = job_metadata["job"]

            title = job_data["title"]

            location_el = soup.find(
                attrs={"class": "JobDescriptionRightColumn_locationsWrapper__N_fz_"}
            )
            if location_el is None:
                return ValueError(f"Location element is None: {url}")
            location = location_el.text

            company = CrawledCompany(
                name=page_data["name"],
                link=f"https://www.cake.me/companies/{page_data['path']}",
            )
            work_type = job_data["remote"]["text"]
            salary = f"{job_data['salary_min']} - {job_data['salary_max']} {job_data['salary_currency']} {job_data['salary_type']}"
            description = job_data["description"]
            raw_description = job_data["description_plain_text"]

            return CrawledJob(
                domain=self.url.hostname or "",
                url=url,
                title=title,
                location=location,
                company=company,
                work_type=work_type,
                salary=salary,
                description=description,
                raw_description=raw_description,
            )
        except Exception as e:
            return RuntimeError(
                f"Failed to crawl data from given link {self.url.geturl()}: {e}"
            )

    def is_crawlable(self, data: str) -> bool:
        return True
