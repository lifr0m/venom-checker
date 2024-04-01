import functools

from tonclient import types
from tonclient.client import TonClient


@functools.cache
def get_venom_client() -> TonClient:
    config = types.ClientConfig()
    return TonClient(config)

