from pathlib import Path


def resolve_project_path(configured_path: Path) -> Path:
    if ".." in str(configured_path) or "\x00" in str(configured_path):
        raise ValueError("Invalid path containing traversal or null bytes")
    
    resolved = configured_path.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Project path does not exist: {configured_path}")

    if not resolved.is_dir():
        raise ValueError(f"Project path is not a directory: {configured_path}")

    if resolved == Path(resolved.anchor):
        raise PermissionError("Filesystem root cannot be used as a project directory")

    return resolved

def ensure_child_path(child: Path, parent: Path) -> Path:
    child_resolved = child.resolve()
    parent_resolved = parent.resolve()

    if not child_resolved.is_relative_to(parent_resolved):
        raise PermissionError(f"Path '{child}' escaped the allowed parent directory '{parent}'")

    return child_resolved
