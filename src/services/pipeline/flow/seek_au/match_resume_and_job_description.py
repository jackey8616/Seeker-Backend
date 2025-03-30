from dataclasses import dataclass
from re import DOTALL, search
from typing import Any

from rouge import Rouge

from models.ai_chat_log import ModelAiChatLog
from services.google.vertex import GoogleVertexService
from services.job.repository import JobRepository
from services.pipeline.step import FinalStep, NextStep, Step, StepDataType


class MatchResumeAndJobDescriptionDataType(StepDataType):
    executor_id: str
    resume: str
    restriction: str
    job_ids: list[str]


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
        job_ids = data.job_ids

        vertex_service = GoogleVertexService()
        conversation_id = vertex_service.start_chat(
            executor_id=executor_id,
            model_name="gemini-1.5-pro",
            system_instructions=[
                "You are a professional job matcher",
                "You will be given a resume, some job hunting restrictions and a series of job descriptions,"
                "follow the format and output a short summarize of given job description and comment on the suitability of the resume, restrictions and job description.",
                "last score a positive number(max 100, min 0) of the fit rate.",
                "Here is the resume and restrictions:",
                f"<RESUME>{resume}</RESUME>",
                f"<RESTRICTIONS>{restriction}</RESTRICTIONS>",
                "<FORMAT>",
                "# Summarize",
                "<summarize>... this is job summarize wrap in summarize tag ...</summarize>",
                "",
                "# Suitability Assessment",
                "<positive-comment>... Positive comment wrap in positive-comment tag ...</positive-comment>",
                "<negative-comment>... Negative comment wrap in negative-comment tag...</negative-comment>",
                "",
                "# Fit Rate",
                "N/100 (N is number from 0 up to 100, if you can't rate, just set N to 0)",
                "</FORMAT>",
            ],
        )

        job_repository = JobRepository()
        fitting_results = []
        for id in job_ids:
            job = job_repository.get_by_id(id=id)
            if job is None:
                continue
            assert job.id is not None

            job_description = job.description
            chat_log = vertex_service.chat(
                executor_id=executor_id,
                id=conversation_id,
                content=f"<JOB_DESCRIPTION>{job.description}</JOB_DESCRIPTION>",
                with_history=False,
            )
            assert chat_log.id is not None
            vertex_service.evaluate(
                chat_log.id, self._evaluate_summarize(job_description, chat_log)
            )

            # Link the ChatLog ID with the Job
            job.chat_log_ids.append(chat_log.id)
            job_repository.update(job)

            fitting_results.append(
                {
                    "link": job.url,
                    "response": chat_log.output,
                }
            )

        pass_data = data.model_dump() | {"fitting_result": fitting_results}

        return next(pass_data)

    def _evaluate_summarize(
        self, input: str, chat_log: ModelAiChatLog
    ) -> dict[str, Any]:
        output = search(r"<summarize>([\s\S]*?)<\/summarize>", chat_log.output, DOTALL)
        if output is None:
            raise ValueError("AI generated content missing <summarize> tag.")

        rouge_score = Rouge().get_scores(input, output.group(1))[0]

        return {"rouge": rouge_score}
