""" 
Arquivo de URLS da API da aplicação.
Todas as urls relativas à APIRest devem ser colocadas neste arquivo, e devem
seguir o padrão apresentado a seguir:

    path('nome_da_app/api/v1/', include('nome_da_app.api_urls')),

"""

from django.urls import path, include

urlpatterns = [
    path('usuario/api/v1/', include('usuario.api_urls')),
]