from capas.models import Comunidad
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point, Polygon
import pygeoj
import json

class ComunidadSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = Comunidad
        fields = ("__all__")


    
    def create(self, datos):
        """ pop geom from datos """
        geom = datos.pop("geom")
        """ geom is transform to native data type django"""
        geom = json.loads(geom)
        objeto = Comunidad(**datos)
        if geom is not None:
            objeto.geom = Polygon(geom)    
        objeto.save()
        return objeto
    
    def update(self, instance, datos):
        """ pop geom from datos """
        geom = datos.pop("geom")
        """ geom is transform to native data type django"""
        geom = json.loads(geom)
        if geom is not None:
            instance.geom = Polygon(geom)    
        
        for key,value in datos.items():
            setattr(instance, key, value)  
        instance.save()
        return instance

    
class ComunidadListSerializador(serializers.ModelSerializer):
    
    link = serializers.HyperlinkedIdentityField(view_name='comunidad-detail', format='html')
    class Meta:
        model = Comunidad
        fields = ("__all__")