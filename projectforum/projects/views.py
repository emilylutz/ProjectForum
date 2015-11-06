from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import FormView
from projectforum.projects.models import Project
from projectforum.projects.forms import *

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
