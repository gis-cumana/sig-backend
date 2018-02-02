from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from capas.models import Usuario
from rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

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
        read_only_fields=("username", )        

        

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

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('institucion',)  

    def update(self, instance, validated_data):

        usuario_data = validated_data.pop('usuario', {})
        institucion = usuario_data.get('institucion')
        
        instance = super(UserSerializer, self).update(instance, validated_data)

        try:
            usuario = instance.usuario
        except ObjectDoesNotExist:
            usuario = Usuario()

        if usuario_data and institucion:
            usuario.institucion = institucion
            usuario.user_id = instance.id
            usuario.save()
        return instance


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()

        fields = ('username','email', 'first_name', 'last_name')
        read_only_fields = ('username','email',)


class UsuarioListSerializador(serializers.ModelSerializer):
    
    link = serializers.HyperlinkedIdentityField(view_name='user-detail', format='html')
    
    
    class Meta:
        model = Usuario
        fields = ("id", "email","username", "first_name", "last_name",  "is_active", "role","fechaCreacion","link")

