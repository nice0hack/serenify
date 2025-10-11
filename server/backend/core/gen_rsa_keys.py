import os
from json import load
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from core.settings import settings

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# приватный
with open(settings.jwt_private_key_path, "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

# публичный
with open(settings.jwt_public_key_path, "wb") as f:
    f.write(private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))
