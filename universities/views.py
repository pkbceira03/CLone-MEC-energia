from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.decorators import action
from django.http import JsonResponse
from datetime import date

from .models import ConsumerUnit, University
from .serializers import ConsumerUnitSerializer, UniversitySerializer, RetrieveUniversitySerializer, ConsumerUnitInRetrieveUniversitySerializer

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

    @action(detail=True, methods=['get'], url_path='energy-bills-list')
    def list_energy_bills(self, request: Request, pk=None):
        consumer_unit = self.get_object()
        year = request.GET.get('year')

        if year:
            energy_bills = consumer_unit.get_energy_bills_by_year(int(year))
        else:
            energy_bills = consumer_unit.get_energy_bills_pending()

        return JsonResponse(energy_bills, safe=False)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ConsumerUnitInRetrieveUniversitySerializer
        return ConsumerUnitSerializer