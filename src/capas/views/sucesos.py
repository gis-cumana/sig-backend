from rest_framework import viewsets
from capas.models import Suceso
from rest_framework.response import Response
from capas.serializadores.sucesos import SucesoSerializador, SucesoListSerializador
#from rest_framework import permissions

class SucesosRecursos(viewsets.ModelViewSet):
    queryset = Suceso.objects.all()
    serializer_class = SucesoSerializador
    #permissions_classes =  (permissions.IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SucesoListSerializador
        return SucesoSerializador

    def destroy(self, request, *args, **kwargs):
        objecto = self.get_object()
        self.perform_destroy(objecto)
        return Response(status=204)
    

