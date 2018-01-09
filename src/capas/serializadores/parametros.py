from capas.models import Categoria, Parametro
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class ParametroSerializador(serializers.ModelSerializer):
    class Meta:
        model = Parametro
        fields = ("id", "nombre", "tipo", "eliminable", "categoria")
    
    
    def create(self, datos):
        nombre = datos.get('nombre').lower().replace('.', '_').replace(" ", "_")
        datos.update({'nombre': nombre})
        parametro = Parametro.objects.create(**datos)
        return parametro

    def update(self, instance, datos):
        
        categoria = datos.pop('categoria')
        nombre = datos.get('nombre').lower().replace('.', '_').replace(" ", "_")
        datos.update({'nombre': nombre})
        newtipo = datos.get('tipo')
        
        instance = self.valida_tipo(instance,newtipo)
        for key,value in datos.items():
            setattr(instance, key, value)
        
        setattr(instance, 'categoria', categoria)
        instance.save()
        return instance
    
    def valida_tipo(self,objeto,newtipo):
        """ Valida los cambios de Tipo """
        if objeto.tipo == newtipo:
            return objeto
        elif objeto.tipo in [Parametro.ENTERO] and newtipo in [Parametro.ENTERO, Parametro.FLOTANTE]:            
            setattr(objeto, 'tipo', newtipo)
            return objeto
        elif objeto.tipo in [Parametro.DATE, Parametro.DATETIME] and newtipo in [Parametro.DATE, Parametro.DATETIME]: 
            setattr(objeto, 'tipo', newtipo)
            return objeto
        else:    
            error = {
                "tipo": "no se puede cambiar de tipo %s a un valor %s" % (objeto.tipo, newtipo)
            }
        raise ValidationError(error)
           

class ParametroListSerializador(serializers.ModelSerializer):
    from .categorias import CategoriaSerializador
    link = serializers.HyperlinkedIdentityField(view_name='parametro-detail', format='html')
    categoria = CategoriaSerializador()
    
    class Meta:
        model = Parametro
        fields = ("id","nombre","tipo", "link", "eliminable", "categoria")

class ParametroCategoriaSerializador(serializers.ModelSerializer):
    from .categorias import CategoriaSerializador
    link = serializers.HyperlinkedIdentityField(view_name='parametro-detail', format='html')
    
    class Meta:
        model = Parametro
        fields = ("id","nombre","tipo", "link", "eliminable",)

