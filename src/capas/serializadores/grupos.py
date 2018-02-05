from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.exceptions import ValidationError



class GruposSerializador(serializers.ModelSerializer):
    
      
    link = serializers.HyperlinkedIdentityField(view_name='group-detail', format='html')
    
    class Meta:
        model = Group
        fields = ("name","link",)       



class GruposListSerializador(serializers.ModelSerializer):
    
      
    link = serializers.HyperlinkedIdentityField(view_name='group-detail', format='html')

    class Meta:
        model = Group
        fields = ("name","link", "usuarios", )       