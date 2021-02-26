from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.blog.api.views import PostViewSet, CategoryListCreateView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

app_name = 'blog_api'

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='categories')
] 

urlpatterns += router.urls

