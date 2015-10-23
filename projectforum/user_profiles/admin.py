from django.contrib import admin
from .models import RegistrationLink, UserProfile


class RegistrationLinkAdmin(admin.ModelAdmin):
    pass


admin.site.register(RegistrationLink, RegistrationLinkAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)
