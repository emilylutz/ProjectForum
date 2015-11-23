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
        exclude = ['owner', 'status', 'timestamp', 'team_members',
                   'applicants']

    def clean_title(self):
        """
        Validate that the title has more than whitespace. Strip the whitespace
        at the start and end.
        """
        new_title = self.cleaned_data['title'].lstrip().rstrip()
        new_title = new_title.replace('\n', ' ').replace('\r', '')
        if len(new_title) <= 0:
            raise forms.ValidationError("Please use a title with more than "
                                        "just whitespace.")
        return new_title
