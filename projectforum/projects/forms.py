from django import forms
from projectforum.projects.models import *

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description', 'payment', 'amount', 'tags')
        widgets = {'tags': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ProjectForm, self).__init__(*args, **kwargs)