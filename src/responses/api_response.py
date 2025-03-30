from dataclasses import dataclass

from fastapi import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


@dataclass
class ApiResponseDto:
    @property
    def data(self):
        raise NotImplementedError()

    def response(self, status_code: int = 200) -> Response:
        return JSONResponse(
            content=jsonable_encoder(
                {
                    "data": self.data,
                }
            ),
            status_code=status_code,
        )
