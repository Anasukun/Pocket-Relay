import shutil

from pocketrelay.adapters.base import AgentAdapter
from pocketrelay.adapters.cli import KNOWN_CLIS, GenericCliAdapter


def detect_cli() -> str | None:
    """Scan PATH for any known coding CLI and return the first one found."""
    for binary in KNOWN_CLIS:
        if shutil.which(binary):
            return binary
    return None


def get_adapter(name: str) -> AgentAdapter:
    if name == "auto":
        found = detect_cli()
        if found:
            return GenericCliAdapter(binary=found)
        # Nothing detected — let it try "agy" anyway so the error is clear
        return GenericCliAdapter(binary="agy")

    # If the name matches a known CLI binary, use it directly
    if name in KNOWN_CLIS:
        return GenericCliAdapter(binary=name)

    # Otherwise treat the name itself as a binary (user's custom CLI)
    return GenericCliAdapter(binary=name)
