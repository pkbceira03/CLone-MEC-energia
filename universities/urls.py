from django.urls import path, include
from rest_framework import routers

from .views import UniversityViewSet

router = routers.DefaultRouter()
router.register(r'universities', UniversityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]




