
from pydantic import BaseModel, Field
from typing import Optional


class JobRequest(BaseModel):
    job_text: str = Field(
        ...,
        min_length=10,
        max_length=10000
    )

    job_url: Optional[str] = None

    company_name: Optional[str] = None
