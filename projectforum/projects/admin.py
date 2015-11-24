from django.contrib import admin

from projectforum.projects.models import Project, ProjectTag
from projectforum.projects.models import ProjectApplication


class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)


class ProjectTagAdmin(admin.ModelAdmin):
    pass


admin.site.register(ProjectTag, ProjectTagAdmin)


class ProjectApplicationAdmin(admin.ModelAdmin):
    pass


admin.site.register(ProjectApplication, ProjectApplicationAdmin)
