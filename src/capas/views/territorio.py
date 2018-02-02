from rest_framework import viewsets, status
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from capas.models import Territorio
from capas.serializadores import TerritorioSerializador, TerritorioListSerializador




class TerritorioRecursos(viewsets.ModelViewSet):
    
    queryset= Territorio.objects.all()
    serializer_class = TerritorioSerializador

    def get_serializer_class(self):
       	if self.action in ['list', "retrieve"]:
            return TerritorioListSerializador
        return TerritorioSerializador
    
    """
    @list_route(methods=['get'], url_path=r'territorio/(?P<tipo>[^/]+)')    
    def get_queryset(self):
      	tipo = self.kwargs['tipo']
    	return Territorio.objects.filter(tipo=tipo)

    """    
    
