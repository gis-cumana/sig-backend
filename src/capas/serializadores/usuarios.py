"""
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from capas.models import Usuario
from rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from .grupos import GruposSerializador
from django.db import transaction

try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists, get_username_max_length)
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
    from allauth.socialaccount.helpers import complete_social_login
    from allauth.socialaccount.models import SocialAccount
    from allauth.socialaccount.providers.base import AuthProcess
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")



class UsuarioSerializador(serializers.ModelSerializer):
    
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    

    class Meta:
        model = Usuario
        fields = ("id", "email", "username", "password","password2")       

        

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise ValidationError("Ya existe un usuario registrado con este correo")
        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(("La clave no coincide, repita la clave"))
        return data

    def custom_signup(self, request, user):
        pass
    
    def get_cleaned_data(self):
        nombre = self.validated_data.get('username', '') 
        if nombre is None:
            nombre = self.data.get('email')
            
        return {
            'username': nombre,
            'password': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        adapter = get_adapter()    
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
    
    
class UserSerializer(UserDetailsSerializer):


    
    institucion = serializers.CharField(source="usuario.institucion")
    grupos = serializers.CharField(source="usuario.grupos")
    
    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields  + ("institucion", "grupos",)    
       

    @transaction.atomic    
    def update(self, instance, validated_data):

       
        usuario_data = validated_data.pop('usuario', {})
        institucion = usuario_data.get('institucion')
        grupos = usuario_data.get('grupos')

        
        grupos = Group.objects.filter(name=grupos)
        
        if not grupos:
            raise serializers.ValidationError(("El grupo asignado no existe"))


        instance = super(UserSerializer, self).update(instance, validated_data)

        try:
            usuario = instance.usuario
        except ObjectDoesNotExist:
            usuario = Usuario()

        
    
        if usuario_data and institucion and grupos:
            usuario.institucion = institucion
            usuario.grupos = grupos.get()
            usuario.user_id = instance.id
            usuario.save()

        return instance



class UserDetailsSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = User

        fields = ('first_name', 'last_name', 'is_active',)
        read_only_fields = ('username','email',)



"""
from rest_framework import serializers
from django.contrib.auth.models import User
from capas.models import Usuario
from allauth.account.adapter import get_adapter
from allauth.account import app_settings as allauth_settings
from allauth.utils import (email_address_exists)
from allauth.account.utils import setup_user_email

from django.db import transaction

class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True, source="user.email")
    password = serializers.CharField(required=True, style={'input_type': 'password'}, source="user.password")
    first_name = serializers.CharField(required=True, source="user.first_name")
    last_name = serializers.CharField(required=True, source="user.last_name")

    class Meta:
        model = Usuario
        fields = ("id", "institucion", "email", "password", "first_name", "last_name",)

    def save(self, request):
        return Usuario()

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    ("A user is already registered with this e-mail address."))
        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def get_cleaned_data(self):
        user = self.validated_data.get("user")
        return {
            'password1': user.get('password', ''),
            'email': user.get('email', ''),
            'first_name': user.get('first_name', ''),
            'last_name': user.get('last_name', ''),
            'institucion': self.validated_data.get('institucion', '')
        }

    @transaction.atomic
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        Usuario.objects.create(user=user, rol="Usuario", institucion=self.cleaned_data.get("institucion"))
        setup_user_email(request, user, [])
        return user

class UserDetailsSerializer(serializers.ModelSerializer):
    institucion = serializers.CharField(required=True, source="usuario.institucion")
    rol = serializers.CharField(read_only=True, source="usuario.rol")

    class Meta:
        model = User
        fields = ('pk', 'email', 'first_name', 'last_name', 'institucion', 'rol')
        read_only_fields = ('email',)

    def update(self, instance, data):
        usuario = data.pop("usuario")
        for key, value in data.items():
            setattr(instance, key, value)
        instance.first_name.title()
        instance.last_name.title()
        instance.save()
        instance.usuario.institucion = usuario.get("institucion")
        instance.usuario.save()
        return instance
