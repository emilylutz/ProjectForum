from django.contrib import admin

from projectforum.projects.models import Project, ProjectTag


class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)


class ProjectTagAdmin(admin.ModelAdmin):
    pass


admin.site.register(ProjectTag, ProjectTagAdmin)
