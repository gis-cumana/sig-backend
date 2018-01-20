from capas.models import ConsejoComunal
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point, Polygon
from rest_framework.exceptions import ValidationError
import pygeoj
import json



class ConsejoComunalSerializador(serializers.ModelSerializer):
    
      
    class Meta:
        model = ConsejoComunal
        fields = ("__all__")
        read_only_fields = ("poblacionCenso","indiceAmenaza","indiceVulnerabilidad","indiceRiesgo")


    
    def create(self, datos):
        """ Validamos que exista la comunidad """
        
        if "comunidad" in datos.keys() and datos.get("comunidad") is not None:
            datos.update({"indiceVulnerabilidad":datos.get("comunidad").indiceVulnerabilidad})
            datos.update({"indiceAmenaza":datos.get("comunidad").indiceAmenaza})
            datos.update({"indiceRiesgo":datos.get("comunidad").indiceRiesgo})

        """ pop geom from datos """
        geom = datos.pop("geom")
        """ geom is transform to native data type django"""
        geom = json.loads(geom)
        objeto = ConsejoComunal(**datos)

        if geom is not None:
            objeto.geom = Polygon(geom)  

        if not objeto.censo.all().exists() and "poblacionDeterminada" in datos.keys():
           objeto.poblacionCenso = datos.get("poblacionDeterminada")              
            
        objeto.save()
        return objeto
        
        
    
    def update(self, instance, datos):
        
        if "comunidad" in datos.keys() and datos.get("comunidad") is not None:
            if datos.get("comunidad") != instance.comunidad:
                instance.indiceVulnerabilidad = datos.get("comunidad").indiceVulnerabilidad
                instance.indiceAmenaza = datos.get("comunidad").indiceAmenaza
                instance.indiceRiesgo = datos.get("comunidad").indiceRiesgo
        
        
        """ pop geom from datos """
        geom = datos.pop("geom")
        """ geom is transform to native data type django"""
        geom = json.loads(geom)
        if geom is not None:
            instance.geom = Polygon(geom)  
        
        if not instance.censo.all().exists() and "poblacionDeterminada" in datos.keys():
           instance.poblacionCenso = datos.get("poblacionDeterminada")     
        
        for key,value in datos.items():
            setattr(instance, key, value)  
        instance.save()
        return instance
        
        
class ConsejoComunalListSerializador(serializers.ModelSerializer):
    
    link = serializers.HyperlinkedIdentityField(view_name='consejocomunal-detail', format='html')
    

    class Meta:
        model = ConsejoComunal
        fields = ("__all__")
        read_only_fields = ("poblacionCenso","indiceAmenaza","indiceVulnerabilidad","indiceRiesgo","link","censo")