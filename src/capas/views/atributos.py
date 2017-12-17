from rest_framework import viewsets
from django.db import connection
from rest_framework.response import Response
from capas.models import Atributos, crear_modelo
from capas.serializadores import AtributoSerializador
from capas.esquema_manager import EsquemaManager

class AtributosRecursos(viewsets.ModelViewSet):

    queryset = Atributos.objects.all().select_related('capa')
    serializer_class = AtributoSerializador

    def destroy(self, request, *args, **kwargs):
        objeto = self.get_object()
        modelo = crear_modelo(objeto.capa.nombre)

        self.perform_destroy(objeto)
        esquema = EsquemaManager(connection)
        esquema.eliminar_columna(modelo, objeto.nombre)
        return Response(status=204)