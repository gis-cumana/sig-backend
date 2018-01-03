from capas.models import Casos
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import datetime, date, time
from .usuarios import UsuarioSerializador

class CasosSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = Casos
        fields = ("__all__")
        read_only_fields = ("visible", "fecha_creado","hora_creado","geom")
    
    
    def create(self, datos):
        #import pdb
        #pdb.set_trace()
        datos.update({'visible':False})
        """ Los geom son null para probar funcionalidades """
        datos = self.validar_fecha_hora(**datos)
        objeto = Casos.objects.create(**datos)
        return objeto


    
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
            raise ValidationError({'Error': 'La fecha del Casos debe ser menor a %s' % (fecha)})
        elif datos.get('fecha') == fecha and datos.get('hora') > hora:
                raise ValidationError({'Error': 'La fecha y hora del Casos deben ser menor a la fecha y hora actual: (%s - %s)' % (fecha, hora)})
        return datos       
            
                    

class CasosListSerializador(serializers.ModelSerializer):
    
    link = serializers.HyperlinkedIdentityField(view_name='casos-detail', format='html')
    usuario = UsuarioSerializador()
    
    class Meta:
        model = Casos
        fields = ("id", "descripcion", "fecha", "hora",  "fecha_creado", "hora_creado", 
            "visible", "geom",  "link", "usuario")

