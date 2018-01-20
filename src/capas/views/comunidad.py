from rest_framework import viewsets, status
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from capas.models import Comunidad
from capas.serializadores import ComunidadSerializador, ComunidadListSerializador




class ComunidadRecursos(viewsets.ModelViewSet):
    
    queryset = Comunidad.objects.all()
    serializer_class = ComunidadSerializador

    def get_serializer_class(self):
        
        if self.action in ['list', "retrieve"]:
            return ComunidadListSerializador
        return ComunidadSerializador
         
    
    def destroy(self, request, *args, **kwargs):
        objeto = self.get_object()
        
        if not objeto.eliminable: 
            respuesta = {
                "mensaje": "Comunidad no se puede eliminar, tiene viviendas asociadas"
            }
            return Response(respuesta,status=400)

        self.perform_destroy(objeto)
        return Response(status=204)          
    



