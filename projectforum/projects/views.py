from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView
from projectforum.projects.models import Project
from projectforum.projects.forms import *
from django.http import Http404, JsonResponse

# Create your views here.
class ProjectListView(ListView):
    """
    Project list view.
    """
    model = Project
    template_name = 'project_list.html'

class CreateView(FormView):
    template_name = 'create.html'
    form_class = ProjectForm

    def form_valid(self, form):
        project_instance = form.save(commit=False)
        setattr(project_instance, 'owner', self.request.user)
        project_instance.save()
        project_url = "/project/" + str(project_instance.id)
        return redirect(project_url)

    def get_form_kwargs(self):
        kwargs = super(CreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if request.user.is_authenticated() == False:
            return redirect("/profile/login?next=/project/create")
        return super(CreateView, self).get(request, *args, **kwargs)

class ProjectDetailView(TemplateView):
    """
    Project list view.
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
        context.update({
            'project': self.project,
            'logged_in': self.logged_in,
            'user': self.request.user,
        })
        return context

def accept_applicant(request, id, username):
    # TODO: make sure user is project owner!
    try:
        project = Project.objects.get(id=id)
        if request.user != project.owner:
            return JsonResponse({'status': -1, 'errors': ["Only the project owner can accept applicant."]})
        applicant = User.objects.get(username=username)
        applicant_accepted = project.accept_applicant(applicant)

    except Project.DoesNotExist:
        return JsonResponse({'status': -1, 'errors': ["Invalid project id"]})
    except User.DoesNotExist:
        return JsonResponse({'status': -1, 'errors': ["Invalid applicant username"]})
    if applicant_accepted:
        return JsonResponse({'status': 1})
    return JsonResponse({'status': -1, 'errors': ["Unable to accept applicant."]})

def apply_to_project(request, id):
    # TODO: make sure user is project owner!
    if not request.user.is_authenticated():
        return JsonResponse({'status': -1, 'errors': ["User must be logged in to apply."]})
    applicant = request.user
    try:
        project = Project.objects.get(id=id)
        project.applicants.add(applicant)
    except Project.DoesNotExist:
        return JsonResponse({'status': -1, 'errors': ["Invalid project id"]})
    return JsonResponse({'status': 1})

def withdraw_application(request, id):
    # TODO: make sure user is project owner!
    if not request.user.is_authenticated():
        return JsonResponse({'status': -1, 'errors': ["User must be logged in to withdraw application."]})
    applicant = request.user
    try:
        project = Project.objects.get(id=id)
        if applicant not in project.applicants.all():
            return JsonResponse({'status': -1, 'errors': ["User must be an applicant to withdraw application."]})
        project.applicants.remove(applicant)
    except Project.DoesNotExist:
        return JsonResponse({'status': -1, 'errors': ["Invalid project id"]})
    return JsonResponse({'status': 1})

def mark_complete(request, id):
    # TODO: make sure user is project owner!
    try:
        project = Project.objects.get(id=id)
        if request.user != project.owner:
            return JsonResponse({'status': -1, 'errors': ["Only the project owner can mark it as complete."]})
        project.status = 4
        project.save()
    except Project.DoesNotExist:
        return JsonResponse({'status': -1, 'errors': ["Invalid project id"]})
    return JsonResponse({'status': 1})

def cancel_project(request, id):
    # TODO: make sure user is project owner!
    try:
        project = Project.objects.get(id=id)
        if request.user != project.owner:
            return JsonResponse({'status': -1, 'errors': ["Only the project owner can mark it as complete."]})
        project.status = 3
        project.save()
    except Project.DoesNotExist:
        return JsonResponse({'status': -1, 'errors': ["Invalid project id"]})
    return JsonResponse({'status': 1})

def reopen_project(request, id):
    # TODO: make sure user is project owner!
    try:
        project = Project.objects.get(id=id)
        if request.user != project.owner:
            return JsonResponse({'status': -1, 'errors': ["Only the project owner can reopen project."]})
        project.status = 2
        project.save()
    except Project.DoesNotExist:
        return JsonResponse({'status': -1, 'errors': ["Invalid project id"]})
    return JsonResponse({'status': 1})

def reopen_applications(request, id):
    # TODO: make sure user is project owner!
    try:
        project = Project.objects.get(id=id)
        if request.user != project.owner:
            return JsonResponse({'status': -1, 'errors': ["Only the project owner can reopen applications."]})
        project.status = 1
        project.save()
    except Project.DoesNotExist:
        return JsonResponse({'status': -1, 'errors': ["Invalid project id"]})
    return JsonResponse({'status': 1})

def close_applications(request, id):
    # TODO: make sure user is project owner!
    try:
        project = Project.objects.get(id=id)
        if request.user != project.owner:
            return JsonResponse({'status': -1, 'errors': ["Only the project owner can reopen applications."]})
        project.status = 2
        project.save()
    except Project.DoesNotExist:
        return JsonResponse({'status': -1, 'errors': ["Invalid project id"]})
    return JsonResponse({'status': 1})
