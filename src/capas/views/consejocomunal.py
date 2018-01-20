from rest_framework import viewsets, status
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from capas.models import ConsejoComunal
from capas.serializadores import ConsejoComunalSerializador, ConsejoComunalListSerializador




class ConsejoComunalRecursos(viewsets.ModelViewSet):
    
    queryset = ConsejoComunal.objects.all()
    serializer_class = ConsejoComunalSerializador

    def get_serializer_class(self):
        
        if self.action in ['list', "retrieve"]:
            return ConsejoComunalListSerializador
        return ConsejoComunalSerializador
         
    
    def destroy(self, request, *args, **kwargs):
        
        objeto = self.get_object()
        
        self.perform_destroy(objeto)
        return Response(status=204)          
        
    



