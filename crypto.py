import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt(data: str, password: str) -> bytes:
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password.encode())
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    encrypted_data = aesgcm.encrypt(nonce, data.encode(), None)
    return salt + nonce + encrypted_data

def decrypt(encrypted_data: bytes, password: str) -> str:
    salt = encrypted_data[:16]
    nonce = encrypted_data[16:28]
    ciphertext = encrypted_data[28:]
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password.encode())
    aesgcm = AESGCM(key)
    decrypted_data = aesgcm.decrypt(nonce, ciphertext, None)
    return decrypted_data.decode()
