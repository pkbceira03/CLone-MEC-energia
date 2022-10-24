from rest_framework import viewsets

from .models import ConsumerUnit, University
from .serializers import ConsumerUnitSerializer, UniversitySerializer, RetrieveUniversitySerializer

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    http_method_names = ['get', 'post', 'put']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrieveUniversitySerializer
        return UniversitySerializer


class ConsumerUnitViewSet(viewsets.ModelViewSet):
    queryset = ConsumerUnit.objects.all()
    serializer_class = ConsumerUnitSerializer
    http_method_names = ['get', 'post', 'put']