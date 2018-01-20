from rest_framework import viewsets, status
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from capas.models import Censo
from capas.serializadores import CensoSerializador, CensoListSerializador




class CensoRecursos(viewsets.ModelViewSet):
    
    queryset = Censo.objects.all()
    serializer_class = CensoSerializador

    def get_serializer_class(self):
        
        if self.action in ['list', "retrieve"]:
            return CensoListSerializador
        return CensoSerializador
         
    
    def destroy(self, request, *args, **kwargs):
        
        objeto = self.get_object()
        
        self.perform_destroy(objeto)
        return Response(status=204)          
        
    



