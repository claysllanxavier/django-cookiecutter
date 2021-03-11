from core.views import (BaseCreateView, BaseDeleteView, BaseDetailView,
                        BaseListView, BaseTemplateView, BaseUpdateView)

from .forms import UsuarioForm
from .models import Usuario

# Views Inicial Usuario


class UsuarioIndexTemplateView(BaseTemplateView):
    # Views para renderizar a tela inicial Usuario
    template_name = "usuario/index.html"
    context_object_name = 'usuario'

    def get_context_data(self, **kwargs):
        context = super(UsuarioIndexTemplateView, self).get_context_data(**kwargs)
        return context


# Views do Models Usuario
class UsuarioListView(BaseListView):
    """Classe para gerenciar a listagem do Usuario"""
    model = Usuario
    template_name = "usuario/usuario_list.html"
    context_object_name = 'usuario'
    list_display = ['nome', 'email', 'telefone', 'endereco']

    def get_context_data(self, **kwargs):
        context = super(UsuarioListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        """Subscrevendo o queryset para
        filtrar os dados conforme o perfil logado

        Returns:
            QuerySet
        """

        queryset = super(UsuarioListView, self).get_queryset()
        if self.request.user.is_superuser:
            return queryset
        else:
            # queryset.filter()
            return queryset


class UsuarioDetailView(BaseDetailView):
    """Classe para gerenciar o detalhe do Usuario """
    model = Usuario
    form_class = UsuarioForm
    success_url = "usuario:usuario-list"
    template_name = 'usuario/usuario_detail.html'
    context_object_name = 'usuario'

    def get_context_data(self, **kwargs):
        context = super(UsuarioDetailView, self).get_context_data(**kwargs)
        return context

    """ Caso deseje controlar o acesso do usuário ao detalhamento
     do item descomente esse método """

    # def dispatch(self, request, *args, **kwargs):
    #    """ Método para verificar se o usuário
    #    tem permissão de detalhar o item
    #    """

    #    # Recuperando o objeto
    #    obj = self.get_object()
    #    if (self.request.user.is_superuser):
    #        return super(UsuarioDetailView, self).dispatch(
    #            request, * args, **kwargs)

    #    # Informando que o usuário não tem permissão de acesso
    #    messages.add_message(request, messages.WARNING,
    #        'Você não tem permissão para visualizar esse registro.')
    #    # Redirecionando o usuário para tela de listagem
    #    return redirect("usuario:usuario-list")


class UsuarioCreateView(BaseCreateView):
    """Classe para gerenciar a criação do Usuario """
    model = Usuario
    form_class = UsuarioForm
    context_object_name = 'usuario'
    success_url = "usuario:usuario-list"
    template_name = 'usuario/usuario_create.html'
    #inlines = []


class UsuarioUpdateView(BaseUpdateView):
    """Classe para gerenciar a atualização do Usuario """
    model = Usuario
    form_class = UsuarioForm
    context_object_name = 'usuario'
    success_url = "usuario:usuario-list"
    template_name = 'usuario/usuario_update.html'
    #inlines = []

    """ Caso seja necessário controlar o acesso do usuário a edição
     do item descomente esse método """

    # def dispatch(self, request, *args, **kwargs):
    #    """ Método para verificar se o usuário
    #    tem permissão de detalhar o item
    #    """

    #    #Recuperando o objeto
    #    obj = self.get_object()
    #    if (self.request.user.is_superuser):
    #        return super(UsuarioUpdateView, self).dispatch(
    #            request, * args, **kwargs)

    #    # Informando que o usuário não tem permissão de acesso
    #    messages.add_message(request, messages.WARNING,
    #        'Você não tem permissão para editar esse registro.')
    #    # Redirecionando o usuário para tela de listagem
    #    return redirect("usuario:usuario-list")


class UsuarioDeleteView(BaseDeleteView):
    """Classe para gerenciar a exclusão do Usuario """
    model = Usuario
    form_class = UsuarioForm
    context_object_name = 'usuario'
    success_url = "usuario:usuario-list"
    template_name = 'usuario/usuario_delete.html'

    """ Caso seja necessário controlar o acesso do usuário a edição
     do item descomente esse método """

    # def dispatch(self, request, *args, **kwargs):
    #    """ Método para verificar se o usuário
    #    tem permissão de detalhar o item
    #    """

    #    # Recuperando o objeto
    #    obj = self.get_object()
    #    if (self.request.user.is_superuser):
    #        return super(UsuarioDeleteView, self).dispatch(
    #            request, * args, **kwargs)

    #    # Informando que o usuário não tem permissão de acesso
    #    messages.add_message(request, messages.WARNING,
    #        'Você não tem permissão para excluir esse registro.')
    #    # Redirecionando o usuário para tela de listagem
    #    return redirect("usuario:usuario-list")


# Fim das Views do Models Usuario
