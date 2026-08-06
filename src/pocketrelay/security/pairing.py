import secrets
import time
from dataclasses import dataclass


@dataclass
class PairingCode:
    code: str
    created_at: float
    ttl_seconds: int = 300
    used: bool = False
    attempts: int = 0

    @property
    def is_expired(self) -> bool:
        return time.time() > (self.created_at + self.ttl_seconds)

class PairingManager:
    MAX_ATTEMPTS = 5

    def __init__(self) -> None:
        self._active_code: PairingCode | None = None

    def generate_code(self, ttl_seconds: int = 300) -> str:
        code = f"{secrets.randbelow(900000) + 100000}"
        self._active_code = PairingCode(code=code, created_at=time.time(), ttl_seconds=ttl_seconds)
        return code

    def verify_code(self, code: str) -> bool:
        if not self._active_code:
            return False
        if self._active_code.used or self._active_code.is_expired:
            return False

        self._active_code.attempts += 1
        
        if self._active_code.attempts > self.MAX_ATTEMPTS:
            self._active_code = None
            return False

        if self._active_code.code == code.strip():
            self._active_code.used = True
            return True
            
        if self._active_code.attempts == self.MAX_ATTEMPTS:
            self._active_code = None
            
        return False

pairing_manager = PairingManager()
