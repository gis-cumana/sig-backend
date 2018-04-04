"""
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from capas.models import Usuario
from capas.serializadores import UsuarioSerializador

class UsuariosRecursos(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializador

    def get_serializer_class(self):
        if self.action in ['list', "retrieve"]:
            return UsuarioSerializador
        return UsuarioSerializador

"""