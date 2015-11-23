from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from projectforum.projects.models import Project
from projectforum.ratings.models import UserReview
from projectforum.user_profiles.models import UserProfile
from projectforum.ratings.forms import *
from projectforum.ratings.models import UserReview


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

def get_review(request, id):
    try:
        review = UserReview.objects.get(id=id)
    except UserReview.DoesNotExist:
        return JsonResponse({'status': -1, 'errors': ["Invalid review id"]})
    return JsonResponse({
        'status': 1,
        'comment': review.comment
        })

def edit_review(request, id, reviewid):
    try:
        review = UserReview.objects.get(id=id)
    except Project.DoesNotExist:
            raise Http404("Projct with given id does not exist")