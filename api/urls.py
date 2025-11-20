from django.urls import path

from .views import PostDetailView, PostListCreateView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='posts-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='posts-detail'),
]