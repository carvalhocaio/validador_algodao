from rest_framework import serializers
from .models import Abastecimento, AbastecimentoItem, OSAutomotiva

class AbastecimentoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbastecimentoItem
        fields = "__all__"

class AbastecimentoSerializer(serializers.ModelSerializer):
    tempo_processamento = serializers.ReadOnlyField()
    abastecimento_items = AbastecimentoItemSerializer(many=True, read_only=True)

    class Meta:
        model = Abastecimento
        exclude = ("rotina", "senha", "usuario", "erro_classe", "wsdl_log",)


class OSAutomotivaSerializer(serializers.ModelSerializer):
    tempo_processamento = serializers.ReadOnlyField()

    class Meta:
        model = OSAutomotiva
        fields = "__all__"
