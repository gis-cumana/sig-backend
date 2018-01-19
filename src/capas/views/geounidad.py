from rest_framework import viewsets, status
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from capas.models import GeoUnidad
from capas.serializadores import GeoUnidadSerializador, GeoUnidadListSerializador
from django.db import transaction
import json


class GeoUnidadRecursos(viewsets.ModelViewSet):
    
    queryset = GeoUnidad.objects.all()
    serializer_class = GeoUnidadSerializador

    def get_serializer_class(self):
        
        if self.action in ['list', "retrieve"]:
            return GeoUnidadListSerializador
        return GeoUnidadSerializador
         
    
    def destroy(self, request, *args, **kwargs):
        objeto = self.get_object()

        if not objeto.eliminable: 
            respuesta = {
                "mensaje": "Geounidad no se puede eliminar, tiene  comunidades asociadas y/o historico de riesgos"
            }
            return Response(respuesta,status=400)

        self.perform_destroy(objeto)
        return Response(status=204)   

    

