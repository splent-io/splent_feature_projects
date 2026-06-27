from flask_wtf import FlaskForm
from wtforms import SubmitField


class SplentFeatureProjectsForm(FlaskForm):
    submit = SubmitField("Save splent_feature_projects")
