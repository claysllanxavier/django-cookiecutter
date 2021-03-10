from django.urls import include, path
from rest_framework import routers

from .api_views import (ClienteViewAPI, ProfissaoViewAPI, ProfissionalViewAPI, UserSendMail, ChangePasswordUser,
                        RecoverPassword, RequestResetAccount, ResetAccount, ProfissionalImageViewSet)
from .views import (ClienteCreateView, ClienteDeleteView, ClienteDetailView, ClienteListView, ClienteUpdateView,
                    ProfissaoCreateView, ProfissaoDeleteView, ProfissaoDetailView, ProfissaoListView,
                    ProfissaoUpdateView, ProfissionalCreateView, ProfissionalDeleteView, ProfissionalDetailView,
                    ProfissionalListView, ProfissionalUpdateView, UsuarioIndexTemplateView)

app_name = 'usuario'
router = routers.DefaultRouter()
router.register(r'profissional', ProfissionalViewAPI, 'profissional-api')
router.register(r'profissional-image', ProfissionalImageViewSet, 'profissional-image-api')
router.register(r'cliente', ClienteViewAPI, 'cliente-api')
router.register(r'profissao', ProfissaoViewAPI, 'profissao-api')

# URLs do Models Profissao
urlpatterns = [
    path('api/usuario/', include(router.urls)),
    path('usuario/', UsuarioIndexTemplateView.as_view(), name='usuario-index'),
    path('usuario/profissao/', ProfissaoListView.as_view(), name='profissao-list'),
    path('usuario/profissao/create/', ProfissaoCreateView.as_view(), name='profissao-create'),
    path('usuario/profissao/<uuid:pk>/', ProfissaoDetailView.as_view(), name='profissao-detail'),
    path('usuario/profissao/update/<uuid:pk>/', ProfissaoUpdateView.as_view(), name='profissao-update'),
    path('usuario/profissao/delete/<uuid:pk>/', ProfissaoDeleteView.as_view(), name='profissao-delete'),
]

# URLs do Models Cliente
urlpatterns += [
    path('usuario/cliente/', ClienteListView.as_view(), name='cliente-list'),
    path('usuario/cliente/create/', ClienteCreateView.as_view(), name='cliente-create'),
    path('usuario/cliente/<uuid:pk>/', ClienteDetailView.as_view(), name='cliente-detail'),
    path('usuario/cliente/update/<uuid:pk>/', ClienteUpdateView.as_view(), name='cliente-update'),
    path('usuario/cliente/delete/<uuid:pk>/', ClienteDeleteView.as_view(), name='cliente-delete'),
]

# URLs do Models Profissional
urlpatterns += [
    path('usuario/profissional/', ProfissionalListView.as_view(), name='profissional-list'),
    path('usuario/profissional/create/', ProfissionalCreateView.as_view(), name='profissional-create'),
    path('usuario/profissional/<uuid:pk>/', ProfissionalDetailView.as_view(), name='profissional-detail'),
    path('usuario/profissional/update/<uuid:pk>/', ProfissionalUpdateView.as_view(), name='profissional-update'),
    path('usuario/profissional/delete/<uuid:pk>/', ProfissionalDeleteView.as_view(), name='profissional-delete'),
]

# URLs do Models Profissao
urlpatterns += [
    path('usuario/profissao/', ProfissaoListView.as_view(), name='profissao-list'),
    path('usuario/profissao/create/', ProfissaoCreateView.as_view(), name='profissao-create'),
    path('usuario/profissao/<uuid:pk>/', ProfissaoDetailView.as_view(), name='profissao-detail'),
    path('usuario/profissao/update/<uuid:pk>/', ProfissaoUpdateView.as_view(), name='profissao-update'),
    path('usuario/profissao/delete/<uuid:pk>/', ProfissaoDeleteView.as_view(), name='profissao-delete'),
]

# URLs do Models Cliente
urlpatterns += [
    path('usuario/cliente/', ClienteListView.as_view(), name='cliente-list'),
    path('usuario/cliente/create/', ClienteCreateView.as_view(), name='cliente-create'),
    path('usuario/cliente/<uuid:pk>/', ClienteDetailView.as_view(), name='cliente-detail'),
    path('usuario/cliente/update/<uuid:pk>/', ClienteUpdateView.as_view(), name='cliente-update'),
    path('usuario/cliente/delete/<uuid:pk>/', ClienteDeleteView.as_view(), name='cliente-delete'),
]

# URLs do Models Profissional
urlpatterns += [
    path('usuario/profissional/', ProfissionalListView.as_view(), name='profissional-list'),
    path('usuario/profissional/create/', ProfissionalCreateView.as_view(), name='profissional-create'),
    path('usuario/profissional/<uuid:pk>/', ProfissionalDetailView.as_view(), name='profissional-detail'),
    path('usuario/profissional/update/<uuid:pk>/', ProfissionalUpdateView.as_view(), name='profissional-update'),
    path('usuario/profissional/delete/<uuid:pk>/', ProfissionalDeleteView.as_view(), name='profissional-delete'),
]

urlpatterns += [path('api/usuario/sendemail/', UserSendMail.as_view({'get': 'sendmail'}), name='sendmail')]
urlpatterns += [path('api/usuario/recoverpassword/',
                     RecoverPassword.as_view({'get': 'recovery_password'}), name='recovery_password')]
urlpatterns += [path('api/usuario/changepassword/',
                     ChangePasswordUser.as_view({'post': 'change_password'}), name='changepassword')]
urlpatterns += [path('api/usuario/requestresetaccount/',
                     RequestResetAccount.as_view({'get': 'request_reset_account'}), name='request_reset_account')]
urlpatterns += [path('api/usuario/resetaccount/',
                     ResetAccount.as_view({'get': 'reset_account'}), name='reset_account')]
urlpatterns += [path('api/profissional/reviews/',
                     ProfissionalViewAPI.as_view({'get': 'busca_avaliacao_nota_profissional'}), name='busca_avaliacao_nota_profissional')]
