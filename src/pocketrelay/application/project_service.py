from pocketrelay.domain.errors import ProjectNotFoundError
from pocketrelay.settings import ProjectConfig, config


class ProjectService:
    def get_projects(self) -> list[ProjectConfig]:
        return [p for p in config.projects if p.enabled]
        
    def get_project(self, slug: str) -> ProjectConfig:
        for p in self.get_projects():
            if p.slug == slug:
                return p
        raise ProjectNotFoundError(f"Project '{slug}' not found.")

project_service = ProjectService()
