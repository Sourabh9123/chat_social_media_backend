from django.contrib import admin

# Register your models here.
from profile_app.models import Profile,Follow


class ProfileAdmin(admin.ModelAdmin):
    search_fields = [ 'user__username','user__email', 'user__id']
    list_display = ['user__username', 'user__email']
    list_display_links = ['user__username', 'user__email']

class FollowAdmin(admin.ModelAdmin):
    search_fields = ['follower__username','follower__email', 'follower__id',
                      'following__username','following__email', 'following__id']
    list_display_links = ['follower__username', 'following__username']
    list_display =['follower__username', 'following__username']
admin.site.register(Profile, ProfileAdmin)

admin.site.register(Follow, FollowAdmin)
