from rest_framework import viewsets
from capas.models import Capas, crear_modelo
from rest_framework.decorators import list_route
from rest_framework.response import Response
from capas.serializadores import CapaSerializador, CapaListSerializador
import pygeoj
from django.core.serializers import serialize
from rest_framework.parsers import FormParser, MultiPartParser
from capas.capa_utils import CapaImporter
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


class CapasRecursos(viewsets.ModelViewSet):

    queryset = Capas.objects.all()
    serializer_class = CapaSerializador

    def destroy(self, request, *args, **kwargs):
        objeto = self.get_object()
        modelo = crear_modelo(objeto.nombre)

        self.perform_destroy(objeto)
        esquema = BaseDatabaseSchemaEditor(connection)
        esquema.delete_model(modelo)
        return Response(status=204)


    def get_serializer_class(self):
        if self.action == 'list':
            return CapaListSerializador
        return CapaSerializador

    @list_route(methods=['get'], url_path=r'tipo=(?P<nombre>[^/]+)')
    def get_capa(self, request, nombre):
        modelo = crear_modelo(nombre)
        queryset = modelo.objects.all()
        data = serialize('geojson', queryset,
                         geometry_field='geom')
        data = json.loads(data)
        return Response(data, content_type="application/json")

class ImportarRecursos(viewsets.ViewSet):
    queryset = Capas.objects.all()
    serializer_class = CapaSerializador
    parser_classes = (MultiPartParser, FormParser,)

    def create(self, request, *args, **kwargs):
        _file = self.request.data.get('file')
        nombre = self.request.data.get("nombre")
        categoria = self.request.data.get("categoria")
        geo = pygeoj.load(_file.fileno())
        importer = CapaImporter(geo, nombre, categoria)
        importer.importar_tabla()
        connection.commit()
        return Response()
