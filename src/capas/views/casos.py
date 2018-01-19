from rest_framework import viewsets
from capas.models import Casos, Imagen
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from capas.serializadores.casos import CasosSerializador, CasosListSerializador, ImagenSerializador

class CasosRecursos(viewsets.ModelViewSet):
    queryset = Casos.objects.all()
    serializer_class = CasosSerializador
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CasosListSerializador
        return CasosSerializador

    def destroy(self, request, *args, **kwargs):
        objecto = self.get_object()
        self.perform_destroy(objecto)
        return Response(status=204)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)