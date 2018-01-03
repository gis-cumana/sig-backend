from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from .enrrutador import RaizRouter
from capas.views import CapasRecursos, CategoriasRecursos,\
                        AtributosRecursos, ParametrosRecursos
from capas.views import CasosRecursos
from capas.views import UsuariosRecursos
from capas.views import TipologiaRecursos

router = RaizRouter(trailing_slash=False)
router.register("capas", CapasRecursos)
router.register("categorias", CategoriasRecursos)
router.register("atributos", AtributosRecursos)
router.register("parametros", ParametrosRecursos)
router.register("casos", CasosRecursos)
router.register("tipologias", TipologiaRecursos)
router.register("usuarios", UsuariosRecursos)

urlpatterns = [
    url(r'^', include(router.urls)),
]