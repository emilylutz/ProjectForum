from django.http import Http404
from django.shortcuts import render, redirect

from projectforum.projects.models import Project
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
        rating.recipient = project.owner
        rating.save()
        # Refreshes project page after posting a comment
        url = "/project/" + str(id)
        return redirect(url)
