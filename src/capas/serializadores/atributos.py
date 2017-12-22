from capas.models import Atributos, crear_modelo
from rest_framework import serializers
from django.contrib.gis.db import models
from capas.esquema_manager import EsquemaManager
from django.db import connection
from rest_framework.exceptions import ValidationError
from django.db import transaction


class AtributoListarSerializador(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='atributos-detail', format='html')
    class Meta:
        model = Atributos
        fields = ("id", "nombre", "tipo", "descripcion","eliminable", "modificable", "link",)

class AtributoSerializador(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='atributos-detail', format='html')
    tipo = serializers.ChoiceField(choices=(Atributos.TEXTO, Atributos.ENTERO, Atributos.FLOTANTE))
    class Meta:
        model = Atributos
        fields = ("__all__")

    def definir_tipo(self, obj):
        if obj.tipo == Atributos.TEXTO:
            return models.CharField(max_length=255, db_column=obj.nombre)
        elif obj.tipo == Atributos.ENTERO:
            return models.IntegerField(db_column=obj.nombre)
        elif obj.tipo == Atributos.FLOTANTE:
            return models.FloatField(db_column=obj.nombre)

    @transaction.atomic
    def create(self, datos):
        nombre = datos.pop("nombre").replace('.', '_').replace(" ", "_").lower()
        datos.update({"nombre": nombre})
        obj = Atributos.objects.create(**datos)

        modelo = crear_modelo(obj.capa.nombre)

        esquema = EsquemaManager(connection)
        campo = self.definir_tipo(obj)
        esquema.agregar_columna(modelo, campo)
        return obj

    @transaction.atomic
    def update(self, obj, datos):
        modelo = crear_modelo(obj.capa.nombre)
        esquema = EsquemaManager(connection)

        nombre = datos.pop("nombre").replace('.', '_').replace(" ", "_").lower()
        tipo = obj.tipo
        if tipo == datos.get("tipo"):
            tipo = None
        elif tipo == Atributos.TEXTO and datos.get("tipo") != Atributos.TEXTO:
            error = {
                        "tipo": "no se puede cambiar de tipo texto a un valor entero o flotante"
                    }
            raise ValidationError(error)
        else:
            tipo = datos.get("tipo")

        esquema.editar_columna(modelo, obj.nombre, nombre, tipo=tipo)
        obj.nombre = nombre
        obj.tipo = tipo
        obj.descripcion = datos.get("descripcion")
        obj.save()
        return obj