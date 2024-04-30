from __future__ import annotations

import ssl

import aiohttp
import certifi
import requests

from config import Environment, Configuration


class BaseClient:
    def __init__(self, env: Environment, config: Configuration):
        self.auth_token: str = ''
        self.__env = env
        self.__config = config
        self.__auth_url = f'{config.ims_url(env)}/{config.auth_uri()}'
        self.__init_token()

    async def send_get(self, url: str):
        headers = {'Content-Type': 'application/json'}
        context = ssl.create_default_context(cafile=certifi.where())
        timeout = aiohttp.ClientTimeout(total=self.__config.api_timeout())

        async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
            async with session.get(url, ssl=context) as response:
                await response.read()

                return response

    async def send_put(self, url: str, json_body: dict):
        headers = {'Content-Type': 'application/json', 'Authorization': self.auth_token}
        context = ssl.create_default_context(cafile=certifi.where())
        timeout = aiohttp.ClientTimeout(total=self.__config.api_timeout())

        async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
            async with session.put(url, json=json_body, ssl=context) as response:
                await response.read()
                if response.status == 401:
                    self.__init_token()
                    response = self.send_put(url, json_body)

                return response

    def get_pim_url(self) -> str:
        return self.__config.pim_url(self.__env)

    def get_gr_url(self) -> str:
        return self.__config.gr_url(self.__env)

    def get_change_status_uri(self) -> str:
        return self.__config.change_status_uri()

    def get_gr_uri(self) -> str:
        return self.__config.golden_record_uri()

    def __init_token(self) -> None:
        url = self.__auth_url
        headers = {'Content-Type': 'application/json'}
        body = {'username': self.__config.auth_user(), 'password': self.__config.auth_password()}

        retries = 3
        while retries > 0:
            response = requests.post(url, json=body, headers=headers, timeout=self.__config.api_timeout())
            if response.status_code != 200:
                retries -= 1
                continue

            json_response = response.json()
            self.auth_token = f'{json_response["token_type"]} {json_response["access_token"]}'
            break
