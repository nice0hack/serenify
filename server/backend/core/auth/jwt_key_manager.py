import os
import uuid
import logging
from typing import Optional, cast
from threading import Lock
from datetime import datetime, timedelta, timezone

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
)
from cryptography.hazmat.primitives import constant_time

from core.settings import settings


logger = logging.getLogger("jwt_key_manager")


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class JWTKeyManager:
    _private_keys: dict[str, bytes] = {}
    _public_keys: dict[str, bytes] = {}
    _created_at: dict[str, datetime] = {}
    _active_kid: Optional[str] = None
    _lock = Lock()

    # ---------- helpers ----------

    @staticmethod
    def _ensure_parent_dir(path: str) -> None:
        d = os.path.dirname(path)
        if d:
            os.makedirs(d, exist_ok=True)

    @staticmethod
    def _atomic_write(path: str, data: bytes) -> None:
        JWTKeyManager._ensure_parent_dir(path)
        tmp = f"{path}.tmp-{uuid.uuid4()}"
        with open(tmp, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)

    @staticmethod
    def _file_created_at(path: str) -> datetime:
        return datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc)

    @staticmethod
    def _compute_kid(public_key_pem: bytes, length: int = 16) -> str:
        digest = hashes.Hash(hashes.SHA256())
        digest.update(public_key_pem)
        h = digest.finalize().hex()
        return h[:length]

    @staticmethod
    def _max_age_timedelta(override: Optional[timedelta] = None) -> Optional[timedelta]:
        if override is not None:
            return override
        seconds = getattr(settings, "jwt_key_max_age_seconds", None)
        days = getattr(settings, "jwt_key_max_age_days", None)
        if seconds is not None:
            return timedelta(seconds=int(seconds))
        if days is not None:
            return timedelta(days=int(days))
        return None

    # ---------- key generation & rotation ----------

    @classmethod
    def generate_keys(cls, key_size: Optional[int] = None) -> tuple[bytes, bytes]:
        if key_size is None:
            key_size = getattr(settings, "jwt_key_size", 2048)

        logger.info(f"[JWTKeyManager] Generating new RSA key pair (size={key_size})")
        private_key_obj = rsa.generate_private_key(
            public_exponent=65537, key_size=cast(int, key_size)
        )

        private_pem = private_key_obj.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        public_pem = private_key_obj.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return private_pem, public_pem

    @classmethod
    def rotate_keys(
        cls,
        priv_path: Optional[str] = settings.jwt_private_key_path,
        pub_path: Optional[str] = settings.jwt_public_key_path,
        key_size: Optional[int] = None,
    ) -> str:
        if not priv_path or not pub_path:
            raise ValueError("Key paths are not defined (check settings)")

        private_pem, public_pem = cls.generate_keys(key_size)
        cls._atomic_write(priv_path, private_pem)
        cls._atomic_write(pub_path, public_pem)

        logger.info(
            f"[JWTKeyManager] Rotated keys and saved to {priv_path}, {pub_path}"
        )
        return cls.load_keys_from_file(priv_path, pub_path)

    # ---------- main entry ----------

    @classmethod
    def load_keys_from_file(
        cls,
        priv_path: Optional[str] = settings.jwt_private_key_path,
        pub_path: Optional[str] = settings.jwt_public_key_path,
        kid: Optional[str] = None,
        rotate_if_older_than: Optional[timedelta] = None,
    ) -> str:
        if not priv_path or not pub_path:
            raise ValueError("Key paths are not defined (check settings)")

        with cls._lock:
            try:
                if not (os.path.exists(priv_path) and os.path.exists(pub_path)):
                    logger.warning(
                        "[JWTKeyManager] Key files not found — generating new"
                    )
                    private_pem, public_pem = cls.generate_keys()
                    cls._atomic_write(priv_path, private_pem)
                    cls._atomic_write(pub_path, public_pem)
                else:
                    private_pem = open(priv_path, "rb").read()
                    public_pem = open(pub_path, "rb").read()

                try:
                    priv_obj = load_pem_private_key(private_pem, password=None)
                    pub_from_priv = priv_obj.public_key().public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo,
                    )
                    if not constant_time.bytes_eq(pub_from_priv, public_pem):
                        logger.error(
                            "[JWTKeyManager] Public key does not match private key — rotating"
                        )
                        return cls.rotate_keys(priv_path, pub_path)
                except Exception as e:
                    logger.error(
                        f"[JWTKeyManager] Failed to parse keys — rotating ({e})"
                    )
                    return cls.rotate_keys(priv_path, pub_path)

                created_at = cls._file_created_at(priv_path)
                max_age = cls._max_age_timedelta(rotate_if_older_than)
                if max_age and (_utcnow() - created_at) > max_age:
                    logger.info("[JWTKeyManager] Keys expired — rotating")
                    return cls.rotate_keys(priv_path, pub_path)

            except Exception as e:
                logger.exception(f"[JWTKeyManager] Error handling key files: {e}")
                raise

            key_id = kid or cls._compute_kid(public_pem)
            cls._private_keys[key_id] = private_pem
            cls._public_keys[key_id] = public_pem
            cls._created_at[key_id] = created_at
            cls._active_kid = key_id

            logger.info(f"[JWTKeyManager] Loaded active key kid={key_id}")
            return key_id

    # ---------- getters ----------

    @classmethod
    def is_active_key_expired(
        cls, *, rotate_if_older_than: Optional[timedelta] = None
    ) -> bool:
        if not cls._active_kid:
            return True
        max_age = cls._max_age_timedelta(rotate_if_older_than)
        if not max_age:
            return False
        created = cls._created_at.get(cls._active_kid)
        if not created:
            return True
        return (_utcnow() - created) > max_age

    @classmethod
    def get_private_key(cls) -> bytes:
        if not cls._active_kid:
            raise RuntimeError("No active JWT key loaded")
        return cls._private_keys[cls._active_kid]

    @classmethod
    def get_public_key(cls) -> bytes:
        if not cls._active_kid:
            raise RuntimeError("No active JWT key loaded")
        return cls._public_keys[cls._active_kid]

    @classmethod
    def get_kid(cls) -> str:
        if not cls._active_kid:
            raise RuntimeError("No active JWT key loaded")
        return cls._active_kid

    @classmethod
    def get_creation_time(cls, kid: Optional[str] = None) -> Optional[datetime]:
        key_id = kid or cls._active_kid
        if not key_id:
            raise RuntimeError("No active JWT key loaded")
        return cls._created_at.get(key_id)

    @staticmethod
    def get_public_key_by_kid(kid: str) -> Optional[str]:
        key = JWTKeyManager._public_keys.get(kid)
        return key.decode() if key else None
