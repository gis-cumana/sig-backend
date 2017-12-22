from rest_framework import viewsets
from django.db import connection
from rest_framework.response import Response
from capas.models import Atributos, crear_modelo
from capas.serializadores import AtributoSerializador
from capas.esquema_manager import EsquemaManager
from rest_framework.exceptions import ValidationError

class AtributosRecursos(viewsets.ModelViewSet):

    queryset = Atributos.objects.all().select_related('capa')
    serializer_class = AtributoSerializador

    def destroy(self, request, *args, **kwargs):
        objeto = self.get_object()
        if not objeto.eliminable:
            raise ValidationError({"mensaje": "este atributo no puede ser eliminado"})
        modelo = crear_modelo(objeto.capa.nombre)

        self.perform_destroy(objeto)
        esquema = EsquemaManager(connection)
        esquema.eliminar_columna(modelo, objeto.nombre)
        return Response(status=204)

    def update(self, request, *args, **kwargs):
        objeto = self.get_object()
        if not objeto.modificable:
            raise ValidationError({"mensaje": "este atributo no puede ser modificado"})
        return super().update(self, request, *args, **kwargs)
