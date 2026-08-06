from collections.abc import AsyncIterator
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass
class AgentRequest:
    prompt: str
    workspace: Path
    conversation_id: str | None = None
    timeout_seconds: int = 900
    sandbox: bool = True

@dataclass
class AgentResult:
    status: str
    response: str
    conversation_id: str | None = None
    error: str | None = None
    usage: dict | None = None

class AgentAdapter(Protocol):
    async def run(self, request: AgentRequest) -> AgentResult:
        ...

    async def stream(self, request: AgentRequest) -> AsyncIterator[dict]:
        ...
