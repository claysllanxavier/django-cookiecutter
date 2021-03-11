from django.urls import include, path
from rest_framework import routers

from .api_views import UsuarioViewAPI, UsuarioGETAPI

router = routers.DefaultRouter()

# URL para a API Usuario
router.register(r'usuario', UsuarioViewAPI, 'usuario-api')
router.register(r'usuario-get', UsuarioGETAPI, 'usuario-get-api')

urlpatterns = router.urls
