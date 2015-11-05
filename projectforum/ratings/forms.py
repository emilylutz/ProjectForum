from django import forms
from projectforum.ratings.models import *

class RatingForm(forms.ModelForm):
    class Meta:
        model = UserReview
        fields = ('score', 'comment')
        widgets = {'score':forms.HiddenInput()}