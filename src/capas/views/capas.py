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
    @list_route(methods=['get', 'put'], url_path=r'nombre/(?P<nombre>[^/]+)')
    def capas_geograficas(self, request, nombre):
        def get(request, modelo):
            queryset = modelo.objects.all()
            data = serialize('geojson', queryset,
                             geometry_field='geom')
            data = json.loads(data)
            return Response(data)

        def update(request, modelo):
            datos = request.data.get("data").replace("'", "\"")
            try:
                datos = json.loads(datos)
                geo = pygeoj.load(data=datos)
                data = []
                for i in geo._data["features"]:
                    nuevo = i["properties"].get("nuevo")
                    modificar = i["properties"].get("modificar")
                    eliminar = i["properties"].get("eliminar")
                    if nuevo is not None or modificar is not None or eliminar is not None:
                        data.append(i)
                geo._data["features"] = data
                importer = CapaImporter(geo, None, None, verificar_nombre=False,
                                        verificar_categoria=False)
                importer.alterar_registros(modelo)

                queryset = modelo.objects.all()
                data = serialize('geojson', queryset,
                                 geometry_field='geom')
                data = json.loads(data)
                return Response(data)
            except json.decoder.JSONDecodeError as e:
                raise ValidationError({"mensaje": "json invalido, "+e})
            except ValueError:
                raise ValidationError({"mensaje": "el geojson es invalido"})


        modelo = crear_modelo(nombre)

        if request.method == "GET":
            return get(request, modelo)
        elif request.method == "PUT":
            return update(request, modelo)

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