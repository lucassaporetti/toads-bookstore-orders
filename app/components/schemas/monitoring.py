from pydantic import BaseModel, Field


class Healthz(BaseModel):
    message: str = Field("ok", description="response ok to health status")
