from django.contrib.auth.models import Group, User
from django.db import models, transaction
from core.models import Base
from rest_framework.authtoken.models import Token


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
    latitude = models.FloatField('Latitude', default=0.0)
    longitude = models.FloatField('Longitude', default=0.0)
    endereco = models.TextField('Endereço Residencial', blank=True, null=True)

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

    def save(self, *args, **kwargs):
        try:
            if User.objects.filter(username=self.email).exists() is False:
                with transaction.atomic():
                    new_user = User.objects.create_user(self.email, self.email,
                                                        User.objects.make_random_password(length=8))
                    self.django_user = new_user
                    token = Token.objects.create(user=self.django_user)
                    self.token = token.key
                super().save(*args, **kwargs)
            else:
                super().save(*args, **kwargs, force_update=True)
        except Exception as error:
            raise RuntimeError(f"Something bad happened: {error}")

    def send_email_account_created(self):
        try:
            # TODO Adicione a mensagem de conta criada com sucesso
            email_message = ""
            # TODO Crie o método de envio de email
            return True
        except:
            return False

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        fields_display = ['nome', 'email', 'telefone', 'endereco']
        """Sugestão de estrutura para facilitar a geração do relacionamento no FastAPI
        """
        # fastapi_tabela_ligacao = [
        #     {
        #         'nome_relacionamento': 'group_permission', 
        #         'nome_tabela_ligacao': 'auth_group_permissions', 
        #         'relacionamento': [
        #             {'coluna': 'group_id', 'campo_foreignkey': 'auth_group.id'}, 
        #             {'coluna': 'permission_id', 'campo_foreignkey': 'auth_permission.id'}
        #         ]
        #     }, 
        #     {
        #         'nome_relacionamento': 'user_group', 
        #         'nome_tabela_ligacao': 'auth_user_groups', 
        #         'relacionamento': [
        #             {'coluna': 'group_id', 'campo_foreignkey': 'auth_group.id'}, 
        #             {'coluna': 'user_id', 'campo_foreignkey': 'auth_user.id'}
        #         ]
        #     }, 
        # ]

    def __str__(self):
        return f"Usuario: {self.cpf} | {self.email}"
