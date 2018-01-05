from capas.models import Casos
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.exceptions import ValidationError
from datetime import datetime, date, time
from .usuarios import UsuarioSerializador
from django.contrib.gis.geos import Point


class CasosSerializador(GeoFeatureModelSerializer):
    
    class Meta:
        model = Casos
        fields = ("__all__")
        geo_field = "geom"
        read_only_fields = ("visible", "fecha_creado","hora_creado",)
    
    
    def create(self, datos):
        
        if 'geom' in datos.keys():
           geom = datos.pop("geom")
           if geom is not None:
                datos.update({'geom': Point(geom.get('coordinates'))})
        
        datos.update({'visible':False})
        datos = self.validar_fecha_hora(**datos)
        objeto = Casos.objects.create(**datos)
        return objeto


    
    def update(self, instance, datos):
        
        if 'geom' in datos.keys():
           geom = datos.pop("geom")
           if geom is not None:
                datos.update({'geom': Point(geom.get('coordinates'))})

        datos = self.validar_fecha_hora(**datos)
        for key,value in datos.items():
            setattr(instance, key, value)
        
        instance.save()
        return instance
    
    
    def validar_fecha_hora(self, **datos): 
        actual = datetime.now()
        fecha = date.today()
        hora = time(actual.hour, actual.minute, actual.second)
        claves = datos.keys()
        
        if  'fecha' not in claves:
            datos.update({'fecha':fecha})
        elif datos.get('fecha') is None:
            setattr(datos, 'fecha', fecha)
        
        if 'hora' not in claves:
            datos.update({'hora':hora})
        elif datos.get('hora') is None:
            setattr(datos, 'hora', hora)    
        
        datos.update({'fecha_creado':fecha})
        datos.update({'hora_creado':hora})

        if datos.get('fecha') > fecha:
            raise ValidationError({'Error': 'La fecha del Casos debe ser menor a %s' % (fecha)})
        elif datos.get('fecha') == fecha and datos.get('hora') > hora:
                raise ValidationError({'Error': 'La fecha y hora del Casos deben ser menor a la fecha y hora actual: (%s - %s)' % (fecha, hora)})
        return datos       
            
                    

class CasosListSerializador(serializers.ModelSerializer):
    
    link = serializers.HyperlinkedIdentityField(view_name='casos-detail', format='html')
    lng = serializers.FloatField(source="geom.x")
    lat = serializers.FloatField(source="geom.y")
    class Meta:
        model = Casos
        fields = ("lng", "lat", "descripcion", "hora", "fecha", "registro", "usuario", "capa", "link", "imagen")
        read_only_fields = ("visible", "fecha_creado", "hora_creado",)

    def create(self, datos):
        geom = datos.pop("geom")
        lng = geom.pop("x")
        lat = geom.pop("y")
        datos.update({"fecha_creado": datetime.now().date(),
                      "hora_creado": datetime.now().time(),
                      "visible": False})
        objeto = Casos(**datos)
        objeto.geom = Point(lng, lat)
        objeto.save()
        return objeto


class CasosVerSerializador(GeoFeatureModelSerializer):
    
    link = serializers.HyperlinkedIdentityField(view_name='casos-detail', format='html')
    usuario = UsuarioSerializador()
    
    class Meta:
        model = Casos
        geo_field = "geom"
        fields = ("id", "descripcion", "fecha", "hora",  "fecha_creado", "hora_creado", 
            "visible", "link", "usuario")        

    def validate(self, data):
        #import pdb
        #pdb.set_trace()
        return data