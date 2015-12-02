from django.http import Http404, JsonResponse, HttpResponse
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
        review_form = ReviewForm(data=request.POST)
        review = review_form.save(commit=False)
        # if project is not finished or canceled
        if (project.status != 3 and project.status != 4):
            return HttpResponse(status=403)
        # if review for a user already exists
        if (len(UserReview.objects.filter(project=project, reviewer=request.user, recipient=review.recipient)) != 0):
            return HttpResponse(status=409)
        # if recipient is not part of the project
        if (review.recipient not in project.team_members.all() and review.recipient != project.owner):
            return HttpResponse(status=403)
        # if user tries to rate self
        if (review.recipient == request.user):
            return HttpResponse(status=403)
        # if reviewer is not part of the project
        if (request.user not in project.team_members.all() and request.user != project.owner):
            return HttpResponse(status=403)

        review.reviewer = request.user
        review.project = project
        review.save()
        setAverage(review.recipient)

        # Refreshes project page after posting a comment
        url = "/project/" + str(id)
        return redirect(url)


def edit_review(request, reviewid):
    try:
        review = UserReview.objects.get(id=reviewid)
        if request.user.is_authenticated() == False:
            return JsonResponse({
                'status': -1,
                'errors': ['User must login to edit review']
            })
        if request.user != review.reviewer:
            return JsonResponse({
                'status': -1,
                'errors': ['User cannot edit another review']
            })
        review.comment = request.POST.get('comment')
        review.score = request.POST.get('score')
        review.save()

        setAverage(review.recipient)
    except UserReview.DoesNotExist:
        return JsonResponse({
            'status': -1,
            'errors': ['Review does not exist']
        })
    return JsonResponse({'status': 1})


def setAverage(user):
    reviews = UserReview.objects.filter(recipient=user)
    profile = UserProfile.objects.get_or_create_profile(user)
    profile.averageRating = sum(
        review.score for review in reviews) / len(reviews)
    profile.save()

