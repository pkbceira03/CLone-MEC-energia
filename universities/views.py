from rest_framework import viewsets

from .models import ConsumerUnit, University
from .serializers import ConsumerUnitSerializer, UniversitySerializer

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    http_method_names = ['get', 'post', 'put']


class ConsumerUnitViewSet(viewsets.ModelViewSet):
    queryset = ConsumerUnit.objects.all()
    serializer_class = ConsumerUnitSerializer
    http_method_names = ['get', 'post', 'put']