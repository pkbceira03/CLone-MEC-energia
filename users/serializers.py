from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework import serializers

from universities.serializers import ConsumerUnitSerializer

from .models import UniversityUser


class UniversityUserSerializer(HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UniversityUser
        fields = ['id', 'url', 'first_name', 'last_name', 'password',
                  'email', 'university']


class RetrieveUniversityUserSerializer(HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)

    favorite_consumer_units = ConsumerUnitSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        model = UniversityUser
        fields = ['id', 'url', 'first_name', 'last_name', 'password',
                  'email', 'university', 'favorite_consumer_units']
