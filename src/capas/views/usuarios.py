from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from capas.serializadores.usuarios import UsuarioSerializador, UsuarioListSerializador

class UsuariosRecursos(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializador

    def get_serializer_class(self):
        if self.action in ['list', "retrieve"]:
            return UsuarioListSerializador
        return UsuarioSerializador
   
    
    def destroy(self, request, *args, **kwargs):
        objeto = self.get_object()
        objeto.is_active = False
        objeto.save()
        #self.perform_destroy(objecto)
        return Response(status=204)

        
    

    

