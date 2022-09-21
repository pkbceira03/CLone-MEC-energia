from django.conf import settings
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views
from django.conf.urls.static import static

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path(r'api/token/', views.obtain_auth_token),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
