from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import JsonResponse

from . import models
from . import serializers

from utils.subgroup_util import Subgroup


class ContractViewSet(viewsets.ModelViewSet):
    queryset = models.Contract.objects.all()
    serializer_class = serializers.ContractSerializer

    @action(detail=False, methods=['get'], url_path='list-subgroups')
    def list_subgroups(self, request: Request, pk=None):
        subgroups = Subgroup.get_all_subgroups()

        return JsonResponse(subgroups, safe=False)


class EnergyBillViewSet(viewsets.ModelViewSet):
    queryset = models.EnergyBill.objects.all()
    serializer_class = serializers.EnergyBillSerializer
