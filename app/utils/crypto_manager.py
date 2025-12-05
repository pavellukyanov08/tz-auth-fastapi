import base64
import hashlib
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from passlib.context import CryptContext


class CryptoManager:
    _pwd_context: CryptContext = CryptContext(
        schemes=["bcrypt"], deprecated="auto"
    )

    @staticmethod
    def _get_secret_key(*, secret_key: str) -> bytes:
        return hashlib.sha256(string=secret_key.encode("utf-8")).digest()

    @classmethod
    def encrypt(cls, *, data: str, secret_key: str) -> str:
        secret_key_bytes = cls._get_secret_key(secret_key=secret_key)
        iv = os.urandom(12)
        encryptor = Cipher(
            algorithm=algorithms.AES(key=secret_key_bytes),
            mode=modes.GCM(initialization_vector=iv),
            backend=default_backend(),
        ).encryptor()
        ciphertext = encryptor.update(data=data.encode("utf-8")) + encryptor.finalize()
        encrypted_data = iv + encryptor.tag + ciphertext
        return base64.urlsafe_b64encode(s=encrypted_data).decode("utf-8")

    @classmethod
    def decrypt(cls, *, encrypted_data: str, secret_key: str) -> str:
        secret_key_bytes = cls._get_secret_key(secret_key=secret_key)
        raw = base64.urlsafe_b64decode(s=encrypted_data.encode("utf-8"))  # type: ignore
        iv = raw[:12]
        tag = raw[12:28]
        ciphertext = raw[28:]
        decryptor = Cipher(
            algorithm=algorithms.AES(key=secret_key_bytes),
            mode=modes.GCM(initialization_vector=iv, tag=tag),
            backend=default_backend(),
        ).decryptor()
        plaintext = decryptor.update(data=ciphertext) + decryptor.finalize()  # type: ignore
        return plaintext.decode("utf-8")

    @classmethod
    def verify_hash_sha256(
        cls, *, data: str, hashed_data: str, use_base64: bool = True
    ) -> bool:
        return hashed_data == cls.get_hash_sha256(
            data=data, use_base64=use_base64
        )

    @staticmethod
    def get_hash_sha256(*, data: str, use_base64: bool = True) -> str:
        h = hashlib.sha256(string=data.encode("utf-8")).digest()  # type: ignore
        if use_base64:
            return base64.urlsafe_b64encode(s=h).decode("utf-8")  # type: ignore
        return h.hex()
