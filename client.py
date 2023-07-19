from __future__ import annotations

import aiohttp
import requests

from config import Environment, Configuration


class StatusChangeResult:
    def __init__(self, info: str, succeed: bool = False):
        self.succeed = succeed
        self.info = info


class StatusChangeModel:
    def __init__(self, mid: str, id_item: str, market: str, status: str, status_reason: str | None = None):
        self.mid = mid
        self.id_item = id_item
        self.market = market
        self.status = status
        self.status_reason = status_reason

    def to_json(self) -> dict[str, str | None]:
        return {'status': self.status, 'statusReason': self.status_reason, 'market': self.market.upper()}


class BaseClient:
    def __init__(self, env: Environment, config: Configuration):
        self.auth_token: str = None
        self.__env = env
        self.__config = config
        self.base_url: str = config.pim_url(env)
        self.timeout = aiohttp.ClientTimeout(total=config.api_timeout())
        self.__init_token()

    async def send_patch(self, uri: str, json_body: dict, re_init_token: bool = False):
        if re_init_token:
            self.__init_token()

        url = f'{self.base_url}/{uri}'
        headers = {'Content-Type': 'application/json', 'Authorization': self.auth_token}

        async with aiohttp.ClientSession(headers=headers, timeout=self.timeout) as session:
            async with session.patch(url, json=json_body) as response:
                await response.read()

                return response

    def __init_token(self) -> None:
        url = f'{self.__config.ims_url(self.__env)}/{self.__config.auth_uri()}'
        headers = {'Content-Type': 'application/json'}
        body = {'username': self.__config.auth_user(), 'password': self.__config.auth_password()}

        retries = 3
        while retries > 0:
            response = requests.post(url, json=body, headers=headers, timeout=self.__config.api_timeout())
            if response.status_code != 200:
                print(
                    f'Calling {self.__config.auth_uri()} failed, code - {response.status_code}, body - {response.text}')
                retries -= 1
                continue

            json_response = response.json()
            self.auth_token = f'{json_response["token_type"]} {json_response["access_token"]}'
            break


class StatusChangeService:
    success = 'Status was changed for item with mid#{mid}, ' \
              'status changed to - {status},  market - {market},  status reason - {reason}'
    error = 'Error during change mid#{mid} - error is: {error}'

    def __init__(self, endpoint_uri: str, client: BaseClient):
        self.change_status_uri = endpoint_uri
        self.client = client

    async def change_status(self, model: StatusChangeModel) -> StatusChangeResult:
        uri = self.change_status_uri.format(id=model.id_item)

        try:
            response = await self.client.send_patch(uri, model.to_json())
            if response.status == 401:
                response = await self.client.send_patch(uri, model.to_json(), re_init_token=True)

            if response.status != 200:
                body = await response.text()
                raise ConnectionError(
                    f'Calling {uri} failed for mid#{model.mid}, response code - {response.status}, body - {body}')

            reason = model.status_reason if model.status_reason else 'None'
            info = self.success.format(mid=model.mid, status=model.status, market=model.market, reason=reason)

            return StatusChangeResult(succeed=True, info=info)
        except ConnectionError as api_error:
            return StatusChangeResult(info=str(api_error))
        except Exception as e:
            error = str(e) if str(e) else e.__repr__()

            return StatusChangeResult(info=self.error.format(mid=model.mid, error=error))