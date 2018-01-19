from capas.models import GeoUnidad, Territorio
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class TerritorioSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = Territorio
        fields = ("__all__")

    """        
    def create(self, datos):
        datos.update({'tipo':'MUNICIPIO'})
        objeto = Territorio.objects.create(**datos)
        return objeto

    
    def update(self, instance, datos):
        
        for key,value in datos.items():
            setattr(instance, key, value)  
        instance.save()
        return instance
    """
class TerritorioListSerializador(serializers.ModelSerializer):
    
    link = serializers.HyperlinkedIdentityField(view_name='territorio-detail', format='html')
    
    class Meta:
        model = Territorio
        fields = ("__all__")        