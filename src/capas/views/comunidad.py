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
        """
        if not objeto.eliminable: 
            respuesta = {
                "mensaje": "Comunidad no se puede eliminar, tiene  comunidades asociadas y/o historico de riesgos"
            }
            return Response(respuesta,status=400)

        self.perform_destroy(objeto)
        return Response(status=204)    
        """ 
    """"
    @list_route(methods=['get', 'put'])
    def get(self, request):
        queryset = Comunidad.objects.all()
        data = serialize('geojson', queryset, geometry_field='geom')
        data = json.loads(data)
        return Response(data)

    """    



