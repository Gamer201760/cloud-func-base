from schemas.response import Response, ErrorResponse, \
    JsonResponse
from schemas.event import EventScheme
from lib.db import ydbclient
import ydb
from crud import create


async def main(event: EventScheme) -> Response:
    print(event)
    try:
        await ydbclient.connect()
        id = await create(event.body.get('name', 'Test'))
        return JsonResponse({
            'id': id
        }, 201)
    except ydb.Error:
        return ErrorResponse('Database error')


async def handler(event, context) -> dict:
    data = EventScheme.model_validate(event)
    payload = await main(data)
    return payload.to_dict()
