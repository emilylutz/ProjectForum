from django import forms
from projectforum.ratings.models import *

class RatingForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows':'3', 'cols': '40'}))

    class Meta:
        model = UserReview
        fields = ('score', 'comment')
        widgets = {'score':forms.HiddenInput()}