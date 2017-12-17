from capas.models import Atributos
from rest_framework import serializers

class AtributoListarSerializador(serializers.ModelSerializer):
    class Meta:
        model = Atributos
        fields = ("id", "nombre", "tipo", "descripcion", )

class AtributoSerializador(serializers.ModelSerializer):
    class Meta:
        model = Atributos
        fields = ("__all__")

    def create(self, datos):
        nombre = datos.pop("nombre").replace('.', '_').replace(" ", "_").lower()
        obj = Atributos.objects.create(**datos, nombre=nombre)
        return obj

    def update(self, instance, datos):
        for key, value in datos.items():
            setattr(instance, key, value)
        instance.nombre.replace('.', '_').replace(" ", "_").lower()
        instance.save()
        return instance