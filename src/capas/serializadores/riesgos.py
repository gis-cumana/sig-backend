from capas.models import GeoUnidad, Riesgos
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point, Polygon
import pygeoj
import json
from django.db import transaction



class RiesgosSerializador(serializers.ModelSerializer):

    class Meta:
        model = Riesgos
        fields = ("id","indiceAmenaza", "indiceVulnerabilidad", "indiceRiesgo","anyo", "fuente", "geounidad")
        read_only_fields = ("indiceModificado", "activo")
        

    def create(self, datos):
        with transaction.atomic():    
            """ Busca el riesgo activo para la geounidad seleccionada """
            riesgoActivo = Riesgos.objects.filter(activo=True,geounidad=datos.get("geounidad"))        
            if riesgoActivo.exists():
                riesgoActivo = riesgoActivo.get()
                riesgoActivo.activo = False
                riesgoActivo.save()

            datos.update({"activo":True})        
            objeto = Riesgos.objects.create(**datos)        
        
            for key,value in datos.items():
                if key not in ["id","geounidad","activo"]:
                    setattr(objeto.geounidad, key, value)
            objeto.geounidad.save()
        return objeto


    def update(self, instance, datos):
        with transaction.atomic():    
            modificado = ""
            for key,value in datos.items():
                setattr(instance, key, value)
                if key in ["indiceAmenaza", "indiceVulnerabilidad"]:
                    if instance.indiceAmenaza != value: 
                        modificado = modificado + key
                    elif  instance.indiceVulnerabilidad != value:    
                        modificado = modificado + key
                    modificado = modificado + ","    
                    setattr(instance, "indiceModificado",modificado)
                if key not in ["id","geounidad","activo"]:
                    setattr(instance.geounidad, key, value)
            instance.save()
            instance.geounidad.save()
            

        return instance
           

class RiesgosListSerializador(serializers.ModelSerializer):
    
    link = serializers.HyperlinkedIdentityField(view_name='riesgos-detail', format='html')
    class Meta:
        model = Riesgos
        fields = ("id","indiceAmenaza", "indiceVulnerabilidad", "indiceRiesgo","indiceModificado","anyo", "fuente", "geounidad", "activo", "link")

class RiesgosGeoUnidadSerializador(serializers.ModelSerializer):

    class Meta:
        model = Riesgos
        fields = ("indiceAmenaza", "indiceVulnerabilidad", "indiceRiesgo","anyo", "fuente")