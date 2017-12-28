from rest_framework import viewsets
from capas.models import Categoria, Parametro
from rest_framework.response import Response
from capas.serializadores.parametros import ParametroSerializador, ParametroListSerializador

class ParametrosRecursos(viewsets.ModelViewSet):
    queryset = Parametro.objects.all()
    serializer_class = ParametroSerializador

    def get_serializer_class(self):
        if self.action in ['list', "retrieve"]:
            return ParametroListSerializador
        return ParametroSerializador
   
   
    def destroy(self, request, *args, **kwargs):
        objecto = self.get_object()

        if not objecto.eliminable:
            respuesta = {
                "mensaje": "El parametro no se puede eliminar, tiene capas asociadas"
            }
            return Response(respuesta,status=400)
        self.perform_destroy(objecto)
        return Response(status=204)
    

