from rest_framework import viewsets, status
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from capas.models import CentroEducativo
from capas.serializadores import CentroEducativoSerializador, CentroEducativoListSerializador




class CentroEducativoRecursos(viewsets.ModelViewSet):
    
    queryset = CentroEducativo.objects.all()
    serializer_class = CentroEducativoSerializador

    def get_serializer_class(self):
        
        if self.action in ['list', "retrieve"]:
            return CentroEducativoListSerializador
        return CentroEducativoSerializador
         
    
    def destroy(self, request, *args, **kwargs):
        
        objeto = self.get_object()
        
        self.perform_destroy(objeto)
        return Response(status=204)          
        
    



