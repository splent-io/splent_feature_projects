from splent_framework.admin import register_admin_resource
from splent_framework.blueprints.base_blueprint import create_blueprint
from splent_framework.services.service_locator import register_service

from splent_io.splent_feature_projects.models import Project
from splent_io.splent_feature_projects.services import ProjectsService

projects_bp = create_blueprint(__name__)


def init_feature(app):
    register_service(app, "ProjectsService", ProjectsService)

    # Surface Project in the admin panel (the wp-admin-style back-office).
    register_admin_resource(
        Project,
        name="project",
        label="Project",
        label_plural="Projects",
        icon="folder",
        group="Research",
        order=10,
        list_columns=["title", "status", "funding"],
        field_widgets={
            "description": "richtext",
            "image": "image",
            "link": "url",
            "status": "select",
            "summary": "textarea",
            "slug": "slug",
        },
        feature="projects",
    )


def inject_context_vars(app):
    return {}
