from pydantic import BaseModel, PrivateAttr

from app.components.config import envs


class RequestGetUserWithCpf(BaseModel):
    _endpoint: str = PrivateAttr(
        default=envs.REGISTRATION_SERVICE_URL + envs.REGISTRATION_GET_USER_ENDPOINT
    )
    _method: str = "get"
