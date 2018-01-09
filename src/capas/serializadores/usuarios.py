from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError



class UsuarioSerializador(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "is_active")
    
    
    def create(self, datos):
        objeto = User.objects.create(**datos)
        return objeto

    def update(self, instance, datos):
      
        for key,value in datos.items():
            setattr(instance, key, value)
        
      
        instance.save()
        return instance
    
    
           

class UsuarioListSerializador(serializers.ModelSerializer):
    
    link = serializers.HyperlinkedIdentityField(view_name='user-detail', format='html')
    
    
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "is_active", "link", "Casos")

