from django import forms
from django.contrib.auth.models import User

from projectforum.ratings.models import *
from projectforum.user_profiles.models import UserProfile


class ReviewForm(forms.ModelForm):
    recipient_username = forms.CharField()
    comment = forms.CharField(widget=forms.Textarea(attrs={
                                                        'rows': '3',
                                                        'cols': '40'
                                                    }))

    class Meta:
        model = UserReview
        fields = ('score', 'comment')
        widgets = {'score': forms.HiddenInput()}

    def save(self, commit=True):
        instance = super(ReviewForm, self).save(commit=commit)
        instance.recipient = User.objects.get(username=self.cleaned_data['recipient_username'])
        return instance