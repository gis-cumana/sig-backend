from rest_framework import viewsets
from capas.models import Casos
from rest_framework.response import Response
from capas.serializadores.casos import CasosSerializador, CasosListSerializador
#from rest_framework import permissions

class CasosRecursos(viewsets.ModelViewSet):
    queryset = Casos.objects.all()
    serializer_class = CasosSerializador
    #permissions_classes =  (permissions.IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CasosListSerializador
        return CasosSerializador

    def destroy(self, request, *args, **kwargs):
        objecto = self.get_object()
        self.perform_destroy(objecto)
        return Response(status=204)
    

