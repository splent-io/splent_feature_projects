"""
CLI commands contributed by splent_feature_projects.

These commands are auto-discovered by the framework and exposed in the
SPLENT CLI under the ``feature:projects`` group.

Usage::

    splent feature:projects hello
"""

import click


@click.command("hello")
def hello():
    """Example command — replace with your own."""
    click.echo("  Hello from splent_feature_projects!")


cli_commands = [hello]
