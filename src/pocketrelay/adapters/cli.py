import asyncio
import json
from collections.abc import AsyncIterator

from pocketrelay.adapters.base import AgentRequest, AgentResult


# Known coding CLIs and how they accept a prompt.
# Each entry: binary_name -> list of args to build a command.
# "{prompt}" is replaced with the actual prompt at runtime.
# Users can add any CLI not on this list via config.
KNOWN_CLIS: dict[str, list[str]] = {
    "agy": ["agy", "-p", "{prompt}", "--output-format", "json"],
    "claude": ["claude", "-p", "{prompt}", "--output-format", "json"],
    "aider": ["aider", "--message", "{prompt}", "--yes"],
    "codex": ["codex", "-q", "{prompt}"],
    "gemini": ["gemini", "-p", "{prompt}"],
    "goose": ["goose", "run", "--text", "{prompt}"],
    "amp": ["amp", "run", "--prompt", "{prompt}"],
    "cody": ["cody", "chat", "-m", "{prompt}"],
    "cursor": ["cursor", "--prompt", "{prompt}"],
}


class GenericCliAdapter:
    """Runs any coding CLI by passing a prompt and reading the output."""

    def __init__(self, binary: str) -> None:
        self.binary = binary

    def _build_command(self, prompt: str) -> list[str]:
        if self.binary in KNOWN_CLIS:
            return [
                prompt if arg == "{prompt}" else arg
                for arg in KNOWN_CLIS[self.binary]
            ]
        # Unknown CLI: fall back to a sensible default
        return [self.binary, "-p", prompt]

    async def run(self, request: AgentRequest) -> AgentResult:
        # Mock execution for testing
        if self.binary == "fake":
            return AgentResult(
                status="SUCCESS",
                response=f"Fake execution completed for prompt: {request.prompt}",
                conversation_id="fake-conv-123",
                usage={"total_tokens": 100},
            )

        command = self._build_command(request.prompt)

        process = await asyncio.create_subprocess_exec(
            *command,
            cwd=request.workspace,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=request.timeout_seconds + 30,
            )
        except TimeoutError:
            process.kill()
            await process.wait()
            raise RuntimeError(f"{self.binary} task timed out")

        stdout_text = stdout.decode("utf-8", errors="replace")
        stderr_text = stderr.decode("utf-8", errors="replace")

        try:
            payload = json.loads(stdout_text)
            return AgentResult(
                status=payload.get("status", "SUCCESS"),
                response=payload.get("response") or payload.get("result") or stdout_text,
                conversation_id=payload.get("conversation_id") or payload.get("session_id"),
                error=payload.get("error") or stderr_text or None,
                usage=payload.get("usage", {}),
            )
        except json.JSONDecodeError:
            return AgentResult(
                status="SUCCESS" if process.returncode == 0 else "ERROR",
                response=stdout_text,
                error=stderr_text if process.returncode != 0 else None,
            )

    async def stream(self, request: AgentRequest) -> AsyncIterator[dict]:
        yield {"event": "start", "binary": self.binary}
