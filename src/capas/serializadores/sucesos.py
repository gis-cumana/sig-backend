from capas.models import Suceso
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import datetime, date, time


class SucesoSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = Suceso
        fields = ("id", "descripcion", "fecha", "hora", "tipo", "visible", "geom", "tipo", "usuario")
    
    
    def create(self, datos):
        datos = self.validar_fecha_hora(**datos)
        suceso = Suceso.objects.create(**datos)
        return suceso


    
    def update(self, instance, datos):
        datos = self.validar_fecha_hora(**datos)
        for key,value in datos.items():
            setattr(instance, key, value)
        
        instance.save()
        return instance
    
    
    def validar_fecha_hora(self, **datos): 
        actual = datetime.now()
        fecha = date.today()
        hora = time(actual.hour, actual.minute, actual.second)
        claves = datos.keys()
        
        if  'fecha' not in claves:
            datos.update({'fecha':fecha})
        elif datos.get('fecha') is None:
            setattr(datos, 'fecha', fecha)
        
        if 'hora' not in claves:
            datos.update({'hora':hora})
        elif datos.get('hora') is None:
            setattr(datos, 'hora', hora)    
        
        datos.update({'fecha_creado':fecha})
        datos.update({'hora_creado':hora})

        if datos.get('fecha') > fecha:
            raise ValidationError({'Error': 'La fecha del suceso debe ser menor a %s' % (fecha)})
        elif datos.get('fecha') == fecha and datos.get('hora') > hora:
                raise ValidationError({'Error': 'La fecha y hora del suceso deben ser menor a la fecha y hora actual: (%s - %s)' % (fecha, hora)})
        return datos       
            
                    

class SucesoListSerializador(serializers.ModelSerializer):
    from .usuarios import UsuarioSerializador
    link = serializers.HyperlinkedIdentityField(view_name='suceso-detail', format='html')
    usuario = UsuarioSerializador()
    
    class Meta:
        model = Suceso
        fields = ("id", "descripcion", "fecha", "hora", "tipo", "fecha_creado", "hora_creado", 
            "visible", "geom", "tipo", "link", "usuario")

