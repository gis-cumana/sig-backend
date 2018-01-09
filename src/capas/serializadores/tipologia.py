from capas.models import TipologiaConstructiva
from rest_framework import serializers

class TipologiaSerializador(serializers.ModelSerializer):
    class Meta:
        model = TipologiaConstructiva
        fields = ("__all__")

    def create(self, datos):
        
        objeto = TipologiaConstructiva.objects.create(**datos)
        return objeto

    def update(self, instance, datos):
        
        for key,value in datos.items():
            setattr(instance, key, value)  
        instance.save()
        return instance

class TipologiaListSerializador(serializers.ModelSerializer):
    
    link = serializers.HyperlinkedIdentityField(view_name='tipologiaconstructiva-detail', format='html')
    #link = serializers.HyperlinkedIdentityField(view_name='casos-detail', format='html')
    class Meta:
        model = TipologiaConstructiva
        fields = ("id", "nombre", "descripcion", "anyo", "link")
