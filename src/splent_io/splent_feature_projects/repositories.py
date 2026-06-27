from __future__ import annotations

from splent_io.splent_feature_projects.models import Project
from splent_framework.repositories.BaseRepository import BaseRepository


class ProjectsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Project)

    def list_published(self) -> list[Project]:
        return (
            Project.query.filter_by(published=True)
            .order_by(Project.order.asc(), Project.title.asc())
            .all()
        )

    def get_by_slug(self, slug: str) -> Project | None:
        return Project.query.filter_by(slug=slug).first()

    def grouped_by_status(self) -> dict[str, list[Project]]:
        grouped: dict[str, list[Project]] = {}
        for project in self.list_published():
            grouped.setdefault(project.status, []).append(project)
        return grouped
