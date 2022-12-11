from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema

from .models import ConsumerUnit, University
from users.requests_permissions import RequestsPermissions
from utils.user_type_util import UserType
from . import serializers

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = serializers.UniversitySerializer
    http_method_names = ['get', 'post', 'put']

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
    queryset = ConsumerUnit.objects.all()
    serializer_class = serializers.ConsumerUnitSerializer
    http_method_names = ['get', 'post', 'put']

    @swagger_auto_schema(query_serializer=serializers.ConsumerUnitParamsSerializer)
    def list(self, request: Request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.defaut_users_permissions
        
        params_serializer = serializers.ConsumerUnitParamsSerializer(data=request.GET)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        request_university_id = request.GET.get('university_id')

        try:
            RequestsPermissions.check_request_permissions(request_university_id, request.user, user_types_with_permission)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)
        
        queryset = ConsumerUnit.objects.filter(university = request_university_id)
        serializer = serializers.ConsumerUnitSerializer(queryset, many=True, context={'request': request})

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