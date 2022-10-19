from rest_framework import viewsets

from . import models
from . import serializers

class ContractViewSet(viewsets.ModelViewSet):
    queryset = models.Contract.objects.all()
    serializer_class = serializers.ContractSerializer

class EnergyBillViewSet(viewsets.ModelViewSet):
    queryset = models.EnergyBill.objects.all()
    serializer_class = serializers.EnergyBillSerializer
