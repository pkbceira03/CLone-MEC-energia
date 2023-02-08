import re
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from django.db import IntegrityError
from django.db.models.manager import BaseManager

from drf_yasg.utils import swagger_auto_schema

from .models import Distributor, Tariff
from users.models import UniversityUser
from universities.models import ConsumerUnit
from .serializers import DistributorSerializer, DistributorSerializerForDocs, BlueAndGreenTariffsSerializer, BlueTariffSerializer, GreenTariffSerializer, ConsumerUnitsBySubgroupByDistributorSerializerForDocs, DistributorListParamsSerializer

from users.requests_permissions import RequestsPermissions

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
                        query_serializer=DistributorListParamsSerializer)
    def list(self, request: Request, *args, **kwargs):
        '''TODO: não tenho certeza se customuser_ptr_id é a melhor maneira.
        Essa rota é exclusivamente para usuários de universidade, por isso
        o filtro é por essa classe.'''
        user: UniversityUser = UniversityUser.objects.filter(customuser_ptr_id=request.user.id).first()
        university_id = user.university.id
        distributors = Distributor.objects.filter(university_id=university_id).order_by('name')

        params_serializer = DistributorListParamsSerializer(data=request.GET)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        request_university_id = request.GET.get('university_id')

        user_types_with_permission = RequestsPermissions.default_users_permissions
        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, request_university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        distributors = Distributor.objects.filter(university_id=request_university_id).order_by('name')
        # units_count_by_distributor = self._get_consumer_units_count_by_distributor(request_university_id, distributors)
        ser = DistributorSerializer(distributors, many=True, context={'request': request})
        """ for dist in ser.data:
            dist['consumer_units'] = units_count_by_distributor[dist['id']]
            tariffs = dist['tariffs']
            dist['tariffs'] = []
            for i in range(0, len(tariffs), 2):
                t = tariffs[i]
                blue = tariffs[i]
                green = tariffs[i+1]
                dist['tariffs'].append({
                    'start_date': t['start_date'],
                    'end_date': t['end_date'],
                    'pending': t['pending'],
                    'subgroup': t['subgroup'],
                    'distributor': t['distributor'],
                    'blue': BlueTariffSerializer(blue).data,
                    'green': GreenTariffSerializer(green).data,
                }) """
        return Response(ser.data)

    """ def _get_consumer_units_count_by_distributor(self, university_id: int, distributors: 'BaseManager[Distributor]') -> dict[int, int]:
        consumer_units = ConsumerUnit.objects.filter(university_id=university_id)
        units_count_by_distributor = {}

        for unit in consumer_units:
            contract = unit.current_contract
            distributor = contract.distributor
            if distributor.id in units_count_by_distributor:
                units_count_by_distributor[distributor.id] += 1
            else:
                units_count_by_distributor[distributor.id] = 1

        for dist in distributors:
            if dist not in units_count_by_distributor:
                units_count_by_distributor[dist.id] = 0
        return units_count_by_distributor """

    @action(detail=True, methods=['get'], url_path='consumer-units-filtered-by-subgroup')
    def consumer_units_filtered_by_subgroup(self, request: Request, pk=None):
        distributor: Distributor = self.get_object()

        consumer_units = distributor.get_consumer_units_filtered_by_subgroup()

        return Response(consumer_units, status=status.HTTP_200_OK)


    """ @swagger_auto_schema(responses={200: ConsumerUnitsBySubgroupByDistributorSerializerForDocs(many=True)})
    @action(detail=False, methods=['get'], url_path='with-subgroups-with-consumer-units')
    def with_subgroups_with_consumer_units(self, request: Request):
        '''TODO: não tenho certeza se customuser_ptr_id é a melhor maneira.'''
        user: UniversityUser = UniversityUser.objects.filter(customuser_ptr_id=request.user.id).first()
        university_id = user.university.id
        distributors = Distributor.objects.filter(university_id=university_id)
        consumer_units = ConsumerUnit.objects.filter(university_id=university_id)
        units_with_subgroup_with_distributor: list[dict] = []

        for units in consumer_units:
            contract = units.current_contract
            distributor: Distributor = contract.distributor
            sub = contract.subgroup
            units_with_subgroup_with_distributor.append({'id': units.id, 'name': units.name, 'distributor': distributor.id, 'subgroup': sub})

        TMP_UNITS_FIELD = 'tmp_units_field'
        distributors_list: list[dict] = []
        for dist in distributors:
            distributors_list.append({'id': dist.id, 'name': dist.name, 'subgroups': [], TMP_UNITS_FIELD: []})
            distributors_list[-1][TMP_UNITS_FIELD] = list(filter(lambda unit: unit['distributor'] == dist.id, units_with_subgroup_with_distributor))

        for dist in distributors_list:
            for unit in dist[TMP_UNITS_FIELD]:
                del unit['distributor']

        for dist in distributors_list:
            subgroups_for_current_dist = set(map(lambda unit: unit['subgroup'], dist[TMP_UNITS_FIELD]))
            for subgroup in subgroups_for_current_dist:
                units_for_current_subgroup = list(filter(lambda unit: unit['subgroup'] == subgroup, dist[TMP_UNITS_FIELD]))
                units_without_subgroup_field = list(map(lambda unit: {'id': unit['id'], 'name': unit['name']}, units_for_current_subgroup))
                dist['subgroups'].append({'subgroup': subgroup, 'consumer_units': units_without_subgroup_field})
            del dist[TMP_UNITS_FIELD]

        return Response(distributors_list, status=status.HTTP_200_OK) """

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

