from dataclasses import dataclass, field
from traceback import format_exc
from typing import Any, Callable

from services.pipeline.step import Step


@dataclass(kw_only=True)
class Pipeline:
    _steps: list[Step] = field(default_factory=list)

    def through(self, steps: list[Step]):
        self._steps = steps
        return self

    def then(self, destination: Callable):
        def execute_pipeline(passable: Any):
            def next_step(passable: Any, remaining_steps: list[Step], final=False):
                if final or not remaining_steps:
                    return destination(passable)

                current_pipe = remaining_steps[0]
                remaining_steps = remaining_steps[1:]

                try:
                    return current_pipe(
                        passable,
                        lambda passable: next_step(passable, remaining_steps),
                        lambda result=None: next_step(
                            result if result is not None else passable,
                            remaining_steps,
                            True,
                        ),
                    )
                except Exception as e:
                    print(f"Pipeline interrupted due to error: {e}")
                    print(format_exc())
                    return e

            return next_step(passable, list(self._steps))

        return execute_pipeline

    def execute(self):
        return self.then(destination=lambda result: result)
