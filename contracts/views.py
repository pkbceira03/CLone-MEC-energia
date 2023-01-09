from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist

from . import models
from . import serializers

from universities.models import ConsumerUnit
from users.requests_permissions import RequestsPermissions

from utils.subgroup_util import Subgroup


class ContractViewSet(viewsets.ModelViewSet):
    queryset = models.Contract.objects.all()
    serializer_class = serializers.ContractSerializer

    def create(self, request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.university_user_permissions

        body_consumer_unit_id = request.data['consumer_unit']

        try:
            consumer_unit = ConsumerUnit.objects.get(id = body_consumer_unit_id)
        except ObjectDoesNotExist:
            return Response({'error': 'consumer unit does not exist'}, status.HTTP_400_BAD_REQUEST)

        university_id = consumer_unit.university.id

        try:    
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)
            
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.university_user_permissions
        contract = self.get_object()

        university_id = contract.consumer_unit.university.id

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(query_serializer=serializers.ContractListParamsSerializer)
    def list(self, request: Request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.defaut_users_permissions
        
        params_serializer = serializers.ContractListParamsSerializer(data=request.GET)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        request_consumer_unit_id = request.GET.get('consumer_unit_id')
        
        try:
            consumer_unit = ConsumerUnit.objects.get(id = request_consumer_unit_id)
        except ObjectDoesNotExist:
            return Response({'error': 'consumer unit does not exist'}, status.HTTP_400_BAD_REQUEST)

        university_id = consumer_unit.university.id

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)
        
        queryset = models.Contract.objects.filter(consumer_unit = consumer_unit.id)
        serializer = serializers.ContractSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user_types_with_permission = RequestsPermissions.defaut_users_permissions
        contract = self.get_object()
        
        university_id = contract.consumer_unit.university.id

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(contract)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: serializers.ListSubgroupsSerializerForDocs(many=True)})
    @action(detail=False, methods=['get'], url_path='list-subgroups')
    def list_subgroups(self, request: Request, pk=None):
        try:
            subgroups = { "subgroups": Subgroup.get_all_subgroups() }
        except Exception as error:
            return Response({'list subgroups error': f'{error}'}, status.HTTP_400_BAD_REQUEST)

        return JsonResponse(subgroups, safe=False)


class EnergyBillViewSet(viewsets.ModelViewSet):
    queryset = models.EnergyBill.objects.all()
    serializer_class = serializers.EnergyBillSerializer

    @swagger_auto_schema(responses={200: serializers.EnergyBillListSerializerForDocs(many=True)},
                        query_serializer=serializers.EnergyBillListParamsSerializer)
    def list(self, request: Request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.defaut_users_permissions

        params_serializer = serializers.EnergyBillListParamsSerializer(data=request.GET)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        request_consumer_unit_id = request.GET.get('consumer_unit_id')

        try:
            consumer_unit = ConsumerUnit.objects.get(id = request_consumer_unit_id)
        except ObjectDoesNotExist:
            return Response({'error': 'consumer unit does not exist'}, status.HTTP_400_BAD_REQUEST)

        university_id = consumer_unit.university.id

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        energy_bills = consumer_unit.get_all_energy_bills()

        return JsonResponse(energy_bills, safe=False)