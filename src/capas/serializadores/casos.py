from capas.models import Casos, Imagen
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.exceptions import ValidationError
from datetime import datetime, date, time
from .usuarios import UsuarioSerializador
from django.contrib.gis.geos import Point


class ImagenSerializador(serializers.ModelSerializer):

    class Meta:
        model = Imagen
        fields = ("imagen", "caso")


class CasosListSerializador(serializers.ModelSerializer):

    link = serializers.HyperlinkedIdentityField(view_name='casos-detail', format='html')
    lng = serializers.FloatField(source="geom.x")
    lat = serializers.FloatField(source="geom.y")
    imagenes = ImagenSerializador(many=True)
    class Meta:
        model = Casos
        fields = ("lng", "lat", "descripcion", "hora", "fecha", "suceso", "usuario", "link", "imagenes",
                  "visible", "fecha_creado", "hora_creado")
        read_only_fields = ("visible", "fecha_creado", "hora_creado")

class CasosSerializador(serializers.ModelSerializer):

    lng = serializers.FloatField(source="geom.x")
    lat = serializers.FloatField(source="geom.y")
    imagenes = ImagenSerializador(many=True)

    class Meta:
        model = Casos
        fields = ("lng", "lat", "descripcion", "hora", "fecha", "suceso", "imagenes")

    def create(self, datos):

        geom = datos.pop("geom")
        imagenes = datos.pop("imagenes")
        lng = geom.pop("x")
        lat = geom.pop("y")
        datos.update({"fecha_creado": datetime.now().date(),
                      "hora_creado": datetime.now().time(),
                      "visible": False})
        datos = self.validar_fecha_hora(**datos)
        objeto = Casos(**datos)
        objeto.geom = Point(lng, lat)
        objeto.save()
        if len(imagenes) > 0:
            self.registrar_imagenes(objeto, imagenes)
        return objeto

    def registrar_imagenes(self, caso, imagenes):
        for i in imagenes:
            Imagen.objects.create(**i, caso=caso)

    def update(self, instance, datos):

        geom = datos.pop("geom")
        lng = geom.pop("x")
        lat = geom.pop("y")

        datos = self.validar_fecha_hora(**datos)

        for key,value in datos.items():
            setattr(instance, key, value)

        instance.geom = Point(lng, lat)
        instance.save()
        return instance

    def validar_fecha_hora(self, **datos):
        fecha = datetime.now().date()
        hora = datetime.now().time()
        claves = datos.keys()

        if  'fecha' not in claves:
            datos.update({'fecha':fecha})
        elif datos.get('fecha') is None:
            setattr(datos, 'fecha', fecha)

        if 'hora' not in claves:
            datos.update({'hora':hora})
        elif datos.get('hora') is None:
            setattr(datos, 'hora', hora)

        if datos.get('fecha') > fecha:
            raise ValidationError({'Error': 'La fecha del Casos debe ser menor a %s' % (fecha)})
        elif datos.get('fecha') == fecha and datos.get('hora') > hora:
                raise ValidationError({'Error': 'La fecha y hora del Casos deben ser menor a la fecha y hora actual: (%s - %s)' % (fecha, hora)})
        return datos