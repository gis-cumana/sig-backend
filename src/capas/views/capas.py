from rest_framework import viewsets
from capas.models import Capas, crear_modelo
from rest_framework.decorators import list_route
from rest_framework.response import Response
from capas.serializadores import CapaSerializador, CapaListSerializador
import pygeoj
import json
from django.core.serializers import serialize
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from capas.capa_utils import CapaImporter
from django.db import connection, transaction
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from rest_framework.exceptions import ValidationError


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

    @transaction.atomic
    @list_route(methods=['get', 'post'], url_path=r'nombre/(?P<nombre>[^/]+)')
    def capas_geograficas(self, request, nombre):
        def get(request, nombre):
            modelo = crear_modelo(nombre)
            queryset = modelo.objects.all()
            data = serialize('geojson', queryset,
                             geometry_field='geom')
            data = json.loads(data)
            return Response(data, content_type="application/json")

        def post(request, nombre):
            modelo = crear_modelo(nombre)
            datos = request.data
            import pdb
            pdb.set_trace()
            geo = pygeoj.load(data=datos)
            importer = CapaImporter(geo, None, None, verificar_nombre=False,
                                    verificar_categoria=False)
            importer.insertar_registros(modelo)

            queryset = modelo.objects.all()
            data = serialize('geojson', queryset,
                             geometry_field='geom')
            data = json.loads(data)
            return Response(data, status=201)

        if request.method == "GET":
            return get(request, nombre)
        elif request.method == "POST":
            return post(request, nombre)

    @transaction.atomic
    @list_route(methods=['post'], url_path=r'importar')
    def importar(self, request, *args, **kwargs):
        def validar(_file):
            if _file is None:
                raise ValidationError({"file":"es necesario la capa"})
        _file = self.request.data.get('file')
        validar(_file)
        nombre = self.request.data.get("nombre")
        categoria = self.request.data.get("categoria")
        if nombre is None:
            nombre = _file.name.replace(".geojson", "")
        if categoria is None:
            categoria = 1
        geo = pygeoj.load(_file.fileno())
        importer = CapaImporter(geo, nombre, categoria)
        importer.importar_tabla()
        return Response()