from capas.models import Vivienda
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point, Polygon
from rest_framework.exceptions import ValidationError
import pygeoj
import json

class ViviendaSerializador(serializers.ModelSerializer):
    
    link = serializers.HyperlinkedIdentityField(view_name='vivienda-detail', format='html')
    
    class Meta:
        model = Vivienda
        fields = ("__all__")
        read_only_fields = ("indiceAmenaza","indiceVulnerabilidad","indiceRiesgo")


    
    def create(self, datos):
        """ Validamos que exista la comunidad y/o el consejo comunal """
        
        self.validar_consejo_comunidad(datos)
        
        if "consejoComunal" in datos.keys() and datos.get("consejoComunal") is not None:
            datos.update({"indiceVulnerabilidad":datos.get("consejoComunal").indiceVulnerabilidad})
            datos.update({"indiceAmenaza":datos.get("consejoComunal").indiceAmenaza})
            datos.update({"indiceRiesgo":datos.get("consejoComunal").indiceRiesgo})
            if "comunidad" in datos.keys():
                datos.update({"comunidad":None})
                

        elif "comunidad" in datos.keys() and datos.get("comunidad") is not None:
            datos.update({"indiceVulnerabilidad":datos.get("comunidad").indiceVulnerabilidad})
            datos.update({"indiceAmenaza":datos.get("comunidad").indiceAmenaza})
            datos.update({"indiceRiesgo":datos.get("comunidad").indiceRiesgo})
            if "consejoComunal" in datos.keys():
                datos.update({"consejoComunal":None})
                       
        
        """ pop geom from datos """
        geom = datos.pop("geom")
        """ geom is transform to native data type django"""
        
        geom = json.loads(geom)
        objeto = Vivienda(**datos)
        if geom is not None:
            objeto.geom = Point(geom)  
        objeto.save()
        return objeto
        
        
    
    def update(self, instance, datos):
        
        self.validar_consejo_comunidad(datos)
        
        if "consejoComunal" in datos.keys() and datos.get("consejoComunal") is not None:
            if datos.get("consejoComunal") != instance.consejoComunal:
                instance.indiceVulnerabilidad = datos.get("consejoComunal").indiceVulnerabilidad
                instance.indiceAmenaza = datos.get("consejoComunal").indiceAmenaza
                instance.indiceRiesgo = datos.get("consejoComunal").indiceRiesgo
                if "comunidad" in datos.keys():
                    datos.update({"comunidad":None})

        elif "comunidad" in datos.keys() and datos.get("comunidad") is not None:
            if datos.get("comunidad") != instance.comunidad:
                instance.indiceVulnerabilidad = datos.get("comunidad").indiceVulnerabilidad
                instance.indiceAmenaza = datos.get("comunidad").indiceAmenaza
                instance.indiceRiesgo = datos.get("comunidad").indiceRiesgo
                if "consejoComunal" in datos.keys():
                    datos.update({"consejoComunal":None})
        
        """ pop geom from datos """
        
        geom = datos.pop("geom")
        
        """ geom is transform to native data type django"""
        
        geom = json.loads(geom)
        if geom is not None:
            instance.geom = Point(geom)    
        
        for key,value in datos.items():
            setattr(instance, key, value)  
        instance.save()
        return instance
        
        

    def validar_consejo_comunidad(self,datos):

        claves = datos.keys()
        
        if "consejoComunal" not in claves and "comunidad" not in claves:
            raise ValidationError("Consejo Comunal y/o Comunidad deben estar presente")

        elif ("consejoComunal" not in claves) and ("comunidad" in claves and datos.get("comunidad") is None):
            raise ValidationError("Consejo Comunal y/o Comunidad no puede ser null")

        elif ("consejoComunal" in claves and datos.get("consejoComunal") is None) and ("comunidad" in claves and datos.get("comunidad") is None):
            raise ValidationError("Consejo Comunal y/o Comunidad no puede ser null")                    

        elif ("consejoComunal" in claves and datos.get("consejoComunal") is None) and ("comunidad" not in claves):
            raise ValidationError("Consejo Comunal y/o Comunidad no puede ser null")


    
class ViviendaListSerializador(serializers.ModelSerializer):
    
    link = serializers.HyperlinkedIdentityField(view_name='vivienda-detail', format='html')
    

    class Meta:
        model = Vivienda
        fields = ("__all__")
        read_only_fields = ("indiceAmenaza","indiceVulnerabilidad","indiceRiesgo")