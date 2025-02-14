from abc import ABC, abstractmethod
from typing import Any, Callable, cast, get_args

from pydantic import BaseModel, ConfigDict, TypeAdapter

type NextStep = Callable[[Any]]
type FinalStep = Callable[[Any | Exception | None]]


class StepDataType(BaseModel):
    model_config = ConfigDict(extra="allow")


class Step[T](ABC):
    def __call__(self, passable: dict, next: NextStep, final: FinalStep):
        data = self.validate(passable)
        return self.perform(data, next, final)

    def validate(self, passable: dict):
        origin_bases = cast(list, getattr(self, "__orig_bases__")) or []  # noqa: B009
        generic_types = get_args(origin_bases[0])
        generic_type = generic_types[0]
        return TypeAdapter(type=generic_type).validate_python(passable)

    @abstractmethod
    def perform(self, data: T, next: NextStep, final: FinalStep):
        raise NotImplementedError()
