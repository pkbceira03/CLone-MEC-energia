from rest_framework import serializers

from utils.cnpj_validator_util import CnpjValidator

from .models import ConsumerUnit, University


class UniversitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = University
        fields = ['url', 'id', 'name', 'acronym', 'cnpj']

    def validate_cnpj(self, cnpj: str):
        try:
            CnpjValidator.validate(cnpj)
        except Exception as e:
            raise serializers.ValidationError(str(e.args))
        return cnpj


class ConsumerUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConsumerUnit
        fields = ['id', 'url', 'name', 'code', 'is_active', 'date', 'is_current_energy_bill_filled', 'pending_energy_bills_number', 'university']

class ConsumerUnitParamsSerializer(serializers.Serializer):
    university_id = serializers.IntegerField()