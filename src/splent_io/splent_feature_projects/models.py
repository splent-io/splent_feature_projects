from splent_framework.db import db


class Project(db.Model):
    """A research project: funded, active or past."""

    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    acronym = db.Column(db.String(64), default="")
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True, index=True)
    summary = db.Column(db.Text, default="")
    description = db.Column(db.Text, default="")      # rich text / HTML
    funding = db.Column(db.String(255), default="")
    status = db.Column(db.String(32), default="active")  # active|past
    link = db.Column(db.String(512), default="")
    image = db.Column(db.String(512), default="")
    order = db.Column(db.Integer, default=0)
    published = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Project<{self.slug}>"
