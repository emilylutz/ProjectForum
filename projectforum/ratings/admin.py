from django.contrib import admin
from projectforum.ratings.models import UserReview


class UserReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserReview, UserReviewAdmin)
