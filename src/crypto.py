from tonclient import types
from tonclient.crypto import TonCrypto

from src.client import get_venom_client


def derive_keypair(
    mnemonic: str,
    path: str = "m/44'/396'/0'/0/0"
) -> types.KeyPair:
    crypto = TonCrypto(get_venom_client())

    params = types.ParamsOfHDKeyXPrvFromMnemonic(mnemonic)
    result = crypto.hdkey_xprv_from_mnemonic(params)
    xprv = result.xprv

    params = types.ParamsOfHDKeyDeriveFromXPrvPath(xprv, path)
    result = crypto.hdkey_derive_from_xprv_path(params)
    xprv = result.xprv

    params = types.ParamsOfHDKeySecretFromXPrv(xprv)
    result = crypto.hdkey_secret_from_xprv(params)
    secret_hex = result.secret

    params = types.ParamsOfHDKeyPublicFromXPrv(xprv)
    result = crypto.hdkey_public_from_xprv(params)
    public_hex = result.public

    return types.KeyPair(public_hex, secret_hex)

