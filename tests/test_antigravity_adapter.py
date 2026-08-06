import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from pocketrelay.adapters.base import AgentRequest
from pocketrelay.adapters.cli import GenericCliAdapter
from pocketrelay.adapters.registry import get_adapter


@pytest.mark.asyncio
async def test_generic_cli_adapter_success():
    adapter = GenericCliAdapter(binary="agy")
    mock_payload = {
        "status": "SUCCESS",
        "response": "Hello world",
        "conversation_id": "conv-456",
        "error": None,
        "usage": {"total_tokens": 50},
    }

    mock_process = AsyncMock()
    mock_process.communicate.return_value = (json.dumps(mock_payload).encode("utf-8"), b"")

    with patch("asyncio.create_subprocess_exec", return_value=mock_process) as mock_exec:
        request = AgentRequest(prompt="Test prompt", workspace=Path("."))
        result = await adapter.run(request)

        assert result.status == "SUCCESS"
        assert result.response == "Hello world"
        assert result.conversation_id == "conv-456"

        args, _kwargs = mock_exec.call_args
        assert "agy" in args
        assert "Test prompt" in args

@pytest.mark.asyncio
async def test_generic_cli_adapter_invalid_json():
    adapter = GenericCliAdapter(binary="agy")
    mock_process = AsyncMock()
    mock_process.communicate.return_value = (b"Not JSON", b"stderr output")
    mock_process.returncode = 0

    with patch("asyncio.create_subprocess_exec", return_value=mock_process):
        request = AgentRequest(prompt="Test prompt", workspace=Path("."))
        result = await adapter.run(request)
        assert result.response == "Not JSON"

def test_adapter_registry_known_cli():
    adapter = get_adapter("agy")
    assert isinstance(adapter, GenericCliAdapter)
    assert adapter.binary == "agy"

def test_adapter_registry_custom_cli():
    adapter = get_adapter("my-custom-tool")
    assert isinstance(adapter, GenericCliAdapter)
    assert adapter.binary == "my-custom-tool"

def test_adapter_registry_fake():
    adapter = get_adapter("fake")
    assert isinstance(adapter, GenericCliAdapter)
    assert adapter.binary == "fake"
