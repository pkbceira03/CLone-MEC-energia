from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from universities.urls import router as universities_router
from contracts.urls import router as contracts_router

router = DefaultRouter()
router.registry.extend(universities_router.registry)
router.registry.extend(contracts_router.registry)

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path(r'api/token/', views.obtain_auth_token),
    path(r'api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
