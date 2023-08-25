import uuid
from lib.db import ydbclient


async def create(name: str = 'Test') -> uuid.UUID:
    id = uuid.uuid4()
    await ydbclient.execute(
        'DECLARE $id as String;'
        'DECLARE $name as String;'
        'UPSERT INTO test (id, name) VALUES ($id, $name);',
        {
            'id': str(id),
            'name': name
        }
    )
    return id
