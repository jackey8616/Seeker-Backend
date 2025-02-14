from dataclasses import dataclass

from services.google.vertex import GoogleVertexService
from services.pipeline.flow.seek_au.crawl_from_links_step import CrawlDetail
from services.pipeline.step import FinalStep, NextStep, Step, StepDataType


class MatchResumeAndJobDescriptionDataType(StepDataType):
    executor_id: str
    resume: str
    restriction: str
    crawled_details: list[CrawlDetail]


@dataclass
class MatchResumeAndJobDescriptionStep(Step[MatchResumeAndJobDescriptionDataType]):
    def perform(
        self,
        data: MatchResumeAndJobDescriptionDataType,
        next: NextStep,
        final: FinalStep,
    ):
        executor_id = data.executor_id
        resume = data.resume
        restriction = data.restriction
        crawled_details = data.crawled_details

        vertex_service = GoogleVertexService()
        conversation_id = vertex_service.start_chat(
            executor_id=executor_id,
            model_name="gemini-1.5-pro",
            system_instructions=[
                "You are a professional job matcher",
                "You will be given a resume, some job hunting restrictions and a series of job descriptions,"
                "follow the format and output a short summarize of given job description and comment the fitness of resume, restrictions and job description,"
                "last score a positive number(max 100, min 0) of the fitness.",
                "Here is the resume and restrictions:",
                f"<RESUME>{resume}</RESUME>",
                f"<RESTRICTIONS>{restriction}</RESTRICTIONS",
                """
                <FORMAT>
                # Job Summarize
                ... this is job summarize ...

                # Fitness
                ... Positive comment ...
                ... Negative comment ...

                # Fitness Score
                N/100 (N is positive number from 0 up to 100)
                </FORMAT>""",
            ],
        )

        job_fitnesses = []
        for detail in crawled_details:
            job_description = detail.model_dump()
            chat_log = vertex_service.chat(
                executor_id=executor_id,
                id=conversation_id,
                content=f"<JOB_DESCRIPTION>{job_description}</JOB_DESCRIPTION>",
                with_history=False,
            )
            job_fitnesses.append(
                {
                    "link": detail.link,
                    "response": chat_log.output,
                }
            )

        pass_data = data.model_dump() | {"fitnesses": job_fitnesses}

        return next(pass_data)
