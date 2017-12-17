from rest_framework import viewsets
from capas.models import Categoria
from rest_framework.response import Response
from capas.serializadores import CategoriaSerializador, CategoriaListSerializador


class CategoriasRecursos(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializador

    def get_serializer_class(self):
        if self.action in ['list', "retrieve"]:
            return CategoriaListSerializador
        return CategoriaSerializador

    def destroy(self, request, *args, **kwargs):
        objecto = self.get_object()

        if not objecto.eliminable:
            respuesta = {
                "mensaje": "Categoria no se puede eliminar, tiene capas asociadas"
            }
            return Response(respuesta,status=400)
        self.perform_destroy(objecto)
        return Response(status=204)

