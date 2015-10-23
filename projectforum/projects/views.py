from django.shortcuts import render
from django.views.generic import ListView
from projectforum.projects.models import Project

# Create your views here.
class ProjectListView(ListView):
    """
    Project list view.
    """
    model = Project
    template_name = 'project_list.html'