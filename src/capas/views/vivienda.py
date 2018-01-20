from rest_framework import viewsets, status
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from capas.models import Vivienda
from capas.serializadores import ViviendaSerializador, ViviendaListSerializador




class ViviendaRecursos(viewsets.ModelViewSet):
    
    queryset = Vivienda.objects.all()
    serializer_class = ViviendaSerializador

    def get_serializer_class(self):
        
        if self.action in ['list', "retrieve"]:
            return ViviendaListSerializador
        return ViviendaSerializador
         
    
    def destroy(self, request, *args, **kwargs):
        
        objeto = self.get_object()
        
        self.perform_destroy(objeto)
        return Response(status=204)          
        
    



