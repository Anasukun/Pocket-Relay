import tempfile
from pathlib import Path

import yaml

from pocketrelay.settings import load_config


def test_load_config_missing_file():
    config = load_config(Path("does_not_exist.yml"))
    assert config.app.name == "PocketRelay"

def test_load_config_valid_file():
    with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as f:
        yaml.dump({"app": {"name": "TestApp"}}, f)
        temp_path = Path(f.name)
        
    try:
        config = load_config(temp_path)
        assert config.app.name == "TestApp"
    finally:
        temp_path.unlink()
