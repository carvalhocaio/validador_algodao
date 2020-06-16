from django.shortcuts import render
import django_filters.rest_framework
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from config.integrador.models import Abastecimento, OSAutomotiva
from config.integrador.serializers import AbastecimentoSerializer, OSAutomotivaSerializer


class AbastecimentoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para listagem e detalhes os abastecimentos
    """
    queryset = Abastecimento.objects.all().order_by('-id')
    serializer_class = AbastecimentoSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('token', 'status', 'wsdl_erro')


class OSAutomotivaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para listagem e detalhes da OS Automotiva
    """
    queryset = OSAutomotiva.objects.all().order_by('-id')
    serializer_class = OSAutomotivaSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('token', 'status', 'wsdl_erro')

