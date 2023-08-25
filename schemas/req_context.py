from pydantic import BaseModel


class RequestContextScheme(BaseModel):
    httpMethod: str
    requestId: str
    authorizer: dict | None = None
