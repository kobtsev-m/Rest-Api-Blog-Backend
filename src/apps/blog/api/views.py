from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView

from apps.blog.models import Post, PostImage, Category
from apps.blog.api.serializers import (
    PostSerializer,
    PostImageSerializer,
    CategorySerializer
)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        post = serializer.save()
        for image_data in self.request.data.getlist('images'):
            image = PostImageSerializer(data={'post': post.pk, 'data': image_data})
            image.is_valid(raise_exception=True)
            image.save()


class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
