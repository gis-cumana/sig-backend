from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from capas.serializadores.grupos import GruposSerializador, GruposListSerializador


class GruposRecursos(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GruposSerializador  
    
    permission_classes = (IsAuthenticated,)    

    def get_serializer_class(self):
        
        if self.action in ['list', "retrieve"]:
            return GruposListSerializador
        return GruposSerializador
         
    
    def destroy(self, request, *args, **kwargs):
        objeto = self.get_object()
        

        if  objeto.usuarios.exists(): 
            respuesta = {
                "mensaje": "Grupo no se puede eliminar, tiene usuarios asociados"
            }
            return Response(respuesta,status=400)

        self.perform_destroy(objeto)
        return Response(status=204)
    
    
