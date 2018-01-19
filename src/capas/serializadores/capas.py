from capas.models import Capas, Atributos
from rest_framework import serializers
from .categorias import CategoriaSerializador
from capas.capa_utils import CapaImporter
from .atributos import AtributoListarSerializador
from django.db import transaction

class CapaListSerializador(serializers.ModelSerializer):
    atributos = AtributoListarSerializador(many=True)
    link = serializers.HyperlinkedIdentityField(view_name='capas-detail', format='html')
    categoria = CategoriaSerializador()
    class Meta:
        model = Capas
        fields = ("id", "nombre", "atributos", "tipo", "categoria", "link")

class CapaCategoriaSerializador(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='capas-detail', format='html')
    class Meta:
        model = Capas
        fields = ("id", "nombre", "tipo", "link")

class CapaSerializador(serializers.ModelSerializer):
    
    tipo = serializers.ChoiceField(choices=(Atributos.GEOMETRICOS))
    class Meta:
        model = Capas
        fields = ("id", "nombre", "tipo", "categoria")

    @transaction.atomic
    def create(self, datos):
        nombre = datos.pop("nombre").replace('.', '_').replace(" ", "_").lower()
        obj = Capas.objects.create(categoria=datos.get("categoria"),
                                   nombre=nombre, tipo=datos.get("tipo"))
        geom = {
            "nombre": "geom",
            "tipo": obj.tipo,
            "capa": obj,
            "descripcion": "campo geometrico de la capa"
        }
        self.registrar_attr(geom)
        [self.registrar_attr({"nombre": i.nombre, "tipo": i.tipo,"capa": obj}) for i in obj.categoria.parametros.all()]
        importer = CapaImporter(None, obj.nombre, obj.categoria_id, verificar_nombre=False)
        importer.desde_tabla(obj)
        return obj

    def registrar_attr(self, data):
        Atributos.objects.create(**data)

    def update(self, instance, datos):
        tipo = datos.pop("tipo")
        for key, value in datos.items():
            setattr(instance, key, value)
        instance.nombre.replace('.', '_').replace(" ", "_").lower()
        instance.save()
        return instance

