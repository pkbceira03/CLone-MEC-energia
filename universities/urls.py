from django.urls import path, include
from rest_framework import routers

from .views import ConsumerUnitViewSet, UniversityViewSet

router = routers.DefaultRouter()
router.register('universities', UniversityViewSet)
router.register('consumer-units', ConsumerUnitViewSet)

