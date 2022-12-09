from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

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
            response = {
                'token': token.key,
                'user': {
                    'email': user.email,
                    'name': f'{user.first_name} {user.last_name}',
                    'type': user.type,
                }
            }

            if user.type == UserType.university_user:
                response['user']['university_id'] = RequestsPermissions.get_university_user_object(user.id).university.id

            return Response(response)
        except Exception as error:
            return Response({'authentication error': f'{error}'}, status.HTTP_400_BAD_REQUEST)
