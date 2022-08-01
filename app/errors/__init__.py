from typing import Optional, Union

from fastapi import HTTPException


class NotFoundError(HTTPException):

    def __init__(
            self,
            _,
            message: Optional[str] = "Not found"
    ) -> None:
        super().__init__(
            status_code=404,
            detail=dict(
                code=404,
                message=message
            )
        )


class UnexpectedError(HTTPException):

    def __init__(
            self,
            _,
            code: int = 400,
            message: Union[Optional[str], Optional[dict]] = "Unexpected error"
    ) -> None:
        HTTPException.__init__(
            self,
            status_code=code,
            detail=dict(
                code=code,
                message=message,
            )
        )
