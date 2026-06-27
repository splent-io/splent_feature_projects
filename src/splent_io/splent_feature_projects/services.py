from splent_io.splent_feature_projects.repositories import ProjectsRepository
from splent_framework.services.BaseService import BaseService


class ProjectsService(BaseService):
    def __init__(self):
        super().__init__(ProjectsRepository())

    def list_published(self):
        return self.repository.list_published()

    def get_by_slug(self, slug: str):
        return self.repository.get_by_slug(slug)

    def grouped_by_status(self):
        return self.repository.grouped_by_status()
