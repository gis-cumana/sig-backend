from capas.models import Comunidad, GeoUnidad
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point, Polygon
from rest_framework.exceptions import ValidationError
import pygeoj
import json

class ComunidadSerializador(serializers.ModelSerializer):
    

    class Meta:
        model = Comunidad
        fields = ("id", "geom","nombre","descripcion","area","statusSocial","tipologiaConstructiva"\
            ,"geounidad","territorio")
        read_only_fields = ("indiceAmenaza","indiceVulnerabilidad","indiceRiesgo", "eliminable")


    
    def create(self, datos):
        """ Validamos que exista la geounidad y/o el territorio """
        self.validar_geounidad_territorio(datos)
        
        if "geounidad" in datos.keys() and datos.get("geounidad") is not None:
            datos.update({"indiceVulnerabilidad":datos.get("geounidad").indiceVulnerabilidad})
            datos.update({"indiceAmenaza":datos.get("geounidad").indiceAmenaza})
            datos.update({"indiceRiesgo":datos.get("geounidad").indiceRiesgo})
            if "territorio" in datos.keys():
                 datos.update({"territorio":None})
                  
            
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
        
        self.validar_geounidad_territorio(datos)
        
        if "geounidad" in datos.keys() and datos.get("geounidad") is not None:
            if datos.get("geounidad") != instance.geounidad:
                instance.indiceVulnerabilidad = datos.get("geounidad").indiceVulnerabilidad
                instance.indiceAmenaza = datos.get("geounidad").indiceAmenaza
                instance.indiceRiesgo = datos.get("geounidad").indiceRiesgo
                if "territorio" in datos.keys():
                    datos.update({"territorio":None})
                """ Esto se debe cambiar cuando se creen cc e infraestructuras """    
 
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

    def validar_geounidad_territorio(self,datos):

        claves = datos.keys()
        
        if "geounidad" not in claves and "territorio" not in claves:
            raise ValidationError("GeoUnidad y/o Territorio deben estar presente")

        elif ("geounidad" not in claves) and ("territorio" in claves and datos.get("territorio") is None):
            raise ValidationError("GeoUnidad y/o Territorio no puede ser null")

        elif ("geounidad" in claves and datos.get("geounidad") is None) and ("territorio" in claves and datos.get("territorio") is None):
            raise ValidationError("GeoUnidad y/o Territorio no puede ser null")                    

        elif ("geounidad" in claves and datos.get("geounidad") is None) and ("territorio" not in claves):
            raise ValidationError("GeoUnidad y/o Territorio no puede ser null")


    
class ComunidadListSerializador(serializers.ModelSerializer):
    
    link = serializers.HyperlinkedIdentityField(view_name='comunidad-detail', format='html')
    class Meta:
        model = Comunidad
        fields = ("id", "geom","nombre","descripcion","area","statusSocial","tipologiaConstructiva"\
            ,"geounidad","territorio", "indiceAmenaza","indiceVulnerabilidad","indiceRiesgo","eliminable","link")