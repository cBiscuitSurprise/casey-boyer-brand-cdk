from dataclasses import dataclass
import os


STRATEGO_SERVER_URL_ENV_VAR_NAME = "STRATEGO_SERVER_URL"


@dataclass(frozen=True)
class GetServerRespones:
    url: str


def get_server() -> GetServerRespones:
    return GetServerRespones(url=os.environ.get(STRATEGO_SERVER_URL_ENV_VAR_NAME))
