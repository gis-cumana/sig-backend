from rest_framework import viewsets
from capas.models import Suceso
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from capas.serializadores.sucesos import SucesosSerialializador, SucesosListaSerialializador

class SucesosRecursos(viewsets.ModelViewSet):
    queryset = Suceso.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return SucesosListaSerialializador
        return SucesosSerialializador

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)