from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('apps.blog.urls')),
    path('api/', include('apps.blog.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
