from flask import request, url_for

from splent_framework.hooks.template_hooks import register_template_hook


def projects_admin_link():
    """Sidebar entry for the Projects management screen (the WP-plugin pattern)."""
    active = (
        "active"
        if request.endpoint and request.endpoint.startswith("projects.admin")
        else ""
    )
    return (
        f'<li class="sidebar-item {active}">'
        f'<a class="sidebar-link" href="{url_for("projects.admin_index")}">'
        '<i class="align-middle" data-feather="folder"></i> '
        '<span class="align-middle">Projects</span>'
        "</a>"
        "</li>"
    )


register_template_hook("layout.authenticated_sidebar", projects_admin_link)
