from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from .enrrutador import RaizRouter
from capas.views import CapasRecursos, CategoriasRecursos,\
                        AtributosRecursos, ParametrosRecursos, ImagenRecursos
from capas.views import CasosRecursos
from capas.views import UsuariosRecursos
from capas.views import TipologiaRecursos
from capas.views import TerritorioRecursos, GeoUnidadRecursos, ComunidadRecursos, RiesgosRecursos
from capas.views import ViviendaRecursos, CentroSaludEmergenciaRecursos, CentroEducativoRecursos 
from capas.views import ConsejoComunalRecursos, CensoRecursos
from capas.views import GruposRecursos


from django.conf import settings
from django.conf.urls.static import static

router = RaizRouter(trailing_slash=False)

router.register("capas", CapasRecursos)
router.register("categorias", CategoriasRecursos)
router.register("atributos", AtributosRecursos)
router.register("parametros", ParametrosRecursos)
router.register("casos", CasosRecursos)
router.register("tipologias", TipologiaRecursos)
router.register("usuarios", UsuariosRecursos)
router.register("imagenes", ImagenRecursos)
router.register("geounidades", GeoUnidadRecursos)
router.register("comunidades", ComunidadRecursos)
router.register("riesgos", RiesgosRecursos)
router.register("viviendas", ViviendaRecursos)
router.register("centrosSaludEmergencias", CentroSaludEmergenciaRecursos)
router.register("centrosEducativos", CentroEducativoRecursos)
router.register("consejosComunales", ConsejoComunalRecursos)
router.register("censos", CensoRecursos)
router.register("territorios", TerritorioRecursos)
router.register("grupos", GruposRecursos)

urlpatterns = [
    url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    #url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls))
        
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)