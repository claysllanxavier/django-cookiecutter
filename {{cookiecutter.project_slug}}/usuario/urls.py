from django.urls import include, path
from rest_framework import routers

from .views import (UsuarioCreateView, UsuarioDeleteView, UsuarioDetailView,
                    UsuarioIndexTemplateView, UsuarioListView,
                    UsuarioUpdateView)

app_name = 'usuario'

# URLs do Models Usuario
urlpatterns = [
    path('api/usuario/', include('usuario.api_urls')),
    path('usuario/', UsuarioIndexTemplateView.as_view(), name='usuario-index'),
    path('usuario/usuario/', UsuarioListView.as_view(), name='usuario-list'),
    path('usuario/usuario/create/', UsuarioCreateView.as_view(), name='usuario-create'),
    path('usuario/usuario/<uuid:pk>/', UsuarioDetailView.as_view(), name='usuario-detail'),
    path('usuario/usuario/update/<uuid:pk>/', UsuarioUpdateView.as_view(), name='usuario-update'),
    path('usuario/usuario/delete/<uuid:pk>/', UsuarioDeleteView.as_view(), name='usuario-delete'),
]
