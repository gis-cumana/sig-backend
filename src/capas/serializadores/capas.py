from capas.models import Capas, Atributos
from rest_framework import serializers
from .categorias import CategoriaSerializador
from capas.capa_utils import CapaImporter
from .atributos import AtributoListarSerializador


class CapaListSerializador(serializers.ModelSerializer):
    atributos = AtributoListarSerializador(many=True)
    link = serializers.HyperlinkedIdentityField(view_name='capas-detail', format='html')
    categoria = CategoriaSerializador()
    class Meta:
        model = Capas
        fields = ("id", "nombre", "atributos", "tipo", "categoria", "link")

class CapaSerializador(serializers.ModelSerializer):
    atributos = AtributoListarSerializador(many=True)
    tipo = serializers.ChoiceField(choices=(Atributos.GEOMETRICOS))
    class Meta:
        model = Capas
        fields = ("id", "nombre", "tipo", "categoria", "atributos")

    def create(self, datos):
        nombre = datos.pop("nombre").replace('.', '_').replace(" ", "_").lower()
        obj = Capas.objects.create(categoria=datos.get("categoria"),
                                   nombre=nombre, tipo=datos.get("tipo"))
        self.registrar_geom(obj, obj.tipo)
        importer = CapaImporter(None, obj.nombre, obj.categoria_id, verificar_nombre=False)
        importer.desde_tabla(obj)
        return obj

    def registrar_geom(self, obj, tipo):
        geom = {
            "nombre": "geom",
            "tipo": tipo,
            "capa": obj,
            "descripcion": "campo geometrico de la capa"
        }
        Atributos.objects.create(**geom)

    def update(self, instance, datos):
        tipo = datos.pop("tipo")
        for key, value in datos.items():
            setattr(instance, key, value)
        instance.nombre.replace('.', '_').replace(" ", "_").lower()
        instance.save()
        return instance

