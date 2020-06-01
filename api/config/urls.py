from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from config.integrador.views import config
from config.api.views import AbastecimentoViewSet, OSAutomotivaViewSet

router = routers.DefaultRouter()
router.register(r'abastecimentos', AbastecimentoViewSet)
router.register(r'osautomotivas', OSAutomotivaViewSet)

urlpatterns = [
    path('', config),
    path('admin/', admin.site.urls),
    path('integrador/', include('config.integrador.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls))
]
