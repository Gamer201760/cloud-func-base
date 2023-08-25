from pydantic import BaseModel

from schemas.req_context import RequestContextScheme


class EventScheme(BaseModel):
    httpMethod: str
    headers: dict
    multiValueHeaders: dict
    queryStringParameters: dict
    multiValueQueryStringParameters: dict
    requestContext: RequestContextScheme
    body: dict = {}
    isBase64Encoded: bool

    class Config:
        orm_mode = True
