import asyncio
import base64
import hashlib

from aiohttp import ClientSession
from loguru import logger
from tonclient import types
from tonclient.crypto import TonCrypto

from src.client import get_venom_client
from src.crypto import derive_keypair


async def main() -> None:
    with open('data/phrases.txt') as file:
        phrases = file.read().strip().split('\n')

    crypto = TonCrypto(get_venom_client())

    total_success = 0
    for i, mnemonic in enumerate(phrases):
        n = i + 1

        keypair = derive_keypair(mnemonic)

        async with ClientSession(headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }) as session:
            url = 'https://rewards.venom.network/api/handshake'
            payload = {
                'pubkey': keypair.public
            }
            async with session.post(url, json=payload) as resp:
                data = await resp.json()

            message = data['secret'].encode()
            unsigned = hashlib.sha256(message).digest()
            unsigned_b64 = base64.b64encode(unsigned).decode()
            params = types.ParamsOfSign(unsigned_b64, keypair)
            result = crypto.sign(params)
            signature = bytes.fromhex(result.signature)
            signature_b64 = base64.b64encode(signature).decode()

            url = 'https://rewards.venom.network/api/auth'
            payload = {
                'signature': signature_b64
            }
            async with session.post(url, json=payload):
                pass

            url = 'https://rewards.venom.network/api/check'
            payload = {
                'walletType': 'EverWallet'
            }
            async with session.post(url, json=payload) as resp:
                data = await resp.json()

            if 'is_whitelisted' in data and data['is_whitelisted']:
                logger.success(n)
                total_success += 1
            else:
                logger.error(n)
    
    logger.info(f'Total passed: {total_success}/{len(phrases)}')


if __name__ == '__main__':
    asyncio.run(main())
