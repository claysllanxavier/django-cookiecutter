from drf_jsonmask.views import OptimizedQuerySetMixin
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import UsuarioSerializer, UsuarioGETSerializer
from .models import Usuario


@permission_classes([IsAuthenticated, ])
class UsuarioViewAPI(ModelViewSet):
    """ Classe para gerenciar as requisições da API para os métodos POST, PUT, PATCH e DELETE """
    queryset = Usuario.objects.select_related().all()
    serializer_class = UsuarioSerializer


@permission_classes([IsAuthenticated, ])
class UsuarioGETAPI(OptimizedQuerySetMixin, ReadOnlyModelViewSet):
    """ Classe para gerenciar as requisições da API para o métodos GET

        A lista filterset_fields deve ser configurada com os campos do models que poderão ser utilizados para realizar
        filtros no models como por exemplo nome_do_campo=valor_a_ser_filtrado

        A lista search_fields deve ser configurada com os campos do models que poderão ser utilizados para realizar
        buscas no models como por exemplo search=valor_a_ser_pesquisado
    """
    queryset = Usuario.objects.select_related().all()
    serializer_class = UsuarioGETSerializer
    filter_backend = [filters.SearchFilter]
    # TODO Configure os parâmetros de filtro (filterset_fields) e buscar (search_fields)
    filterset_fields = []
    search_fields = []