from django.contrib import admin

# Register your models here.
from profile_app.models import Profile,Follow

admin.site.register(Profile)

admin.site.register(Follow)
