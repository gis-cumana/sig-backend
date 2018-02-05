from capas.models import Suceso
from rest_framework import serializers
from .casos import CasosListSerializador
class SucesosSerialializador(serializers.ModelSerializer):

    class Meta:
        model = Suceso
        fields = ("__all__")

class SucesosListaSerialializador(serializers.ModelSerializer):
    casos = CasosListSerializador(many=True)
    class Meta:
        model = Suceso
        fields = ("id", "nombre", "fecha", "hora", "casos")
