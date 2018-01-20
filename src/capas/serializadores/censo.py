from capas.models import Censo
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point, Polygon
from rest_framework.exceptions import ValidationError
from datetime import datetime, date, time
import pygeoj
import json

class CensoSerializador(serializers.ModelSerializer):
    
       
    class Meta:
        model = Censo
        fields = ("__all__")
        read_only_fields = ("poblacionCenso","indiceAmenaza","indiceVulnerabilidad","indiceRiesgo")


    
    def create(self, datos):
        
        if "fecha" in datos.keys() and datos.get("fecha") > datetime.now().date():
                raise ValidationError("La fecha del censo debe ser igual o anterior a la fecha actual") 
        
        if "fecha" in datos.keys() and datos.get("fecha") is None:
            datos.update({"fecha",datetime.now().date()})
        
        objeto = Censo(**datos)
        
        """ Actualizamos los datos en el consejo Comunal """
        objeto.consejocomunal.poblacionCenso = objeto.totalHabitantes
        objeto.consejocomunal.save()
        objeto.save()

        return objeto
        
        
    
    def update(self, instance, datos):
        
        if "fecha" in datos.keys() and datos.get("fecha") > datetime.now().date():
                raise ValidationError("La fecha del censo debe ser igual o anterior a la fecha actual") 
        
        if "fecha" in datos.keys() and datos.get("fecha") is None:
            datos.update({"fecha",datetime.now().date()})
        
        """ Actualizamos los datos en el consejo comunal """
        
        for key,value in datos.items():
            setattr(instance, key, value)  
       
        if "totalHabitantes" in datos.keys():
            instance.consejocomunal.poblacionCenso = datos.get("totalHabitantes")
        
        instance.consejocomunal.save()    
        instance.save()
        return instance
        
        
class CensoListSerializador(serializers.ModelSerializer):
    
    link = serializers.HyperlinkedIdentityField(view_name='censo-detail', format='html')

    class Meta:
        model = Censo
        fields = ("__all__")
        read_only_fields = ("poblacionCenso","indiceAmenaza","indiceVulnerabilidad","indiceRiesgo","link")