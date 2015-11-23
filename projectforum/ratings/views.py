from django.http import Http404
from django.shortcuts import render, redirect

from projectforum.projects.models import Project
from projectforum.ratings.models import UserReview
from projectforum.ratings.forms import *


def make_review(request, id):
    if request.method == 'POST':
        try:
            project = Project.objects.get(id=id)
        except Project.DoesNotExist:
            raise Http404("Projct with given id does not exist")
        if request.user.is_authenticated() == False:
            return redirect("/profile/login")
        rating_form = ReviewForm(data=request.POST)
        rating = rating_form.save(commit=False)
        rating.reviewer = request.user
        rating.project = project
        rating.save()
        # Refreshes project page after posting a comment
        url = "/project/" + str(id)
        return redirect(url)

# allows the user to edit a review from dropdown change
def get_review_username(request, id, username):
    if request.method == 'GET':
        try:
            project = Projects.objects.get(id=id)
            review = UserReview.objects.get(project=project, )
        except Project.DoesNotExist:
            raise Http404("Projct with given id does not exist")