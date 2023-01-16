from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist

from . import serializers
from .requests_permissions import RequestsPermissions

from utils.user_type_util import UserType

class AuthenticationToken(ObtainAuthToken):

    @swagger_auto_schema(responses={200: serializers.AuthenticationTokenSerializerForDocs()})
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,
                                            context={'request': request})

            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
        except:
            return Response({'datail': 'Unable to log in with provided credentials'}, status.HTTP_401_UNAUTHORIZED)

        try:
            UserType.get_user_type(user.type)
            response = AuthenticationToken.create_and_update_login_response(token.key, user.id, user.email, user.first_name, user.last_name, user.type)

            return Response(response)
        except Exception as error:
            return Response({'authentication error': f'{error}'}, status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(query_serializer=serializers.AuthenticationGetTokenParamsSerializer,
                        responses={200: serializers.AuthenticationGetTokenSerializerForDocs()})
    def get(self, request, *args, **kwargs):
        params_serializer = serializers.AuthenticationGetTokenParamsSerializer(data=request.data)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        try:
            Token.objects.get(pk=request.data['token'])

            valid_token = True
        except ObjectDoesNotExist:
            valid_token = False

        response = {
            'is_valid_token': valid_token
        }

        return Response(response)

    def create_and_update_login_response(token, user_id, user_email, user_first_name, user_last_name, user_type):
        response = AuthenticationToken.create_base_login_response(token, user_email, user_first_name, user_last_name, user_type)

        if user_type in RequestsPermissions.university_user_permissions:
            user = RequestsPermissions.get_university_user_object(user_id)
            university_id = user.university.id

            response = AuthenticationToken.update_university_user_response(response, university_id)

        return response

    def create_base_login_response(token, user_email, user_first_name, user_last_name, user_type):
        response = {
                'token': token,
                'user': {
                    'email': user_email,
                    'first_name': user_first_name,
                    'last_name': user_last_name,
                    'type': user_type,
                }
            }

        return response

    def update_super_user_response(response):
        return response

    def update_university_user_response(response, university_id):
        response = AuthenticationToken.insert_university_id_on_response(response, university_id)
        
        return response

    def insert_university_id_on_response(response, university_id):
        response['user']['universityId'] = university_id

        return response