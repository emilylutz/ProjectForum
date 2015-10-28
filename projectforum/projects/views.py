from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView
from projectforum.projects.models import Project
from projectforum.projects.forms import *
from django.http import Http404

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
    success_url = '/project/create/complete/'

    def form_valid(self, form):
        project_instance = form.save(commit=False)
        if self.request.user.is_authenticated() == False:
            return redirect("/project/create/fail")
        setattr(project_instance, 'owner', self.request.user)
        project_instance.save()
        return redirect(self.success_url)

    def get_form_kwargs(self):
        kwargs = super(CreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

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

