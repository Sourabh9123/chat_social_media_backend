from django.urls import path
from post_app.views import  (
    PostListCreateView,
    PostDetailView,
    
    CommentDetailView,
    CommentListCreateView,
    LikeListCreateView,
    BlockUserListCreateView,
    BlockUserDetailView,
    PostSavedListCreateView
)

urlpatterns = [
    path("", PostListCreateView.as_view(), name="post_list"),
    path("<uuid:post_id>/", PostDetailView.as_view(), name="post_detail"),
    path("comment/<uuid:post_id>/", CommentListCreateView.as_view(), name="create_or_list_comment"),# create comment on post
    path("comment_id/<comment_id>/", CommentDetailView.as_view(), name="edit_or_delete"),# edit or delete comment on post
    path("like/<uuid:post_id>/", LikeListCreateView.as_view(), name="create_or_list_like"), # create like or remove
    path('block/', BlockUserListCreateView.as_view(), name='block_user'),
    path('unblock/<uuid:user_id>/', BlockUserDetailView.as_view(), name='unblock_user'),
    path('saved-posts/', PostSavedListCreateView.as_view(), name='get-save-post'),



]
