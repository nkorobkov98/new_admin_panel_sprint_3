import logging
import os
from typing import Optional

import elasticsearch.client.indices
from elasticsearch import Elasticsearch, helpers

from backoff import backoff
from http import HTTPStatus

logger = logging.getLogger(__name__)


class Connection:
    def __init__(self, connection: Elasticsearch):
        self._connection = connection

    def create_index(self, index_name: str, schema: dict):
        logging.info(
            f"Creating index {index_name} with the following schema:{schema}"
        )
        res = self._connection.indices.create(index=index_name, ignore=HTTPStatus.BAD_REQUEST,
                                              body=schema)
        logger.info(f"Result: {res}")

    def post(
            self,
            data: dict,
            identifier: Optional[str],
            index: str = "movies"
    ):
        """
        Send document to the corresponding mapping.

            Warning:
                If repeat this action with the same parameters, the mapping
                 entry will increment '_version' and result be 'updated'
        """
        resp = self._connection.index(
            index=index,
            id=identifier,
            document=data
        )
        logger.debug(resp["result"])

    def post_bulk(self, data: list[dict], index: str = "movies"):
        actions = [
            {
                "_id": d["id"],
                **d
            }
            for d in data
        ]
        result = helpers.bulk(self._connection, actions, index=index)
        logger.debug(result)

    def delete_bulk(self, data: list[str], index: str = "movies"):
        actions = [
            {
                '_op_type': 'delete',
                "_id": str(d),
            }
            for d in data
        ]
        result = helpers.bulk(self._connection, actions, index=index)
        logger.debug(result)

    def is_exist(self, index_name: str) -> bool:
        index = elasticsearch.client.indices.IndicesClient(self._connection)
        return index.exists(index=index_name)


@backoff([ConnectionError, ConnectionRefusedError, ])
def create_connection() -> Connection:
    connection = Elasticsearch(
        [os.environ.get("ES_HOST")],
        port=int(os.environ.get("ES_PORT"))
    )
    if connection.ping():
        return Connection(connection)
    raise ConnectionError
