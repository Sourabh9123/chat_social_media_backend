from django.contrib import admin
from post_app.models import Post, Comment, Like, Block, SavedPost



class BlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'blocker', 'blocked', 'blocked_at')


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author','created_at')  # Add the fields you want to display, including 'id'
    ordering = ('created_at',)   #('-created_at',)
    search_fields = ('id','title', 'author',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'text','parent')  # Add 'id' and other relevant fields

class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', "post__id")  # Add 'id' and other relevant fields



class SavedPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', )  # Add 'id' and other relevant fields




admin.site.register(SavedPost, SavedPostAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Block, BlockAdmin)



