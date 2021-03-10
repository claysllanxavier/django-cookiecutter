from nuvols.core.views import (BaseCreateView, BaseDeleteView, BaseDetailView,
                               BaseListView, BaseTemplateView, BaseUpdateView)

from .forms import ClienteForm, ProfissaoForm, ProfissionalForm
from .models import Cliente, Profissao, Profissional


# Views Inicial Usuario
class UsuarioIndexTemplateView(BaseTemplateView):
    # Views para renderizar a tela inicial Usuario
    template_name = "usuario/index.html"
    context_object_name = 'usuario'

    def get_context_data(self, **kwargs):
        context = super(UsuarioIndexTemplateView, self).get_context_data(**kwargs)
        return context


# Views do Models Profissao
class ProfissaoListView(BaseListView):
    """Classe para gerenciar a listagem do Profissao"""
    model = Profissao
    template_name = "usuario/profissao_list.html"
    context_object_name = 'profissao'
    list_display = ['nome']

    def get_context_data(self, **kwargs):
        context = super(ProfissaoListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        """Subscrevendo o método queryset para
        filtrar os dados conforme o perfil do
        usuário logado

        Returns:
            QuerySet
        """

        # Chamando a query padrão da classe
        queryset = super(ProfissaoListView, self).get_queryset()
        # Verificando se o usuário é superuser para retornar todos os registros
        if self.request.user.is_superuser:
            return queryset
        else:
            # queryset.filter()
            return queryset


class ProfissaoDetailView(BaseDetailView):
    """Classe para gerenciar o detalhe do Profissao """
    model = Profissao
    form_class = ProfissaoForm
    success_url = "usuario:profissao-list"
    template_name = 'usuario/profissao_detail.html'
    context_object_name = 'profissao'

    def get_context_data(self, **kwargs):
        context = super(ProfissaoDetailView, self).get_context_data(**kwargs)
        return context

    """ Caso seja necessário controlar o acesso do usuário ao detalhamento
     do item descomente esse método """

    # def dispatch(self, request, *args, **kwargs):
    #    """ Método para verificar se o usuário
    #    tem permissão de detalhar o item
    #    """

    #    # Recuperando o objeto
    #    obj = self.get_object()
    #    if (self.request.user.is_superuser):
    #        return super(ProfissaoDetailView, self).dispatch(
    #            request, * args, **kwargs)

    #    # Informando que o usuário não tem permissão de acesso
    #    messages.add_message(request, messages.WARNING,
    #        'Você não tem permissão para visualizar esse registro.')
    #    # Redirecionando o usuário para tela de listagem
    #    return redirect("usuario:profissao-list")


class ProfissaoCreateView(BaseCreateView):
    """Classe para gerenciar a criação do Profissao """
    model = Profissao
    form_class = ProfissaoForm
    context_object_name = 'profissao'
    success_url = "usuario:profissao-list"
    template_name = 'usuario/profissao_create.html'
    # inlines = []


class ProfissaoUpdateView(BaseUpdateView):
    """Classe para gerenciar a atualização do Profissao """
    model = Profissao
    form_class = ProfissaoForm
    context_object_name = 'profissao'
    success_url = "usuario:profissao-list"
    template_name = 'usuario/profissao_update.html'
    # inlines = []

    """ Caso seja necessário controlar o acesso do usuário a edição
     do item descomente esse método """

    # def dispatch(self, request, *args, **kwargs):
    #    """ Método para verificar se o usuário
    #    tem permissão de detalhar o item
    #    """

    #    #Recuperando o objeto
    #    obj = self.get_object()
    #    if (self.request.user.is_superuser):
    #        return super(ProfissaoUpdateView, self).dispatch(
    #            request, * args, **kwargs)

    #    # Informando que o usuário não tem permissão de acesso
    #    messages.add_message(request, messages.WARNING,
    #        'Você não tem permissão para editar esse registro.')
    #    # Redirecionando o usuário para tela de listagem
    #    return redirect("usuario:profissao-list")


class ProfissaoDeleteView(BaseDeleteView):
    """Classe para gerenciar a exclusão do Profissao """
    model = Profissao
    form_class = ProfissaoForm
    context_object_name = 'profissao'
    success_url = "usuario:profissao-list"
    template_name = 'usuario/profissao_delete.html'

    """ Caso seja necessário controlar o acesso do usuário a edição
     do item descomente esse método """

    # def dispatch(self, request, *args, **kwargs):
    #    """ Método para verificar se o usuário
    #    tem permissão de detalhar o item
    #    """

    #    # Recuperando o objeto
    #    obj = self.get_object()
    #    if (self.request.user.is_superuser):
    #        return super(ProfissaoDeleteView, self).dispatch(
    #            request, * args, **kwargs)

    #    # Informando que o usuário não tem permissão de acesso
    #    messages.add_message(request, messages.WARNING,
    #        'Você não tem permissão para excluir esse registro.')
    #    # Redirecionando o usuário para tela de listagem
    #    return redirect("usuario:profissao-list")


# Fim das Views do Models Profissao


# Views do Models Cliente
class ClienteListView(BaseListView):
    """Classe para gerenciar a listagem do Cliente"""
    model = Cliente
    template_name = "usuario/cliente_list.html"
    context_object_name = 'cliente'
    list_display = ['nome', 'email', 'telefone', 'endereco_res']

    def get_context_data(self, **kwargs):
        context = super(ClienteListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        """Subscrevendo o método queryset para
        filtrar os dados conforme o perfil do
        usuário logado

        Returns:
            QuerySet
        """

        # Chamando a query padrão da classe
        queryset = super(ClienteListView, self).get_queryset()
        # Verificando se o usuário é superuser para retornar todos os registros
        if self.request.user.is_superuser:
            return queryset
        else:
            # queryset.filter()
            return queryset


class ClienteDetailView(BaseDetailView):
    """Classe para gerenciar o detalhe do Cliente """
    model = Cliente
    form_class = ClienteForm
    success_url = "usuario:cliente-list"
    template_name = 'usuario/cliente_detail.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super(ClienteDetailView, self).get_context_data(**kwargs)
        return context

    """ Caso seja necessário controlar o acesso do usuário ao detalhamento
     do item descomente esse método """

    # def dispatch(self, request, *args, **kwargs):
    #    """ Método para verificar se o usuário
    #    tem permissão de detalhar o item
    #    """

    #    # Recuperando o objeto
    #    obj = self.get_object()
    #    if (self.request.user.is_superuser):
    #        return super(ClienteDetailView, self).dispatch(
    #            request, * args, **kwargs)

    #    # Informando que o usuário não tem permissão de acesso
    #    messages.add_message(request, messages.WARNING,
    #        'Você não tem permissão para visualizar esse registro.')
    #    # Redirecionando o usuário para tela de listagem
    #    return redirect("usuario:cliente-list")


class ClienteCreateView(BaseCreateView):
    """Classe para gerenciar a criação do Cliente """
    model = Cliente
    form_class = ClienteForm
    context_object_name = 'cliente'
    success_url = "usuario:cliente-list"
    template_name = 'usuario/cliente_create.html'
    # inlines = []


class ClienteUpdateView(BaseUpdateView):
    """Classe para gerenciar a atualização do Cliente """
    model = Cliente
    form_class = ClienteForm
    context_object_name = 'cliente'
    success_url = "usuario:cliente-list"
    template_name = 'usuario/cliente_update.html'
    # inlines = []

    """ Caso seja necessário controlar o acesso do usuário a edição
     do item descomente esse método """

    # def dispatch(self, request, *args, **kwargs):
    #    """ Método para verificar se o usuário
    #    tem permissão de detalhar o item
    #    """

    #    #Recuperando o objeto
    #    obj = self.get_object()
    #    if (self.request.user.is_superuser):
    #        return super(ClienteUpdateView, self).dispatch(
    #            request, * args, **kwargs)

    #    # Informando que o usuário não tem permissão de acesso
    #    messages.add_message(request, messages.WARNING,
    #        'Você não tem permissão para editar esse registro.')
    #    # Redirecionando o usuário para tela de listagem
    #    return redirect("usuario:cliente-list")


class ClienteDeleteView(BaseDeleteView):
    """Classe para gerenciar a exclusão do Cliente """
    model = Cliente
    form_class = ClienteForm
    context_object_name = 'cliente'
    success_url = "usuario:cliente-list"
    template_name = 'usuario/cliente_delete.html'

    """ Caso seja necessário controlar o acesso do usuário a edição
     do item descomente esse método """

    # def dispatch(self, request, *args, **kwargs):
    #    """ Método para verificar se o usuário
    #    tem permissão de detalhar o item
    #    """

    #    # Recuperando o objeto
    #    obj = self.get_object()
    #    if (self.request.user.is_superuser):
    #        return super(ClienteDeleteView, self).dispatch(
    #            request, * args, **kwargs)

    #    # Informando que o usuário não tem permissão de acesso
    #    messages.add_message(request, messages.WARNING,
    #        'Você não tem permissão para excluir esse registro.')
    #    # Redirecionando o usuário para tela de listagem
    #    return redirect("usuario:cliente-list")


# Fim das Views do Models Cliente


# Views do Models Profissional
class ProfissionalListView(BaseListView):
    """Classe para gerenciar a listagem do Profissional"""
    model = Profissional
    template_name = "usuario/profissional_list.html"
    context_object_name = 'profissional'
    list_display = ['nome', 'email', 'telefone', 'profissao', 'categoria']

    def get_context_data(self, **kwargs):
        context = super(ProfissionalListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        """Subscrevendo o método queryset para
        filtrar os dados conforme o perfil do
        usuário logado

        Returns:
            QuerySet
        """

        # Chamando a query padrão da classe
        queryset = super(ProfissionalListView, self).get_queryset()
        # Verificando se o usuário é superuser para retornar todos os registros
        if self.request.user.is_superuser:
            return queryset
        else:
            # queryset.filter()
            return queryset


class ProfissionalDetailView(BaseDetailView):
    """Classe para gerenciar o detalhe do Profissional """
    model = Profissional
    form_class = ProfissionalForm
    success_url = "usuario:profissional-list"
    template_name = 'usuario/profissional_detail.html'
    context_object_name = 'profissional'

    def get_context_data(self, **kwargs):
        context = super(ProfissionalDetailView, self).get_context_data(**kwargs)
        return context

    """ Caso seja necessário controlar o acesso do usuário ao detalhamento
     do item descomente esse método """

    # def dispatch(self, request, *args, **kwargs):
    #    """ Método para verificar se o usuário
    #    tem permissão de detalhar o item
    #    """

    #    # Recuperando o objeto
    #    obj = self.get_object()
    #    if (self.request.user.is_superuser):
    #        return super(ProfissionalDetailView, self).dispatch(
    #            request, * args, **kwargs)

    #    # Informando que o usuário não tem permissão de acesso
    #    messages.add_message(request, messages.WARNING,
    #        'Você não tem permissão para visualizar esse registro.')
    #    # Redirecionando o usuário para tela de listagem
    #    return redirect("usuario:profissional-list")


class ProfissionalCreateView(BaseCreateView):
    """Classe para gerenciar a criação do Profissional """
    model = Profissional
    form_class = ProfissionalForm
    context_object_name = 'profissional'
    success_url = "usuario:profissional-list"
    template_name = 'usuario/profissional_create.html'

    # inlines = []

    def get_context_data(self, **kwargs):
        context = super(
            ProfissionalCreateView,
            self).get_context_data(
            **kwargs)
        context['form_profissao'] = ProfissaoForm
        return context


class ProfissionalUpdateView(BaseUpdateView):
    """Classe para gerenciar a atualização do Profissional """
    model = Profissional
    form_class = ProfissionalForm
    context_object_name = 'profissional'
    success_url = "usuario:profissional-list"
    template_name = 'usuario/profissional_update.html'
    # inlines = []

    """ Caso seja necessário controlar o acesso do usuário a edição
     do item descomente esse método """

    # def dispatch(self, request, *args, **kwargs):
    #    """ Método para verificar se o usuário
    #    tem permissão de detalhar o item
    #    """

    #    #Recuperando o objeto
    #    obj = self.get_object()
    #    if (self.request.user.is_superuser):
    #        return super(ProfissionalUpdateView, self).dispatch(
    #            request, * args, **kwargs)

    #    # Informando que o usuário não tem permissão de acesso
    #    messages.add_message(request, messages.WARNING,
    #        'Você não tem permissão para editar esse registro.')
    #    # Redirecionando o usuário para tela de listagem
    #    return redirect("usuario:profissional-list")


class ProfissionalDeleteView(BaseDeleteView):
    """Classe para gerenciar a exclusão do Profissional """
    model = Profissional
    form_class = ProfissionalForm
    context_object_name = 'profissional'
    success_url = "usuario:profissional-list"
    template_name = 'usuario/profissional_delete.html'

    """ Caso seja necessário controlar o acesso do usuário a edição
     do item descomente esse método """

    # def dispatch(self, request, *args, **kwargs):
    #    """ Método para verificar se o usuário
    #    tem permissão de detalhar o item
    #    """

    #    # Recuperando o objeto
    #    obj = self.get_object()
    #    if (self.request.user.is_superuser):
    #        return super(ProfissionalDeleteView, self).dispatch(
    #            request, * args, **kwargs)

    #    # Informando que o usuário não tem permissão de acesso
    #    messages.add_message(request, messages.WARNING,
    #        'Você não tem permissão para excluir esse registro.')
    #    # Redirecionando o usuário para tela de listagem
    #    return redirect("usuario:profissional-list")

# Fim das Views do Models Profissional
