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
        objecto = self.get_object()
        objecto.is_active = False
        objecto.save()
        #self.perform_destroy(objecto)
        return Response(status=204)

        
    

    

