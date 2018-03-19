"""
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from capas.models import Usuario

class UsuariosRecursos(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UserDetailsSerializer

    def get_serializer_class(self):
        if self.action in ['list', "retrieve"]:
            return UserDetailsSerializer
        return UserDetailsSerializer
   
   
    def destroy(self, request, *args, **kwargs):
        objeto = self.get_object()
        objeto.is_active = False
        objeto.save()
        #self.perform_destroy(objecto)
        return Response(status=204)   
"""
    

