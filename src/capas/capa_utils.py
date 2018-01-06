from .geometrias import MultiPoligono, Poligono, Punto, Linea, MultiPunto, MultiLinea, Raster
from django.contrib.gis.db import models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db import connection
from .models import Capas, Atributos, Categoria, Parametro
from rest_framework.exceptions import ValidationError
import json

class CapaImporter():

    def __init__(self, capa, nombre, categoria, verificar_nombre=True,
                 verificar_categoria=True):
        self.cursor = connection.cursor()
        if verificar_nombre:
            self.nombre = self.validar_nombre(nombre)
        if verificar_categoria:
            self.categoria = self.validar_categoria(categoria)
        self.capa = capa
        self.status = False

    def get_tipo(self, tipo):
        """
        Obtener el tipo de dato geometrico
        """
        if tipo == Atributos.PUNTO:
            return models.PointField()
        elif tipo == Atributos.POLIGONO:
            return models.PolygonField()
        elif tipo == Atributos.POLIGONO_MULTIPLE:
            return models.MultiPolygonField()
        elif tipo == Atributos.PUNTO_MULTIPLE:
            return models.MultiPointField()
        elif tipo == Atributos.LINEA:
            return models.LineStringField()
        elif tipo == Atributos.LINEA_MULTIPLE:
            return models.MultiLineStringField()
        elif tipo == Atributos.TEXTO:
            return models.CharField(max_length=255)
        elif tipo == Atributos.ENTERO:
            return models.IntegerField()
        elif tipo == Atributos.FLOTANTE:
            return models.FloatField()
        elif tipo == Parametro.IMAGEN:
            return models.ImageField(upload_to="/")
        elif tipo == Parametro.DATE:
            return models.DateField()
        elif tipo == Parametro.DATETIME:
            return models.DateTimeField()
        else:
            return models.RasterField()

    def validar_categoria(self, categoria):
        if categoria is None:
            raise ValidationError({"categoria": "es requerida"})
        categoria = int(categoria)
        if Categoria.objects.filter(id=categoria).first() is None:
            raise ValidationError({"categoria": "no existe una categoria registrada con este ID"})
        return categoria

    def get_valor(self, tipo, valor):
        """
        Convertir el valor de geojson en una instancia de la
        clase apropiada segun el tipo de geometria
        """
        if tipo == Atributos.PUNTO:
            return Punto.get(valor)
        elif tipo == Atributos.POLIGONO:
            return Poligono.get(valor)
        elif tipo == Atributos.POLIGONO_MULTIPLE:
            return MultiPoligono.get(valor)
        elif tipo == Atributos.PUNTO_MULTIPLE:
            return MultiPunto.get(valor)
        elif tipo == Atributos.LINEA:
            return Linea.get(valor)
        elif tipo == Atributos.LINEA_MULTIPLE:
            return MultiLinea.get(valor)
        else:
            return Raster.get(valor)

    def validar_nombre(self, nombre):
        """
        valida que el nombre sea valido
        """
        try:
            nombre = nombre.replace('.', '_').replace(" ", "_").lower()
            if nombre is None:
                raise ValidationError({"nombre": "nombre de la capa es requerido"})
            if Capas.objects.filter(nombre=nombre).first() is not None:
                raise ValidationError({"nombre": "ya existe una capa registrada con este nombre"})
            return nombre
        except ValidationError as e:
            connection.rollback()
            raise ValidationError(e)

    def validar_capa(self):
        """
        Validar que toda la capa tiene un solo dato geometrico y
        que no exista otro en base de datos
        """
        tipo = self.capa[0].geometry.type
        for item in self.capa:
            if item.geometry.type.replace("Multi", "") != tipo.replace("Multi", ""):
                print(item.geometry.type, tipo.replace("Multi", ""))
                raise ValidationError("la capa tiene multiples tipos de geometria")
            tipo = item.geometry.type
        if Capas.objects.filter(nombre=self.nombre.lower()).count() > 0:
            connection.rollback()
            raise ValidationError({"mensaje": "ya existe la capa registrada"})

    def importar_tabla(self):
        """
        crea la tabla con su estructura en la base de datos
        """
        self.validar_capa()
        attrs = self.capa.common_attributes

        opciones = {
            "__module__": "capas"
        }
        for i in attrs:
            if i.lower() == "id":
                continue
            opciones.update({i.lower(): models.CharField(max_length=255, null=True)})
        opciones.update({"geom": self.get_tipo(self.capa[0].geometry.type)})
        modelo = type(self.nombre, (models.Model,), opciones)
        esquema = BaseDatabaseSchemaEditor(connection)
        esquema.deferred_sql = []
        esquema.create_model(modelo)
        self.insertar_registros(modelo)
        self.registrar_estructura(attrs)

    def alterar_registros(self, modelo):
        for obj in self.capa:
            if obj.properties.get("modificar"):
                self.modificar_registros(modelo, obj)
            if obj.properties.get("nuevo"):
                self.insertar_registros(modelo, obj)
            if obj.properties.get("eliminar"):
                self.eliminar_registros(modelo, obj)

    def insertar_registros(self, modelo, obj):
        datos = {}
        obj.properties.pop("nuevo")
        if obj.properties.get("pk") is not None:
            obj.properties.pop("pk")
        [datos.update({key.lower(): value}) for key, value in obj.properties.items()]
        valor = self.get_valor(obj.geometry.type, obj.geometry.coordinates)
        datos.update({"geom": valor})
        modelo.objects.create(**datos)

    def modificar_registros(self, modelo, obj):
        datos = {}
        obj.properties.pop("modificar")
        pk = obj.properties.get("pk")
        objeto = modelo.objects.filter(id=pk).first()
        if objeto is None:
            raise ValidationError({"mensaje": "no existe un registro con ID " + str(pk)})
        [datos.update({key.lower(): value}) for key, value in obj.properties.items()]
        valor = self.get_valor(obj.geometry.type, obj.geometry.coordinates)
        datos.update({"geom": valor})
        instancia = modelo(**datos)
        instancia.id = pk
        instancia.save()

    def eliminar_registros(self, modelo, obj):
        obj.properties.pop("eliminar")
        pk = obj.properties.get("pk")
        modelo.objects.filter(id=pk).delete()

    def registrar_estructura(self, attrs):
        """
        registrar la estructura de la capa a nivel de datos
        """
        tipo = self.capa[0].geometry.type
        self.cursor.execute("INSERT INTO capas_capas (nombre, categoria_id, tipo) values(%s, %s, %s) RETURNING id;", (self.nombre, self.categoria, tipo,))
        _id = self.cursor.fetchone()[0]
        self.cursor.execute("INSERT INTO capas_atributos (capa_id, nombre, tipo) values(%s, 'geom', %s);", (_id, self.capa[0].geometry.type,))
        for i in attrs:
            if i.lower() == "id":
                continue
            self.cursor.execute("INSERT INTO capas_atributos (capa_id, nombre, tipo) values(%s, %s, 'Text');", (_id, i.lower(),))

    def desde_tabla(self, instancia):
        opciones = {
            "__module__": "capas"
        }
        geom = instancia.atributos.filter(nombre="geom").first()
        if geom is None:
            raise ValidationError({"capa": "falta atributo geom"})
        opciones.update({"geom": self.get_tipo(geom.tipo)})
        for i in instancia.atributos.all():
            if i.nombre.lower() in ["id", "geom"]:
                continue
            opciones.update({i.nombre.lower(): self.get_tipo(i.tipo)})
        modelo = type(instancia.nombre, (models.Model,), opciones)
        esquema = BaseDatabaseSchemaEditor(connection)
        esquema.deferred_sql = []
        esquema.create_model(modelo)