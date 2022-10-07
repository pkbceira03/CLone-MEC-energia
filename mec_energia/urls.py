from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views
from django.conf.urls.static import static

import universities.urls as universities_urls

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path(r'api/token/', views.obtain_auth_token),
    path(r'api/', include(universities_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
