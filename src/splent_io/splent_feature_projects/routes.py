import re

from flask import (
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required

from splent_io.splent_feature_projects import projects_bp
from splent_io.splent_feature_projects.models import Project
from splent_framework.db import db
from splent_framework.services.service_locator import service_proxy

projects_service = service_proxy("ProjectsService")


# =====================================================================
# PUBLIC
# =====================================================================
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


# =====================================================================
# ADMIN — domain-specific management (the "plugin" screen)
# =====================================================================
# Known status values that always appear first, in this order; any extra
# values found in the data follow afterwards.
KNOWN_STATUSES = ["active", "past"]


def _slugify(value):
    base = re.sub(r"[^a-z0-9]+", "-", (value or "").lower()).strip("-")
    return base or "project"


def _unique_slug(title, exclude_id=None):
    base = _slugify(title)
    slug, i = base, 2
    while True:
        q = Project.query.filter_by(slug=slug)
        if exclude_id:
            q = q.filter(Project.id != exclude_id)
        if not q.first():
            return slug
        slug, i = f"{base}-{i}", i + 1


def _ordered_groups():
    """All projects (incl. drafts) grouped by status; known statuses first."""
    grouped = {}
    for p in Project.query.order_by(
        Project.order.asc(), Project.title.asc()
    ).all():
        grouped.setdefault(p.status or "active", []).append(p)
    ordered = {g: grouped.pop(g) for g in KNOWN_STATUSES if g in grouped}
    ordered.update(grouped)
    return ordered


def _known_groups():
    existing = [
        s[0] for s in db.session.query(Project.status).distinct().all() if s[0]
    ]
    seen, out = set(), []
    for g in KNOWN_STATUSES + existing:
        if g and g not in seen:
            seen.add(g)
            out.append(g)
    return out


def _form_to_data(form):
    return {
        "acronym": (form.get("acronym") or "").strip(),
        "title": (form.get("title") or "").strip(),
        "summary": (form.get("summary") or "").strip(),
        "description": (form.get("description") or "").strip(),
        "funding": (form.get("funding") or "").strip(),
        "status": (form.get("status") or "active").strip() or "active",
        "link": (form.get("link") or "").strip(),
        "image": (form.get("image") or "").strip(),
        "order": int(form.get("order") or 0),
        "published": bool(form.get("published")),
    }


@projects_bp.route("/admin/projects", methods=["GET"])
@login_required
def admin_index():
    return render_template(
        "projects/admin/list.html",
        groups=_ordered_groups(),
        known_groups=_known_groups(),
    )


@projects_bp.route("/admin/projects/new", methods=["GET", "POST"])
@login_required
def admin_new():
    if request.method == "POST":
        data = _form_to_data(request.form)
        if not data["title"]:
            flash("Title is required.", "danger")
            return redirect(url_for("projects.admin_new"))
        data["slug"] = _unique_slug(data["title"])
        db.session.add(Project(**data))
        db.session.commit()
        flash(f"Added {data['title']}.", "success")
        return redirect(url_for("projects.admin_index"))
    return render_template(
        "projects/admin/form.html", project=None, known_groups=_known_groups()
    )


@projects_bp.route("/admin/projects/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def admin_edit(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == "POST":
        data = _form_to_data(request.form)
        if not data["title"]:
            flash("Title is required.", "danger")
            return redirect(url_for("projects.admin_edit", project_id=project_id))
        if data["title"] != project.title:
            data["slug"] = _unique_slug(data["title"], exclude_id=project.id)
        for key, value in data.items():
            setattr(project, key, value)
        db.session.commit()
        flash(f"Updated {project.title}.", "success")
        return redirect(url_for("projects.admin_index"))
    return render_template(
        "projects/admin/form.html", project=project, known_groups=_known_groups()
    )


@projects_bp.route("/admin/projects/<int:project_id>/move", methods=["POST"])
@login_required
def admin_move(project_id):
    project = Project.query.get_or_404(project_id)
    new_group = (request.form.get("group") or "").strip()
    if new_group and new_group != project.status:
        project.status = new_group
        db.session.commit()
        flash(f"Moved {project.title} to {new_group}.", "success")
    return redirect(url_for("projects.admin_index"))


@projects_bp.route("/admin/projects/<int:project_id>/delete", methods=["POST"])
@login_required
def admin_delete(project_id):
    project = Project.query.get_or_404(project_id)
    title = project.title
    db.session.delete(project)
    db.session.commit()
    flash(f"Removed {title}.", "success")
    return redirect(url_for("projects.admin_index"))
