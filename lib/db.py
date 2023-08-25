import ydb
import os

endpoint = os.getenv("YDB_ENDPOINT", 'grpc://localhost:2136')
database = os.getenv("YDB_DATABASE", "/local")


class YDBClient:
    def __init__(self, endpoint: str, database: str) -> None:
        self.endpoint = endpoint
        self.database = database

        self.driver = ydb.aio.Driver(
            endpoint=endpoint,
            database=database,
            credentials=ydb.credentials_from_env_variables()
        )

        self.pool = ydb.aio.SessionPool(self.driver, size=10)

    async def connect(self):
        await self.driver.wait(timeout=10)

    def getDriver(self) -> ydb.aio.Driver:
        return self.driver

    def getPool(self) -> ydb.aio.SessionPool:
        return self.pool

    async def execute(self, query: str, parametrs: dict) -> list[dict] | None:
        return await self.pool.retry_operation(
            self.transaction,
            query,
            parametrs
        )

    async def transaction(
        self,
        session: ydb.Session,
        query: str,
        payload: dict
    ) -> list[dict] | None:
        parametrs = self._transform_payload(payload)
        header = f'PRAGMA TablePathPrefix("{self.database}");\n'
        prepare: ydb.DataQuery = await session.prepare(header + query)
        data = await session.transaction(ydb.SerializableReadWrite()).execute(
            prepare,
            parametrs,
            commit_tx=True,
        )
        if len(data) == 0:
            return None

        if len(data[-1].rows) == 0:
            return None

        return data[-1].rows

    def _transform_payload(self, payload: dict) -> dict:
        return {'$' + key: value.encode() if isinstance(value, str)
                else value for key, value in payload.items()}


ydbclient = YDBClient(endpoint, database)
