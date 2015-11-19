from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View, TemplateView
from django.views.generic.edit import FormView

from projectforum.projects.models import Project
from projectforum.projects.forms import *
from projectforum.ratings.forms import ReviewForm
from projectforum.ratings.models import UserReview
from projectforum.user_profiles.models import UserProfile

import project_filters


class ProjectListView(ListView):
    """
    Project list view.
    """
    model = Project
    template_name = 'project_list.html'


class ProjectView(View):
    """
    Returns a JSON list of projects accempting applicants based on parameters:
          '*' marks the default value
    status: The current state of the project
        *1: Accepting Applicants
        2: In progress
        3: Canceled
        4: Finished
    order: How the results should be sorted:
        *timestamp: When was the project created?
        payment: Whether we sort by salary.  Will subsort ascending descending
                 based on type
        title: Sort by the titles in alphabetical order
    salary:
        *Lump: Lump Sum
        Hourly
    ascending: Whether or not we sort by ascending or descending order
        *True: Ascending order
        False: Descending order
    starting_from: Integer Default is 1.  Return projects starting from this
                   number
    ending_at: Integer Default is 10. Stop returning projects at this number
    """
    def get(self, request, *args, **kwargs):
        status = int(request.GET.get('status', 1))
        order = request.GET.get('order', 'timestamp')
        salary = request.GET.get('salary', 'Lump')
        ascending = bool(request.GET.get('ascending', True))
        starting_from = int(request.GET.get('starting_from', 0))
        ending_at = int(request.GET.get('ending_at', 10))
        return project_filters.get_project_list(status=status,
                                                order=order,
                                                salary=salary,
                                                ascending=ascending,
                                                starting_from=starting_from,
                                                ending_at=ending_at)


class CreateView(FormView):
    template_name = 'create.html'
    form_class = ProjectForm

    def form_valid(self, form):
        project_instance = form.save(commit=False)
        setattr(project_instance, 'owner', self.request.user)
        project_instance.save()
        form.save_m2m()
        return redirect(reverse('project:detail',
                                kwargs={'id': project_instance.id}))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateView, self).dispatch(*args, **kwargs)


