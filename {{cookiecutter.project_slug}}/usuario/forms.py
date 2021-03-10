from nuvols.core.forms import BaseForm

from .models import Cliente, Profissao, Profissional


class ProfissaoForm(BaseForm):
    """ Form padrão para o model Profissao """

    class Meta:
        exclude = ['deleted', 'enabled']
        model = Profissao


class ClienteForm(BaseForm):
    """ Form padrão para o model Cliente """
    class Meta:
        exclude = ['deleted', 'enabled', 'django_user', 'token', 'firebase']
        model = Cliente


class ClienteReduzidoForm(BaseForm):
    """ Form reduzido para utilizar nos madal's do model Cliente """
    class Meta:
        exclude = [
            'deleted',
            'enabled',
            'endereco_res',
            'endereco_com',
            'django_user', 'token', 'firebase']
        model = Cliente


class ProfissionalForm(BaseForm):
    """ Form padrão para o model Profissional """

    class Meta:
        exclude = ['deleted', 'enabled', 'django_user', 'token', 'firebase']
        model = Profissional
