from pathlib import Path

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    name: str = "PocketRelay"
    mode: str = "local"
    data_dir: Path = Path("./data")
    worktree_dir: Path = Path("./data/worktrees")
    max_concurrent_tasks: int = 1
    default_task_timeout_seconds: int = 900
    telemetry_enabled: bool = False

class TelegramSettings(BaseModel):
    transport: str = "polling"
    owner_ids: list[int] = Field(default_factory=list)
    allowed_chat_types: list[str] = ["private"]
    reject_unknown_users: bool = True
    max_prompt_length: int = 12000

class SecuritySettings(BaseModel):
    require_pairing: bool = True
    pairing_code_ttl_seconds: int = 300
    redact_secrets: bool = True
    allow_raw_shell: bool = False
    allow_auto_commit: bool = False
    allow_auto_push: bool = False
    allow_non_workspace_files: bool = False

class ProjectConfig(BaseModel):
    slug: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{1,40}$")
    display_name: str
    repository_path: Path
    adapter: str = "auto"
    default_branch: str = "main"
    enabled: bool = True
    allowed_test_commands: list[list[str]] = Field(default_factory=list)

class ConfigFile(BaseModel):
    app: AppSettings = Field(default_factory=AppSettings)
    telegram: TelegramSettings = Field(default_factory=TelegramSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    projects: list[ProjectConfig] = Field(default_factory=list)

class Settings(BaseSettings):
    telegram_bot_token: str = ""
    pocketrelay_master_key: str = ""
    pocketrelay_log_level: str = "INFO"
    pocketrelay_database_path: Path = Path("./data/pocketrelay.db")
    pocketrelay_config_path: Path = Path("./config.yml")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

def load_config(config_path: Path) -> ConfigFile:
    if not config_path.exists():
        return ConfigFile()
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
        return ConfigFile.model_validate(data)

settings = Settings()
config = load_config(settings.pocketrelay_config_path)
