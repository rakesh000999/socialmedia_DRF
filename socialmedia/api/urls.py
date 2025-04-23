from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, ProfileDetailView,
    PostListCreateView, PostDetailView,
    LikePostView, CommentCreateView,
    AdminDeletePostView
)

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profile
    path('profile/<int:id>/', ProfileDetailView.as_view(), name='profile_detail'),

    # Post Management
    path('posts/', PostListCreateView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    # Like / Unlike
    path('posts/<int:id>/like/', LikePostView.as_view(), name='like_post'),

    # Comment
    path('posts/<int:id>/comment/', CommentCreateView.as_view(), name='comment_post'),

    # Admin delete post
    path('admin/posts/<int:id>/', AdminDeletePostView.as_view(), name='admin_delete_post'),
]
