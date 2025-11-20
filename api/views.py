from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Posts
from .serializers import PostSerializer
from .permissions import IsOwnerOrAdmin


class PostListCreateView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_admin:
            return Posts.objects.all()

        return Posts.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]