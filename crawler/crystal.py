# %pip install pycryptodome

def decrypt(ciphertext, key, iv):
    """Decrypts the given ciphertext using the given key and IV.

    Args:
        ciphertext: The ciphertext to decrypt.
        key: The key to use for decryption.
        iv: The IV to use for decryption.

    Returns:
        The decrypted plaintext.
    """

    # Import the necessary libraries.
    import base64
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad

    # Convert the ciphertext to a bytestring.
    ciphertext = base64.b64decode(ciphertext)

    # Create an AES cipher object.
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())

    # Decrypt the ciphertext.
    plaintext = cipher.decrypt(ciphertext)

    # Remove the PKCS#7 padding from the plaintext.
    plaintext = unpad(plaintext, AES.block_size)

    # Return the decrypted plaintext.
    return plaintext.decode("utf-8")

import json
import requests

from uuid import uuid4

async def crystal():
    key = str(uuid4()).replace('-', '')
    r = await requests.get('https://loatool.taeu.kr/api/crystal-history', headers={
        'User-Agent': 'Mozilla/5.0',
    }, cookies={
        '__gpl': key,
    })
    # 고정인듯?
    iv = 'y8tjifj89e383kke'
    _decrypted = decrypt(r.text, key, iv)

    return json.loads(_decrypted)
    # {"sell":2988.0,"buy":2980.0,"serverParseDt":"2023-05-20 13:27:34"}

# from crawler.crystal import crystal
# @app.command()
# async def 크리값(ctx, *):
#     result = await crystal()
#     # 데이터 처리

#     embed=discord.Embed()
#     # ??

#     await ctx.send(embed=embed)
