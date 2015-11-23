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

    def clean_title(self):
        """
        Validate that the title has more than whitespace. Strip the whitespace
        at the start and end. Remove line breaks.
        """
        new_title = self.cleaned_data['title'].lstrip().rstrip()
        new_title = new_title.replace('\n', ' ').replace('\r', '')
        if len(new_title) <= 0:
            raise forms.ValidationError("Please use a title with more than "
                                        "just whitespace.")
        return new_title

    def clean_description(self):
        """
        Validate that the title has more than whitespace. Strip the whitespace
        at the start and end.
        """
        new_description = self.cleaned_data['description'].lstrip().rstrip()
        if len(new_description) <= 0:
            raise forms.ValidationError("Please use a description with more "
                                        "than just whitespace.")
        return new_description
