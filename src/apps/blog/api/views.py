from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView

from apps.blog.models import Post, Category
from apps.blog.api.serializers import PostSerializer, CategorySerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
