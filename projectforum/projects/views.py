from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from django.views.generic.edit import FormView
from projectforum.projects.models import Project
from projectforum.projects.forms import *

import project_filters

# Create your views here.
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
        payment: Whether we sort by salary.  Will subsort ascending descending based on type
        title: Sort by the titles in alphabetical order
    salary:
        *Lump: Lump Sum
        Hourly
    ascending: Whether or not we sort by ascending or descending order
        *True: Ascending order
        False: Descending order
    starting_from: Integer Default is 1.  Return projects starting from this number
    ending_at: Integer Default is 10. Stop returning projects at this number
    """
    def get(self, request, *args, **kwargs):
        status = int(request.GET.get('status', 1))
        order = request.GET.get('order', 'timestamp')
        salary = request.GET.get('salary', 'Lump')
        ascending = bool(request.GET.get('ascending', True))
        starting_from = int(request.GET.get('starting_from', 0))
        ending_at = int(request.GET.get('ending_at', 10))
        return project_filters.get_project_list(status = status, order = order, salary = salary,
                ascending = ascending, starting_from = starting_from, ending_at = ending_at)

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
