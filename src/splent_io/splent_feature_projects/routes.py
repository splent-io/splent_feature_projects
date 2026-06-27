from flask import abort, render_template

from splent_io.splent_feature_projects import projects_bp
from splent_framework.services.service_locator import service_proxy

projects_service = service_proxy("ProjectsService")


@projects_bp.route("/projects", methods=["GET"])
def index():
    grouped = projects_service.grouped_by_status()
    return render_template("projects/list.html", grouped=grouped)


@projects_bp.route("/projects/<slug>", methods=["GET"])
def detail(slug):
    project = projects_service.get_by_slug(slug)
    if project is None:
        abort(404)
    return render_template("projects/detail.html", project=project)
