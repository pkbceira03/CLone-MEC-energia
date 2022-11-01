from rest_framework import routers

from .views import UniversityUsersViewSet

router = routers.DefaultRouter()
router.register('users', UniversityUsersViewSet)
