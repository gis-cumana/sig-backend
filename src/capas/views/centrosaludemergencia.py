from rest_framework import viewsets, status
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from capas.models import CentroSaludEmergencia
from capas.serializadores import CentroSaludEmergenciaSerializador, CentroSaludEmergenciaListSerializador




class CentroSaludEmergenciaRecursos(viewsets.ModelViewSet):
    
    queryset = CentroSaludEmergencia.objects.all()
    serializer_class = CentroSaludEmergenciaSerializador

    def get_serializer_class(self):
        
        if self.action in ['list', "retrieve"]:
            return CentroSaludEmergenciaListSerializador
        return CentroSaludEmergenciaSerializador
         
    
    def destroy(self, request, *args, **kwargs):
        
        objeto = self.get_object()
        
        self.perform_destroy(objeto)
        return Response(status=204)          
        
    