class ProjectDetailView(TemplateView):
    """
    Project detail view.
    """
    template_name = 'project_detail.html'

    def get(self, request, *args, **kwargs):
        try:
            self.project = Project.objects.get(id=kwargs['id'])
        except Project.DoesNotExist:
            raise Http404("Project with given id does not exist")
        self.user = self.request.user
        self.logged_in = self.request.user.is_authenticated()
        return super(ProjectDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        form = ReviewForm(self.request.POST or None)
        project_reviews = UserReview.objects.filter(project=self.project)
        context.update({
            'project': self.project,
            'logged_in': self.logged_in,
            'user': self.request.user,
            'form': form,
            'project_reviews': project_reviews
        })
        return context


def accept_applicant(request, id, username):
    usermodel = get_user_model()
    try:
        project = Project.objects.get(id=id)
        if request.user != project.owner:
            return JsonResponse({
                'status': -1,
                'errors': [
                    "Only the project owner can accept applicant."
                ]
            })
        applicant = usermodel.objects.get(username=username)
        applicant_accepted = project.accept_applicant(applicant)

    except Project.DoesNotExist:
        return JsonResponse({'status': -1, 'errors': ["Invalid project id"]})
    except usermodel.DoesNotExist:
        return JsonResponse({
            'status': -1,
            'errors': ["Invalid applicant username"]
        })
    if applicant_accepted:
        return JsonResponse({'status': 1})
    return JsonResponse({
        'status': -1,
        'errors': ["Unable to accept applicant."]
    })


def apply_to_project(request, id):
    if not request.user.is_authenticated():
        return JsonResponse({
            'status': -1,
            'errors': ["User must be logged in to apply."]
        })
    applicant = request.user
    try:
        project = Project.objects.get(id=id)
        project.applicants.add(applicant)
    except Project.DoesNotExist:
        return JsonResponse({
            'status': -1,
            'errors': ["Invalid project id"]
        })
    return JsonResponse({'status': 1})


def withdraw_application(request, id):
    if not request.user.is_authenticated():
        return JsonResponse({
            'status': -1,
            'errors': ["User must be logged in to withdraw application."]
        })
    applicant = request.user
    try:
        project = Project.objects.get(id=id)
        if applicant not in project.applicants.all():
            return JsonResponse({
                'status': -1,
                'errors': [
                    "User must be an applicant to withdraw application."
                ]
            })
        project.applicants.remove(applicant)
    except Project.DoesNotExist:
        return JsonResponse({'status': -1, 'errors': ["Invalid project id"]})
    return JsonResponse({'status': 1})


def mark_complete(request, id):
    try:
        project = Project.objects.get(id=id)
        if request.user != project.owner:
            return JsonResponse({
                'status': -1,
                'errors': ["Only the project owner can mark it as complete."]
            })
        project.status = 4
        project.save()
    except Project.DoesNotExist:
        return JsonResponse({'status': -1, 'errors': ["Invalid project id"]})
    return JsonResponse({'status': 1})


def cancel_project(request, id):
    try:
        project = Project.objects.get(id=id)
        if request.user != project.owner:
            return JsonResponse({
                'status': -1,
                'errors': ["Only the project owner can mark it as complete."]
            })
        project.status = 3
        project.save()
    except Project.DoesNotExist:
        return JsonResponse({'status': -1, 'errors': ["Invalid project id"]})
    return JsonResponse({'status': 1})


def reopen_project(request, id):
    try:
        project = Project.objects.get(id=id)
        if request.user != project.owner:
            return JsonResponse({
                'status': -1,
                'errors': ["Only the project owner can reopen project."]
            })
        project.status = 2
        project.save()
    except Project.DoesNotExist:
        return JsonResponse({'status': -1, 'errors': ["Invalid project id"]})
    return JsonResponse({'status': 1})


def reopen_applications(request, id):
    try:
        project = Project.objects.get(id=id)
        if request.user != project.owner:
            return JsonResponse({
                'status': -1,
                'errors': ["Only the project owner can reopen applications."]
            })
        project.status = 1
        project.save()
    except Project.DoesNotExist:
        return JsonResponse({'status': -1, 'errors': ["Invalid project id"]})
    return JsonResponse({'status': 1})


def close_applications(request, id):
    try:
        project = Project.objects.get(id=id)
        if request.user != project.owner:
            return JsonResponse({
                'status': -1,
                'errors': ["Only the project owner can reopen applications."]
            })
        project.status = 2
        project.save()
    except Project.DoesNotExist:
        return JsonResponse({
            'status': -1,
            'errors': ["Invalid project id"]
        })
    return JsonResponse({'status': 1})

def bookmark_add(request, id):
    try:
        project = Project.objects.get(id=id)
        if request.user == project.owner:
            return JsonResponse({
                'status': -1,
                'errors': ["Project owner cannot bookmark own project"]
            })
        if not request.user.is_authenticated():
            return JsonResponse({
                'status': -1,
                'errors': ["User must be logged in to add bookmarks."]
            })
        profile = UserProfile.objects.get(user=request.user)
        profile.bookmarked_projects.add(project)
    except Project.DoesNotExist:
        return JsonResponse({
            'status': -1,
            'errors': ["Invalid project id"]
        })
    return JsonResponse({'status': 1})

def bookmark_remove(request, id):
    try:
        project = Project.objects.get(id=id)
        if request.user == project.owner:
            return JsonResponse({
                'status': -1,
                 'errors': ["Project owner cannot bookmark own project"]
            })
        if  not request.user.is_authenticated():
            return JsonResponse({
                'status': -1,
                'errors': ["User must be logged in to remove bookmarks."]
            })
        profile = UserProfile.objects.get(user=request.user)
        profile.bookmarked_projects.remove(project)
    except Project.DoesNotExist:
        return JsonResponse({
            'status': -1,
            'errors': ["Invalid project id"]
        })
    return JsonResponse({'status': 1})
