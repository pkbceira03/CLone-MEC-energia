from rest_framework.serializers import HyperlinkedModelSerializer, Serializer, ModelSerializer
from rest_framework import serializers


from utils.validators import CnpjValidator

from .models import Distributor
from universities.models import University
from tariffs.models import Tariff

class DistributorSerializer(HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # https://www.django-rest-framework.org/api-guide/relations/#serializer-relations
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())

    class Meta:
        model = Distributor
        fields = '__all__'
    
    def validate_cnpj(self, cnpj: str):
        try:
            CnpjValidator.validate(cnpj)
        except Exception as e:
            raise serializers.ValidationError(str(e.args))
        return cnpj

class BlueTariffSerializer(ModelSerializer):
    peak_tusd_in_reais_per_kw = serializers.FloatField()
    peak_tusd_in_reais_per_mwh = serializers.FloatField()
    peak_te_in_reais_per_mwh = serializers.FloatField()
    off_peak_tusd_in_reais_per_kw = serializers.FloatField()
    off_peak_tusd_in_reais_per_mwh = serializers.FloatField()
    off_peak_te_in_reais_per_mwh = serializers.FloatField()

    class Meta:
        model = Tariff
        fields = ['peak_tusd_in_reais_per_kw','peak_tusd_in_reais_per_mwh','peak_te_in_reais_per_mwh','off_peak_tusd_in_reais_per_kw','off_peak_tusd_in_reais_per_mwh','off_peak_te_in_reais_per_mwh']

class GreenTariffSerializer(ModelSerializer):
    peak_tusd_in_reais_per_mwh = serializers.FloatField()
    peak_te_in_reais_per_mwh = serializers.FloatField()
    off_peak_tusd_in_reais_per_mwh = serializers.FloatField()
    off_peak_te_in_reais_per_mwh = serializers.FloatField()
    na_tusd_in_reais_per_kw = serializers.FloatField()

    class Meta:
        model = Tariff
        fields = ['peak_tusd_in_reais_per_mwh','peak_te_in_reais_per_mwh','off_peak_tusd_in_reais_per_mwh','off_peak_te_in_reais_per_mwh','na_tusd_in_reais_per_kw',]


class BlueAndGreenTariffsSerializer(Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    subgroup = serializers.ChoiceField(allow_blank=False, choices=Tariff.subgroups)
    distributor = serializers.PrimaryKeyRelatedField(queryset=Distributor.objects.all())

    blue = BlueTariffSerializer()
    green = GreenTariffSerializer()

    def validate(self, data):
        print('>>>', self.initial_data)
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError('Start date must be before end date')
        return data

    class Meta:
        fields = '__all__'