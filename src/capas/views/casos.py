from rest_framework import viewsets
from capas.models import Casos, Imagen
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from capas.serializadores.casos import CasosSerializador, CasosListSerializador, ImagenSerializador
from django.db import transaction
from rest_framework.decorators import list_route
from rest_framework.exceptions import ValidationError

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

    @transaction.atomic
    @list_route(methods=['put'], url_path=r'(?P<id_caso>[^/]+)/visible', permission_classes=[AllowAny])
    def visible(self, request, id_caso):
        caso = queryset.filter(id=id_caso).first()
        if caso is None:
            raise ValidationError({"mensaje": "caso no existe"})
        caso.visible = not caso.visible
        caso.save()
        return Response()