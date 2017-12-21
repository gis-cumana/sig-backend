from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from .enrrutador import RaizRouter
from capas.views import CapasRecursos, CategoriasRecursos,\
                        AtributosRecursos

router = RaizRouter(trailing_slash=False)
router.register("capas", CapasRecursos)
router.register("categorias", CategoriasRecursos)
router.register("atributos", AtributosRecursos)

urlpatterns = [
    url(r'^', include(router.urls)),
]