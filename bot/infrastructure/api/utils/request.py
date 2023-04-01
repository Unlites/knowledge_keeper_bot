import requests
from http import HTTPStatus
from bot.infrastructure.api.errors import KnowledgeKeeperAPIConnectionError
from bot.infrastructure.api.errors import KnowledgeKeeperAPIError
from bot.infrastructure.api.errors import UnauthorizedError


def do_request(
    method,
    url,
    body=None,
    params=None,
    headers=None,
) -> dict | None:
    try:
        response = requests.request(
            method,
            url,
            data=body,
            headers=headers,
            params=params,
        )

        data = response.json()["data"]
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            raise UnauthorizedError
        elif response.status_code != HTTPStatus.OK:
            raise KnowledgeKeeperAPIError(data)

        return data
    except ConnectionError as e:
        raise KnowledgeKeeperAPIConnectionError(e)
