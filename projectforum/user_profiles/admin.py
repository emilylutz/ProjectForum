from django.contrib import admin
from projectforum.user_profiles.models import (
    RegistrationLink,
    UserProfile,
    UserSkillTag
)


class RegistrationLinkAdmin(admin.ModelAdmin):
    pass


admin.site.register(RegistrationLink, RegistrationLinkAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)


class UserSkillTagAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserSkillTag, UserSkillTagAdmin)
