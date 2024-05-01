from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from blog.models import Category, Post, Comment
from rest_framework.viewsets import ModelViewSet
from .serializers import CategorySerializer, CommentSerializer, PostSerializer, AddPostSerializer, UpdatePostSerializer
from .permissions import IsOwnerOrAdmin, IsAdminOrReadOnly
from rest_framework import permissions


class ApiPost(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categories', 'author']
    search_fields = ['title', 'category', 'author_name']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddPostSerializer
        elif self.request.method == 'PATCH':
            return UpdatePostSerializer
        else:
            return PostSerializer

    queryset = Post.objects.all()

    # method saving 1
    def create(self, request, *args, **kwargs):
        author = self.request.user
        title = request.data['title']
        content = request.data['content']
        image = request.data['image']
        categories = request.data['categories']
        post = Post.objects.create(author=author, title=title, content=content, image=image)
        post.categories.set(categories)  # Set a new list of categories

        return Response('post created successfully', status=status.HTTP_200_OK)


class ApiCategory(ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ApiComment(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrAdmin, permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])

    def get_serializer_context(self):
        return {'author': self.request.user, 'post_id': self.kwargs['post_pk']}

