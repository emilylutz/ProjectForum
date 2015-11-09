from django.contrib import admin

from projectforum.projects.models import Project


class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)
