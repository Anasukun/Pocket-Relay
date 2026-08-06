import json
from pathlib import Path

import structlog

from pocketrelay.settings import config, settings

logger = structlog.get_logger()


class AuthService:
    def __init__(self) -> None:
        self._paired_ids_path = settings.pocketrelay_database_path.parent / "paired_owners.json"
        self._dynamic_owners: set[int] = set()
        self._load_paired_ids()

    def _load_paired_ids(self) -> None:
        if self._paired_ids_path.exists():
            try:
                data = json.loads(self._paired_ids_path.read_text(encoding="utf-8"))
                self._dynamic_owners = set(data.get("owner_ids", []))
                logger.info("Loaded paired owner IDs", count=len(self._dynamic_owners))
            except (json.JSONDecodeError, OSError) as e:
                logger.warning("Failed to load paired owners file", error=str(e))

    def _save_paired_ids(self) -> None:
        try:
            self._paired_ids_path.parent.mkdir(parents=True, exist_ok=True)
            self._paired_ids_path.write_text(
                json.dumps({"owner_ids": sorted(self._dynamic_owners)}),
                encoding="utf-8",
            )
        except OSError as e:
            logger.error("Failed to save paired owners file", error=str(e))

    def is_allowed(self, user_id: int) -> bool:
        return user_id in config.telegram.owner_ids or user_id in self._dynamic_owners

    def add_owner(self, user_id: int) -> None:
        if user_id not in config.telegram.owner_ids and user_id not in self._dynamic_owners:
            self._dynamic_owners.add(user_id)
            self._save_paired_ids()
            logger.info("Paired new owner", user_id=user_id)


auth_service = AuthService()
