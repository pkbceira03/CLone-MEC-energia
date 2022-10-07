from rest_framework import serializers

from universities.utils import CnpjValidator

from .models import University


class UniversitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'name', 'cnpj']

    def validate_cnpj(self, cnpj: str):
        try:
            CnpjValidator.validate(cnpj)
        except Exception as e:
            raise serializers.ValidationError(str(e.args))
        return cnpj
