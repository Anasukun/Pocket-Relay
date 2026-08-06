import hashlib
import time
import secrets
from dataclasses import dataclass


@dataclass
class ApprovalRequest:
    id: str
    task_id: str
    user_id: int
    action_type: str
    payload_hash: str
    created_at: float
    ttl_seconds: int = 300
    status: str = "PENDING"  # PENDING, APPROVED, REJECTED, EXPIRED

    @property
    def is_expired(self) -> bool:
        return time.time() > (self.created_at + self.ttl_seconds)

class ApprovalService:
    def __init__(self) -> None:
        self._requests: dict[str, ApprovalRequest] = {}

    def compute_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def create_request(self, task_id: str, user_id: int, action_type: str, payload_content: str, ttl_seconds: int = 300) -> ApprovalRequest:
        payload_hash = self.compute_hash(payload_content)
        req_id = f"appr-{secrets.token_hex(12)}"
        req = ApprovalRequest(
            id=req_id,
            task_id=task_id,
            user_id=user_id,
            action_type=action_type,
            payload_hash=payload_hash,
            created_at=time.time(),
            ttl_seconds=ttl_seconds,
            status="PENDING",
        )
        self._requests[req_id] = req
        return req

    def get_request(self, req_id: str) -> ApprovalRequest | None:
        return self._requests.get(req_id)

    def consume_approval(self, req_id: str, user_id: int, expected_payload_hash: str) -> bool:
        req = self.get_request(req_id)
        if not req:
            return False
        if req.user_id != user_id or req.status != "PENDING":
            return False
        if req.is_expired:
            req.status = "EXPIRED"
            return False
        if req.payload_hash != expected_payload_hash:
            return False
        req.status = "APPROVED"
        return True

    def reject_approval(self, req_id: str, user_id: int) -> bool:
        req = self.get_request(req_id)
        if not req or req.user_id != user_id or req.status != "PENDING":
            return False
        req.status = "REJECTED"
        return True

approval_service = ApprovalService()
