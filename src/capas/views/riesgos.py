from rest_framework import viewsets, status
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from capas.models import Riesgos, GeoUnidad
from capas.serializadores import RiesgosSerializador, RiesgosListSerializador,GeoUnidadSerializador
from django.db import transaction



class RiesgosRecursos(viewsets.ModelViewSet):
    
    queryset = Riesgos.objects.all()
    serializer_class = RiesgosSerializador

    def get_serializer_class(self):
        
        if self.action in ['list', "retrieve"]:
            return RiesgosListSerializador
        return RiesgosSerializador
    
    
    def destroy(self, request, *args, **kwargs):
      
            respuesta = {
                "mensaje": "Riesgo no se puede eliminar, es un historico de Geounidad"
            }
            return Response(respuesta,status=400)

 


    