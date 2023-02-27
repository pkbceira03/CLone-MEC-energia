import re
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from django.db import IntegrityError

from drf_yasg.utils import swagger_auto_schema

from utils.endpoints_util import EndpointsUtils

from .models import Distributor, Tariff
from .serializers import DistributorSerializer, DistributorSerializerForDocs, BlueAndGreenTariffsSerializer, BlueTariffSerializer, GreenTariffSerializer, ConsumerUnitsBySubgroupByDistributorSerializerForDocs, DistributorListParamsSerializer

from users.requests_permissions import RequestsPermissions
from universities.models import ConsumerUnit

class DistributorViewSet(ModelViewSet):
    queryset = Distributor.objects.all()
    serializer_class = DistributorSerializer

    def destroy(self, request, *args, **kwargs):
        distributor: Distributor = self.get_object()
        user_types_with_permission = RequestsPermissions.default_users_permissions
        
        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, distributor.university.id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        units = ConsumerUnit.objects.filter(university=distributor.university)

        blocking_units_ids = []
        for unit in units:
            current_contract = unit.current_contract
            if current_contract != None:
                if current_contract.distributor.id == distributor.id:
                    blocking_units_ids.append(unit.id)

        if len(blocking_units_ids) != 0:
            return Response(
                {
                    'errors': ['There are active contracts associated to this distributor'],
                    'consumer_units_ids': blocking_units_ids,
                }, status=status.HTTP_400_BAD_REQUEST)

        Distributor.objects.filter(pk=distributor.id).delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={200: DistributorSerializerForDocs()},
                        query_serializer = DistributorListParamsSerializer)
    def list(self, request: Request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.default_users_permissions

        params_serializer = DistributorListParamsSerializer(data=request.GET)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        request_university_id = request.GET.get('university_id')
        request_only_pending = request.GET.get('only_pending')
        only_pending = EndpointsUtils.convert_string_request_param_to_boolean(request_only_pending)

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, request_university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        if only_pending:
            distributors = Distributor.get_distributors_pending(request_university_id)
        else:
            distributors = Distributor.objects.filter(university_id = request_university_id)

        ser = DistributorSerializer(distributors, many=True, context={'request': request})

        return Response(ser.data, status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='consumer-units-by-subgroup')
    def consumer_units_filtered_by_subgroup(self, request: Request, pk=None):
        distributor: Distributor = self.get_object()

        consumer_units = distributor.get_consumer_units_filtered_by_subgroup()

        return Response(consumer_units, status=status.HTTP_200_OK)

class TariffViewSet(ViewSet):
    queryset = Tariff.objects.all()
    serializer_class = BlueAndGreenTariffsSerializer

    @swagger_auto_schema(request_body=BlueAndGreenTariffsSerializer)
    def create(self, request: Request):
        ser = BlueAndGreenTariffsSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        data = ser.validated_data
        start_date = data['start_date']
        end_date = data['end_date']
        distributor = data['distributor']
        subgroup = data['subgroup']
        try:
            Tariff.objects.bulk_create([
                Tariff(**data['blue'], subgroup=subgroup, flag=Tariff.BLUE, start_date=start_date, end_date=end_date, distributor=distributor),
                Tariff(**data['green'], subgroup=subgroup, flag=Tariff.GREEN, start_date=start_date, end_date=end_date, distributor=distributor)
            ])
        except IntegrityError as error:
            return self._handle_integrity_error(error)
        except Exception as e:
            raise e
        return Response(ser.data, status=status.HTTP_201_CREATED)

    def _handle_integrity_error(self, error: IntegrityError):
        error_message = str(error)
        if 'duplicate key value violates unique constraint' in error_message:
            duplicate_key = re.search('\)=(\(.*\))', error_message).groups(0)[0]
            formatted_error = f'There is already a tariff with given (subgroup, distributor, flag)={duplicate_key}'
            return Response({'errors': [formatted_error]}, status=status.HTTP_403_FORBIDDEN)
        else:
            raise error

    @swagger_auto_schema(request_body=BlueAndGreenTariffsSerializer)
    def update(self, request: Request, pk=None):
        '''Essa rota de fato foge um pouco do padrão REST: ```PUT /api/tariffs/id```.
        Nesse caso, `id` NÃO É USADO, de maneira que `id` pode ser setado para
        qualquer coisa. Ainda assim, é possível identificar as tarifas pelo
        _subgrupo_ e _distribuidora_.'''

        ser = BlueAndGreenTariffsSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        data = ser.validated_data
        tariffs = Tariff.objects.filter(subgroup=data['subgroup'], distributor=data['distributor'])
        if 0 == tariffs.count():
            return Response({'errors': [f'Could not find tariffs with '
            f'subgroup={data["subgroup"]} and distributor_id={data["distributor"].id}']}, status=status.HTTP_404_NOT_FOUND)
        assert 2 == tariffs.count()

        start_date = data['start_date']
        end_date = data['end_date']

        tariffs.filter(flag=Tariff.BLUE).update(**data['blue'], start_date=start_date, end_date=end_date)
        tariffs.filter(flag=Tariff.GREEN).update(**data['green'], start_date=start_date, end_date=end_date)

        blue_tariff = Tariff.objects.filter(subgroup=data['subgroup'], distributor=data['distributor'], flag=Tariff.BLUE).first()
        green_tariff = Tariff.objects.filter(subgroup=data['subgroup'], distributor=data['distributor'], flag=Tariff.GREEN).first()

        ser = BlueAndGreenTariffsSerializer({
            'start_date': start_date,
            'end_date': end_date,
            'distributor': data['distributor'],
            'subgroup': data['subgroup'],
            'blue': blue_tariff,
            'green': green_tariff
        })
        return Response(ser.data)

