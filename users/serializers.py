from rest_framework.serializers import HyperlinkedModelSerializer, Serializer, ModelSerializer
from rest_framework import serializers

from universities.serializers import ConsumerUnitSerializer

from .models import CustomUser, UniversityUser
from .models import University


class CustomUserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'url', 'first_name', 'last_name',
                  'email', 'type', 'created_on']

        
class UniversityUserSerializer(HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    type = serializers.CharField(read_only=True)
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())

    class Meta:
        model = UniversityUser
        fields = ['id', 'url', 'first_name', 'last_name', 'password',
                  'email', 'type', 'created_on', 'university']


class RetrieveUniversityUserSerializer(HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())
    type = serializers.CharField(read_only=True)

    favorite_consumer_units = ConsumerUnitSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        model = UniversityUser
        fields = ['id', 'url', 'first_name', 'last_name', 'password',
                  'email', 'type', 'university', 'favorite_consumer_units']

class FavoriteConsumerUnitActionSerializer(Serializer):
    action = serializers.ChoiceField(allow_blank=False, choices=['remove', 'add'])
    consumer_unit_id = serializers.IntegerField()

class UniversityUserAuthenticatedSerializerForDocs(ModelSerializer):
    email = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())

    class Meta:
        model = UniversityUser
        fields = ['email','name','type', 'university']

class AuthenticationTokenSerializerForDocs(Serializer):
    token = serializers.Field()
    user = UniversityUserAuthenticatedSerializerForDocs()
    
class AuthenticationGetTokenParamsSerializer(Serializer):
    token = serializers.Field()

class AuthenticationGetTokenParamsSerializerForDocs(Serializer):
    is_valid_token = serializers.BooleanField()