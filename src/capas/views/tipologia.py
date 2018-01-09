from rest_framework import viewsets, status
from capas.models import TipologiaConstructiva
from rest_framework.response import Response
from capas.serializadores import TipologiaSerializador, TipologiaListSerializador


class TipologiaRecursos(viewsets.ModelViewSet):
    queryset = TipologiaConstructiva.objects.all()
    serializer_class = TipologiaConstructiva

    def get_serializer_class(self):
        if self.action in ['list', "retrieve"]:
            return TipologiaListSerializador
        return TipologiaSerializador

    def destroy(self, request, *args, **kwargs):
        objecto = self.get_object()
        self.perform_destroy(objecto)
        return Response(status.HTTP_204_NO_CONTENT)

