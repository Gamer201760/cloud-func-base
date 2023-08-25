class Response:
    status_code: int = 200
    headers: dict = {
        'Content-type': 'application/json'
    }
    body: dict = {}

    def to_dict(self) -> dict:
        return dict(
            status_code=self.status_code,
            headers=self.headers,
            body=self.body
        )


class CreatedResponse(Response):
    status_code = 201


class BadRequest(Response):
    status_code = 400


class ErrorResponse(Response):
    def __init__(self, msg: str = 'Error', code: int = 404) -> None:
        self.body['detail'] = msg
        self.status_code = code


class JsonResponse(Response):
    def __init__(self, body: dict, code: int = 200) -> None:
        self.body = body
        self.status_code = code
