from django_filters.rest_framework import DjangoFilterBackend
from drf_jsonmask.views import OptimizedQuerySetMixin
from help.settings import SENDGRID_API_KEY
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.contrib.auth.models import User
from .models import Cliente, Profissao, Profissional, Usuario
from atendimento.models import Agendamento, Avaliacao, Atendimento
from atendimento.serializers import AvaliacaoSerializer, AvaliacaoGetSerializer
from .serializers import ClienteSerializer, ProfissaoSerializer, ProfissionalSerializer, ProfissionalGetSerializer
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from rest_framework.exceptions import MethodNotAllowed, ValidationError, ParseError
from rest_framework.parsers import MultiPartParser
from django.http import JsonResponse


# API do Models Profissão
class ProfissaoViewAPI(OptimizedQuerySetMixin, ModelViewSet):
    """ End point para retornar os dados do Profissional.

        Campos de filtros -> Nome, Email, Cpf
    """
    queryset = Profissao.objects.all()
    serializer_class = ProfissaoSerializer

    @action(methods=['post'], detail=False)
    def validate(self, request, format=None):
        serializer = ProfissaoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)


# API do Models Cliente
class ClienteViewAPI(OptimizedQuerySetMixin, ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['nome', 'email', 'cpf']
    search_fields = ['nome', 'email', 'cpf']


# API do Models Profissional
class ProfissionalViewAPI(OptimizedQuerySetMixin, ModelViewSet):
    queryset = Profissional.objects.select_related().all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['categoria', 'email', 'cpf', 'nome']
    search_fields = ['nome', 'email', 'categoria', 'categoria__nome']

    def get_serializer_class(self):
        actions = ['list', 'retrieve']
        if self.action in actions:
            return ProfissionalGetSerializer
        return ProfissionalSerializer

    @action(methods=['post'], detail=False)
    def marcar_favorito(self, request, format=None):
        try:
            cliente_uuid = self.request.data.get('cliente')
            profissional_uuid = self.request.data.get('profissional')
            if Profissional.marcar_favorito(profissional_uuid, cliente_uuid):
                return Response([], status=status.HTTP_201_CREATED)
            return Response([], status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=False)
    def desmarcar_favorito(self, request, format=None):
        try:
            cliente_uuid = self.request.data.get('cliente');
            profissional_uuid = self.request.data.get('profissional')
            if Profissional.desmarcar_favorito(profissional_uuid, cliente_uuid):
                return Response([], status=status.HTTP_201_CREATED)
            return Response([], status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Profissional de teste bfe79b46-10f0-4ec1-9b62-3872279c7f41
    @action(methods=['get'], detail=False)
    def busca_avaliacao_nota_profissional(self, request, format=None):
        try:
            avaliacoes = None
            profissional_uuid = request.GET['profissional']
            agendamentos = Agendamento.objects.filter(fk_profissional=profissional_uuid, etapa=7).values_list('id', flat=True)
            avaliacoes = Avaliacao.objects.filter(fk_atendimento__in=agendamentos)
            if avaliacoes != None:
                avaliacoes_serializer = AvaliacaoGetSerializer(avaliacoes, many=True)
                return Response({'results': avaliacoes_serializer.data},
                                status=status.HTTP_200_OK)
            return Response({'results': None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfissionalImageViewSet(ModelViewSet):
    parser_classes = [MultiPartParser]
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer


class UserSendMail(ViewSet):
    """
    Viewset para enviar o email de confirmação do cadastro do usuário na plataforma
    """
    queryset = Profissional.objects.all()

    @action(methods=['get'], detail=False)
    def sendmail(self, request, pk=None):
        """
        Action para envio do email de confirmação de cadastro na plataforma
        Parameters
        ----------
        request -> Contendo a chave email que será recuperada para envio do email.

        Returns
        -------
        HttpResponse com success caso finalize com sucesso e error com o possível error no envio.
        """
        try:
            email_to = request.GET['email']
            user_password = None
            email_message = None
            if email_to is None:
                return Response({'error': 'O e-mail deve ser informado'},
                                status=status.HTTP_404_NOT_FOUND)
            user = User.objects.filter(username=email_to).first()
            if user is None:
                return Response({'error': 'Nenhum usuário encontrado com os dados informados'},
                                status=status.HTTP_404_NOT_FOUND)
            email_message = "Seja bem vindo à plataforma <strong>HelpTO</strong><br/><br/> Ficamos felizes com seu cadastro. "
            email_message += "Seus dados de acesso são:<br/><br/>"
            if Usuario.current_user_is_client(user) is True:
                client_user = Usuario.get_client_user_from_django_user(user)
                if client_user is not None:
                    user_password = client_user.password
                email_message += f"<h3>Login -> {email_to} <br/>Senha -> {user_password}</h3>"
            if Usuario.current_user_is_professional(user) is True:
                professional = Usuario.get_professional_user_from_django_user(user)
                if professional is not None:
                    user_password = professional.password
                email_message += f"<h3>Login -> {email_to}<br/>Senha ->{user_password}. <br/><br/></h3> "
                email_message += "Solicitamos que aguarde a aprovação do seu cadastro para acessar a plataforma."

            if user_password is not None and email_message is not None:
                message = Mail(from_email='adm@helpto.com.br', to_emails=email_to,
                               subject='Bem vindo(a) a plataforma Help TO',
                               html_content=email_message)
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                sg.send(message)
                return Response([{'success': 'mensagem enviada com sucesso'}], status=status.HTTP_200_OK)
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangePasswordUser(ViewSet):
    queryset = Profissional.objects.all()

    @action(methods=['post'], detail=False)
    def change_password(self, request, format=None):
        """
        Caso ocorra uma exceção o padrão de retorno deve sempre seguir o formato:

             return Response({'error': 'descricao_do_erro', status=status.HTTP_ERROR_STATUS)

        Os tipos de status de erro do HTTP podem ser pesquisados no link abaixo

            https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

        Lembre que uma das premissas do Python é que explícito é melhor que implícito, portanto seja o mais específico
        possível no retorno do erro
        """
        try:
            # Rercuperando os dados informardos
            username = request.data['email']
            old_password = request.data['old_password']
            new_password = request.data['new_password']
            if username is None or old_password is None or new_password is None:
                return Response({'error': 'Os campos emails senha antiga e nova senha devem ser fornecidos'}, status=status.HTTP_400_BAD_REQUEST)
            # Recuperando o usuãrio informado
            user = User.objects.get(username=username)
            if user is None:
                return Response({'error': 'Nenhum usuário encontrado com os dados informados'}, status=status.HTTP_404_NOT_FOUND)
            user.set_password(new_password)
            user.save()
            return Response({'success': "Senha alterada com sucesso"}, status=status.HTTP_200_OK)
        except PermissionDenied as permission_error:
            return Response({'error': permission_error}, status=status.HTTP_401_UNAUTHORIZED)
        except MethodNotAllowed as method_error:
            return Response({'error': method_error}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except ObjectDoesNotExist as not_found_error:
            return Response({'error': "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as validation_error:
            return Response({'error': validation_error}, status=status.HTTP_400_BAD_REQUEST)
        except ParseError as validation_error:
            return Response({'error': validation_error}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecoverPassword(ViewSet):
    queryset = Profissional.objects.all()
    @action(methods=['get'], detail=False)
    def recovery_password(self, request, format=None):
        try:
            username = request.GET['email']
            if username is None:
                return Response({'error': 'O email deve ser fornecido'}, status=status.HTTP_404_NOT_FOUND)
            user = User.objects.get(username=username)
            if user is None:
                return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
            new_password = User.objects.make_random_password(length=8)
            user.set_password(new_password)
            user.save()
            email_to = request.GET['email']
            message = Mail(from_email='adm@helpto.com.br', to_emails=email_to,
                           subject='Olá, \n',
                           html_content=f'Sua senha temporária é <strong>{new_password}</strong> lembre-se de alterá-la na área do seu perfil')
            try:
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                sg.send(message)
                return Response([{'success': 'mensagem enviada com sucesso'}], status=status.HTTP_200_OK)
            except Exception as error:
                return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as error:
            return Response({'error': 'Ocorreu um erro ao tentar recuperar sua senha'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RequestResetAccount(ViewSet):
    queryset = Profissional.objects.all()
    @action(methods=['get'], detail=False)
    def request_reset_account(self, request, format=None):
        message = "Para confirmar a exclusão de sua conta e iniciar o cadastro novamente clique no link abaixo. \n\n";
        try:
            username = request.GET['email']
            if username is None:
                return Response({'error': 'O email deve ser fornecido'}, status=status.HTTP_404_NOT_FOUND)
            user = User.objects.get(username=username)
            if user is None:
                return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
            message += f"<a href='https://helpto.com.br/core/api/usuario/resetaccount?email={username}'>"
            message += "Resetar a conta para recadastrar minha conta</a>"
            email_to = request.GET['email']
            message = Mail(from_email='adm@helpto.com.br', to_emails=email_to, subject='Olá, \n', html_content=message)
            try:
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                sg.send(message)
                # TODO Redirecionar para uma página de sucesso.
                return Response([{'Sucesso': 'Sua solictação de reinicio do cadastro foi processada com sucesso.'}], status=status.HTTP_200_OK)
            except Exception as error:
                return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as error:
            return Response({'error': 'Ocorreu um erro ao tentar apagar sua conta'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResetAccount(ViewSet):
    queryset = Profissional.objects.all()
    @action(methods=['get'], detail=False)
    def reset_account(self, request, format=None):
        message = "Sua conta foi excluída, agora você pode iniciar o cadastro novamente.";
        try:
            username = request.GET['email']
            if username is None:
                return Response({'Erro': 'O email deve ser fornecido'}, status=status.HTTP_404_NOT_FOUND)
            user = User.objects.filter(username=username).first()
            if user is None:
                return Response({'Erro': 'Nenhum usuário foi encontrado na nossa base de dados'},
                                status=status.HTTP_404_NOT_FOUND)
            User.objects.get(username=username).delete()
            email_to = request.GET['email']
            message = Mail(from_email='adm@helpto.com.br', to_emails=email_to, subject='Olá, \n', html_content=message)
            try:
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                sg.send(message)
                return Response([
                    {'Sucesso': 'Sua conta foi apagada com sucesso, já pode se cadastrar novamente na plataforma'}],
                    status=status.HTTP_200_OK)
            except Exception as error:
                return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as error:
            return Response({'error': 'Ocorreu um erro ao tentar apagar sua conta incompleta'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
