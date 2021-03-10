from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.shortcuts import get_object_or_404
from help.mensagens import MSG_REGISTRO_EXISTENTE
from help.utils import registro_existente
from nuvols.core.models import Base
from rest_framework.authtoken.models import Token
from sendgrid.helpers.mail import Mail
from help.settings import SENDGRID_API_KEY
from sendgrid import SendGridAPIClient


class Profissao(Base):
    """ Classe para gerenciar as profissões dos prestadores
    """
    nome = models.CharField("Profissão", max_length=300, unique=True)

    class Meta:
        verbose_name = 'Profissão'
        verbose_name_plural = 'Profissões'
        fields_display = ['nome', ]

    def __str__(self):
        return "{}".format(self.nome)


class Usuario(Base):
    """ Classe padrão para gerenciamento de todos os usuários da plataforma
    """
    django_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    cpf = models.CharField(max_length=11, blank=True, null=True)
    nome = models.CharField(max_length=300)
    email = models.EmailField()
    telefone = models.CharField(max_length=100, blank=True, null=True)
    token = models.TextField(blank=True, null=True, editable=False)
    firebase = models.TextField('Token do usuário no Firebase', blank=True, null=True)
    access_token = models.TextField('Access Token', blank=True, null=True)
    id_token = models.TextField('ID Token', blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.FloatField('Latitude', default=0.0)
    longitude = models.FloatField('Longitude', default=0.0)

    class Meta:
        abstract = True

    def delete(self, using='default', keep_parents=False):
        """
        Sobscrevendo o Delete para realmente excluir os dados do banco de dados e não apenas
        marcar como deleted and enabled
        """
        try:
            with transaction.atomic():
                # Verificando se existe um Django User com esse username
                if User.objects.filter(username=self.email).exists():
                    # Apagando o user do Django
                    User.objects.get(username=self.email).delete()
                super(Usuario, self).delete()
        except:
            pass

    @staticmethod
    def current_user_is_professional(user) -> bool:
        try:
            if user is not None:
                return Profissional.objects.filter(django_user=user).exists()
            return False
        except Exception as error:
            return False

    @staticmethod
    def current_user_is_client(user) -> bool:
        """
        Método para verificar se o usuário corrente é um cliente
        Parameters
        ----------
        user: Instância de User

        Returns
        -------
        bool
            True se for um cliente e false se não for um cliente
        """
        try:
            if user is not None:
                return Cliente.objects.filter(django_user=user).exists()
            return False
        except Exception as error:
            return False

    @staticmethod
    def get_professional_user_from_django_user(user):
        """ Método para retornar o profissional logado baseado no User do Django

        Parameters
        ----------
        user : Instância de User
            Instância do usuário logado no sistema

        Returns
        -------
        Profissional
            Instância do profissional
        """
        try:
            return Profissional.objects.get(django_user=user)
        except Exception as error:
            return 0

    @staticmethod
    def get_client_user_from_django_user(user):
        """Método para retornar o cliente logado baseado no DjangoUser

        Parameters
        ----------
        user : DjangoUser Logado

        Returns
        -------
        Cliente
            Instância do cliente logado no sistema
        """
        #
        try:
            return Cliente.objects.get(django_user=user)
        except Exception as error:
            return 0


class Cliente(Usuario):
    """ Classe para gerenciar os dados dos clientes da plataforma
    """
    endereco_res = models.TextField('Endereço Residencial', blank=True, null=True)
    endereco_com = models.TextField('Endereço Comercial', blank=True, null=True)

    def clean(self):
        if registro_existente(self, 'email'):
            raise ValidationError(MSG_REGISTRO_EXISTENTE.format('Cliente com esse Email'))

    def save(self, *args, **kwargs):
        try:
            if User.objects.filter(username=self.email).exists() is False:
                with transaction.atomic():
                    if self.password == None or self.password == "":
                        self.password = User.objects.make_random_password(length=8)
                    new_user = User.objects.create_user(self.email, self.email, self.password)
                    self.django_user = new_user
                    new_user.groups.add(Group.objects.get(name='Cliente'))
                    token = Token.objects.create(user=self.django_user)
                    self.token = token.key
                super().save(*args, **kwargs)
            else:
                super().save(*args, **kwargs, force_update=True)
        except Exception as error:
            raise RuntimeError(f"Something bad happened: {error}")

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        fields_display = ['nome', 'email', 'telefone', 'endereco_res']

    def __str__(self):
        return "{}".format(self.nome)


class Profissional(Usuario):
    """ Classe para gerenciar os dados do profissionais/prestadores de serviço na plataforma

    Parameters
    ----------
    Usuario : Usuario
        Instância de Usuario

    Raises
    ------
    ValidationError
        Será levantada uma exceção caso seja informado um e-mail já cadastrado na plataforma
    """

    CHOICES_TIPO_CONTA = (('Conta Corrente', 'Conta Corrente'), ('Conta Poupança', 'Conta Poupança'))

    foto = models.ImageField("Foto", upload_to="prestador/profile", blank=True, null=True, max_length=300)
    profissao = models.ForeignKey("usuario.Profissao", verbose_name="Profissão", on_delete=models.PROTECT, blank=True,
                                  null=True)
    especialidade = models.CharField("Especialidade", max_length=300, blank=True, null=True)
    endereco = models.TextField("Endereço", blank=True)
    aprovado = models.BooleanField("Profissional aprovado?", default=False)
    email_cadastro_aprovado_enviado = models.BooleanField(default=False)
    categoria = models.ForeignKey('servico.Categoria', verbose_name='Categoria do serviço', on_delete=models.PROTECT,
                                  null=True, blank=True)
    curtidas = models.PositiveSmallIntegerField(default=3, blank=True, null=True)
    favorito_clientes = models.ManyToManyField(Cliente, blank=True)
    cnpj = models.CharField(max_length=50, blank=True, null=True)
    # Área para os dados bancários
    banco_codigo = models.PositiveBigIntegerField("Número da Agência", null=True, blank=True)
    banco_nome = models.CharField("Nome do Banco", blank=True, null=True, max_length=250)
    banco_tipo_conta = models.CharField("Tipo da Conta", choices=CHOICES_TIPO_CONTA, blank=True, null=True,
                                        max_length=50)
    banco_numero_conta = models.CharField("Número da Conta", blank=True, null=True, max_length=50)
    banco_pix = models.TextField("Chave do Pix", blank=True, null=True)

    # def clean(self):
    #     """
    #     Método para verificar se o email informado já existe na base de dados
    #     Returns
    #     -------
    #         ValidationError com mensagem que o email já existe
    #     """
    #     if registro_existente(self, 'email'):
    #         raise ValidationError(MSG_REGISTRO_EXISTENTE.format('Email'))

    def get_user_category(self):
        """
        Método para retornar a categoria a qual o usuário está vinculado
        Returns
        -------
            Instância de Categoria
        """
        from servico.models import Categoria
        try:
            return Categoria.objects.get(id=self.categoria.id)
        except Exception as error:
            pass

    def quantidade_curtidas(self):
        """
        Método para retornar a quantidade de curtidas que um profissional possuí
        Returns
        -------
            Int -> Quantidade de curtidas
        """
        try:
            return self.favorito_clientes.all().count()
        except Exception as error:
            return 0

    @staticmethod
    def marcar_favorito(profissional_uuid: str, cliente_uuid: str):
        try:
            profissional = get_object_or_404(Profissional, id=profissional_uuid)
            profissional.favorito_clientes.add(cliente_uuid)
            return True
        except Exception as error:
            return False

    @staticmethod
    def desmarcar_favorito(profissional_uuid: str, cliente_uuid: str):
        try:
            profissional = get_object_or_404(Profissional, id=profissional_uuid)
            profissional.favorito_clientes.remove(cliente_uuid)
            return True
        except Exception as error:
            return False

    def send_email_approved_professional_account(self):
        """
        Método para envio de email confirmando a aprovação do cadastro do profissional
        Returns
        -------
        bool True se for processado com sucesso e False se for processado com erro
        """
        try:
            email_message = "Seu cadastro como profissional em nossa plataforma foi aprovado e liberado.\n"
            email_message += "Acesse o aplicativo com seu usuário e senha para cadastrar seus serviços."
            message = Mail(from_email='adm@helpto.com.br', to_emails=self.email,
                           subject='Bem vindo(a) a plataforma Help TO',
                           html_content=f'<strong>{email_message}</strong>')
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            sg.send(message)
            return True
        except:
            return False

    def save(self, *args, **kwargs):
        try:
            if User.objects.filter(username=self.email).exists() is False:
                with transaction.atomic():
                    if self.password == None or self.password == "":
                        self.password = User.objects.make_random_password(length=8)
                    new_user = User.objects.create_user(self.email, self.email, self.password)
                    new_user.groups.add(Group.objects.get(name='Profissional'))
                    self.django_user = new_user
                    token = Token.objects.create(user=self.django_user)
                    self.token = token.key
                super().save(*args, **kwargs)
            else:
                if self.aprovado == True and self.email_cadastro_aprovado_enviado == False:
                    #Enviando o email para o profissional aprovado.
                    if self.send_email_approved_professional_account():
                        self.email_cadastro_aprovado_enviado = True
                super().save(*args, **kwargs, force_update=True)
        except Exception as error:
            raise RuntimeError(f"Something bad happened: {error}")

    class Meta:
        verbose_name = 'Profissional'
        verbose_name_plural = 'Profissionais'
        fields_display = ['nome', 'email', 'telefone', ]
        fk_fields_modal = ['profissao', ]

    def __str__(self):
        return "{}".format(self.nome)
