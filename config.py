from enum import Enum, unique
from typing import TypedDict

import toml


@unique
class Environment(Enum):
    DEV = 'dev'
    SANDBOX = 'sandbox'
    STAGE = 'stage'
    PROD = 'prod'


class ApiMap(TypedDict):
    timeout: float
    auth_uri: str
    auth_user: str
    auth_password: str
    change_status_uri: str


class UrlEnvMap(TypedDict):
    dev: str
    sandbox: str
    stage: str
    prod: str


class ConfigMap(TypedDict):
    api: ApiMap
    pim_url: UrlEnvMap
    ims_url: UrlEnvMap


class Configuration:
    def __init__(self):
        with open('config.toml', 'r') as file:
            self.__entries: ConfigMap = toml.loads(file.read())

    def change_status_uri(self) -> str:
        return self.__entries['api']['change_status_uri']

    def auth_uri(self) -> str:
        return self.__entries['api']['auth_uri']

    def ims_url(self, env: Environment) -> str:
        if env.value not in self.__entries['ims_url']:
            raise Exception(f'IMS url for provided env({env.value}) not found')

        return self.__entries['ims_url'][env.value]

    def pim_url(self, env: Environment) -> str:
        if env.value not in self.__entries['pim_url']:
            raise Exception(f'PIM url for provided env({env.value}) not found')

        return self.__entries['pim_url'][env.value]

    def api_timeout(self) -> float:
        return self.__entries['api']['timeout']

    def auth_user(self) -> str:
        return self.__entries['api']['auth_user']

    def auth_password(self) -> str:
        return self.__entries['api']['auth_password']
