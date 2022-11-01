from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response


from universities.models import ConsumerUnit

from .models import UniversityUser
from .serializers import RetrieveUniversityUserSerializer, UniversityUserSerializer


class UniversityUsersViewSet(ModelViewSet):
    queryset = UniversityUser.objects.all()
    serializer_class = UniversityUserSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrieveUniversityUserSerializer
        return UniversityUserSerializer

    @action(detail=True, methods=['post'], url_path='favorite-consumer-units')
    def add_or_remove_favorite_consumer_unit(self, request: Request, pk=None):
        consumer_unit_id = request.POST.get('consumer_unit_id')
        action = request.POST.get('action')
        user: UniversityUser = self.get_object()

        try:
            user.add_or_remove_favorite_consumer_unit(consumer_unit_id, action)
        except ConsumerUnit.DoesNotExist:
            return Response({'error': ['Consumer unit not found']}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': e.args}, status=status.HTTP_403_FORBIDDEN)

        action_status = 'added' if action == 'add' else 'removed'
        return Response({'status': action_status})
