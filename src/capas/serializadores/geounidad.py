from capas.models import GeoUnidad
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point, Polygon
import pygeoj
import json
from .riesgos import RiesgosGeoUnidadSerializador

class GeoUnidadSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = GeoUnidad
        fields = ("id","nombre", "descripcion", "geom", "area", "territorio")
        read_only_fields = ("eliminable","indiceAmenaza", "indiceRiesgo", "indiceVulnerabilidad", "anyo", "fuente",)

    def create(self, datos):
        """ pop geom from datos """
        geom = datos.pop("geom")
        """ geom is transform to native data type django """
        geom = json.loads(geom)
        objeto = GeoUnidad(**datos)
        if geom is not None:
            objeto.geom = Polygon(geom)    
        objeto.save()
        return objeto
    
    def update(self, instance, datos):
        """ pop geom from datos """
        geom = datos.pop("geom")
        """ geom is transform to native data type django """
        geom = json.loads(geom)
        if geom is not None:
            instance.geom = Polygon(geom)    
        
        for key,value in datos.items():
            setattr(instance, key, value)  
        instance.save()
        return instance
        
    
class GeoUnidadListSerializador(serializers.ModelSerializer):
   
    link = serializers.HyperlinkedIdentityField(view_name='geounidad-detail', format='html')
    class Meta:
        model = GeoUnidad
        fields = ("id", "nombre","area", "indiceAmenaza", "indiceRiesgo", "indiceVulnerabilidad",\
            "fuente","anyo","geom","eliminable","link")