from datetime import UTC, datetime
from typing import Optional

from pydantic import BaseModel, Field

from pdl_api.models.person import Person


def utcnow():
    return datetime.now(UTC)


class ErrorResponse(BaseModel):
    type: str = Field(..., description="The type of error")
    message: str = Field(..., description="The error message")


class Response(BaseModel):
    """The response from the API extended with additional data"""

    person: Optional[Person] = Field(
        None, description="The person data, if the response is successful"
    )
    error: Optional[ErrorResponse] = Field(
        None, description="The error response, if an error occurred"
    )
    status: int = Field(..., description="The HTTP status code of the response")
    dataset_version: Optional[str] = Field(
        default=None,
        description="The version of the dataset. Only present in successful responses.",
    )
    likelihood: Optional[int] = Field(
        default=None, description="The likelihood of a match. Only present in successful responses."
    )
    query: dict = Field(default_factory=dict)
    query_time: datetime = Field(default_factory=utcnow)
    additional_data: dict = Field(default_factory=dict)

    def __init__(self, **data):
        """Check whether the response is an error or a person response
        and create the appropriate object.
        From an api request the objects are in "data", if the response is from our data model
        it will be under "person" or "error" keys.
        """
        if "data" in data:
            if "error" in data or "person" in data:
                raise ValueError("Response can't have both 'data' and 'error' or 'person' keys")

            is_person = "status" in data and data["status"] == 200
            p_or_e_key = "person" if is_person else "error"
            data[p_or_e_key] = data.pop("data", {})

        super().__init__(**data)

    @property
    def is_person(self) -> bool:
        return self.person is not None

    @property
    def is_error(self) -> bool:
        return self.error is not None

    @property
    def safe_person(self) -> Person:
        if not self.person:
            raise ValueError("No person data")
        return self.person

    @property
    def safe_error(self) -> ErrorResponse:
        if not self.error:
            raise ValueError("No error data")
        return self.error
