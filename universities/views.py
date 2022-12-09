from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import JsonResponse

from .models import ConsumerUnit, University
from users.requests_permissions import RequestsPermissions
from utils.user_type_util import UserType
from .serializers import ConsumerUnitSerializer, UniversitySerializer, RetrieveUniversitySerializer, ConsumerUnitInRetrieveUniversitySerializer

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    http_method_names = ['get', 'post', 'put']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrieveUniversitySerializer
        return UniversitySerializer

    @action(detail=True, methods=['post'])
    def create_consumer_unit_and_contract(self, request, pk=None):
        obj = self.get_object()
        data = request.data

        if not data.get("consumer_unit"):
            raise Exception("Is necessary the data for create Consumer Unit")

        if not data.get("contract"):
            raise Exception("Is necessary the data for create Contract")

        try:
            obj.create_consumer_unit_and_contract(data['consumer_unit'], data['contract'])
            
            return Response({'Consumer Unit and Contract created'})
        except Exception as error:
            raise Exception(str(error))


class ConsumerUnitViewSet(viewsets.ModelViewSet):
    users_type_with_permission = [
        UserType.super_user,
        UserType.university_user
    ]

    queryset = ConsumerUnit.objects.all()
    serializer_class = ConsumerUnitSerializer
    http_method_names = ['get', 'post', 'put']

    def list(self, request: Request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.defaut_users_permissions      
        
        request_university_id = request.GET.get('university_id')
        if not request_university_id:
            return Response({'error': 'Is necessary the query params - university_id.'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            
        try:
            RequestsPermissions.check_request_permissions(request_university_id, request.user, user_types_with_permission)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)
        
        queryset = ConsumerUnit.objects.filter(university = request_university_id)
        serializer = ConsumerUnitSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)

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
