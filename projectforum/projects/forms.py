from django import forms

from projectforum.lib.fields import TagsField
from projectforum.projects.models import Project, ProjectTag


class ProjectForm(forms.ModelForm):
    """
    Form for creating a new project.
    """
    required_css_class = 'required'

    tags = TagsField(ProjectTag, 'text', max_length=ProjectTag.max_length)

    class Meta:
        model = Project
        exclude = ['owner', 'status', 'timestamp', 'team_members']
