from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema

from .models import ConsumerUnit, University
from users.requests_permissions import RequestsPermissions
from users.models import UniversityUser, CustomUser
from . import serializers

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = serializers.UniversitySerializer
    http_method_names = ['post', 'put', 'get']

    def create(self, request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.super_user_permissions

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, None)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)
            
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.super_user_permissions
        university = self.get_object()

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, university.id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        return super().update(request, *args, **kwargs)

    def list(self, request):
        user_types_with_permission = RequestsPermissions.super_user_permissions

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, None)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        queryset = University.objects.all()
        serializer = serializers.UniversitySerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user_types_with_permission = RequestsPermissions.defaut_users_permissions
        university = self.get_object()
        
        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, university.id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(university)
        return Response(serializer.data)


class ConsumerUnitViewSet(viewsets.ModelViewSet):
    queryset = ConsumerUnit.objects.all()
    serializer_class = serializers.ConsumerUnitSerializer
    http_method_names = ['get', 'post', 'put']

    def create(self, request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.university_user_permissions

        body_university_id = request.data['university']

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, body_university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)
            
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.university_user_permissions
        university = self.get_object()

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, university.id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        query_serializer=serializers.ConsumerUnitParamsSerializer,
        responses={200: serializers.ListConsumerUnitSerializerForDocs})
    def list(self, request: Request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.defaut_users_permissions

        params_serializer = serializers.ConsumerUnitParamsSerializer(data=request.GET)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        request_university_id = request.GET.get('university_id')

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, request_university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)
        
        queryset = ConsumerUnit.objects.filter(university = request_university_id)
        serializer = serializers.ConsumerUnitSerializer(queryset, many=True, context={'request': request})

        # Caso o usuário seja de universidade, buscamos se saber cada uc é uma de suas ucs favoritas ou não
        # Caso sim, retornamos o atributo "is_favorite" como True. Caso não, "is_favorite" como False
        if request.user.type in RequestsPermissions.university_user_permissions:
            user: UniversityUser = UniversityUser.objects.get(pk=request.user.id)
            favorite_consumer_units = set(user.favorite_consumer_units.all())
            consumer_units = []
            # Esse loop assume que  UCs em queryset e em serializer.data
            # estão ordenadas igualmente
            for unit, unit_dict in zip(queryset, serializer.data):
                is_favorite = unit in favorite_consumer_units
                consumer_units.append({**unit_dict, 'is_favorite': is_favorite})
        else:
            consumer_units = serializer.data
            
        return Response(consumer_units, status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user_types_with_permission = RequestsPermissions.defaut_users_permissions
        consumer_unit = self.get_object()
        
        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, consumer_unit.university.id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(consumer_unit)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializers.CreateConsumerUnitAndContractSerializerForDocs)
    @action(detail=False, methods=['post'])
    def create_consumer_unit_and_contract(self, request, pk=None):
        user_types_with_permission = RequestsPermissions.university_user_permissions

        data = request.data

        params_serializer = serializers.CreateConsumerUnitAndContractSerializerForDocs(data=request.data)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            body_university_id = data['consumer_unit']['university']

            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, body_university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        try:
            ConsumerUnit.create_consumer_unit_and_contract(data['consumer_unit'], data['contract'])
            
            return Response({'Consumer Unit and Contract created'})
        except Exception as error:
            raise Exception(str(error))

    
    @swagger_auto_schema(request_body=serializers.CreateConsumerUnitAndContractSerializerForDocs)
    @action(detail=False, methods=['post'])
    def edit_consumer_unit_and_contract(self, request, pk=None):
        user_types_with_permission = RequestsPermissions.university_user_permissions

        data = request.data

        params_serializer = serializers.CreateConsumerUnitAndContractSerializerForDocs(data=request.data)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            body_university_id = data['consumer_unit']['university']

            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, body_university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        try:
            ConsumerUnit.edit_consumer_unit_and_contract(data['consumer_unit'], data['contract'])
            
            return Response({'Consumer Unit and Contract edited'})
        except Exception as error:
            raise Exception(str(error))

    @swagger_auto_schema(request_body=serializers.EditConsumerUnitCodeAndCreateContractSerializerForDocs)
    @action(detail=False, methods=['post'])
    def edit_consumer_unit_code_and_create_contract(self, request, pk=None):
        user_types_with_permission = RequestsPermissions.university_user_permissions

        data = request.data

        params_serializer = serializers.EditConsumerUnitCodeAndCreateContractSerializerForDocs(data=request.data)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            body_consumer_unit_id = data['consumer_unit']['consumer_unit_id']

            university = ConsumerUnit.objects.get(id = body_consumer_unit_id)

            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, university.id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        try:
            ConsumerUnit.edit_consumer_unit_code_and_create_contract(data['consumer_unit'], data['contract'])
            
            return Response({'Consumer Unit and Contract created'})
        except Exception as error:
            raise Exception(str(error))