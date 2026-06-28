import re

from splent_framework.seeders.BaseSeeder import BaseSeeder

from splent_io.splent_feature_projects.models import Project


def _slugify(value: str) -> str:
    value = value.lower().strip()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


# Generic demo data. Products that need richer, research-oriented projects use
# the splent_feature_research_projects refinement, which ships its own seeder.
_PROJECTS = [
    {
        "title": "Sample Project One",
        "summary": "A short description of the first project.",
        "status": "active",
    },
    {
        "title": "Sample Project Two",
        "summary": "A short description of the second project.",
        "status": "past",
    },
]


class ProjectsSeeder(BaseSeeder):
    def run(self):
        data = [
            Project(
                title=p["title"],
                slug=_slugify(p["title"]),
                summary=p["summary"],
                description=p["summary"],
                status=p["status"],
                order=i,
                published=True,
            )
            for i, p in enumerate(_PROJECTS, start=1)
        ]
        self.seed(data)
