import os
import platform
import subprocess
import sys
import time
from pathlib import Path

from core.management.commands.parser_content import ParserContent
from core.management.commands.utils import Utils
from core.models import Base
from django.apps import apps
from django.core.management.base import BaseCommand



class AppModel:
    """Classe responsável por todo o processo de análise do models do Django para 
    gerar os arquivos tantos do projeto Django como do Fastapi

    Arquivos Django Gerados:
        1 - templates (create, list, update, detail, delete)
        2 - forms
        3 - views
        4 - urls
        5 - api_views
        6 - api_urls
        7 - serializers

    Arguments:
        path_fastapi {String} -- Caminho do projeto Fastapi
        app_name {String} -- Nome do app do projeto que será mapeada para gerar os arquivos do projeto

    Keyword Arguments:
        model_name {String} -- Nome do models a ser mapeado, caso não seja passado o script fará a 
                               análise de todos os models da app (default: {None})
    """

    def __init__(self, path_fastapi, app_name, model_name=None):
        try:
            self.path_core = os.path.join(self.BASE_DIR, "core")
            self.path_fastapi = path_fastapi
            self.models = None
            self.model = None
            self.app_name = str(app_name).strip()
            self.app_name_lower = self.app_name.lower()
            self.app = apps.get_app_config(self.app_name_lower)
            self.model_name = str(model_name).strip()
            self.model_name_lower = self.model_name.lower()

            if model_name is not None:
                self.model = self.app.get_model(self.model_name)
            else:
                self.models = ((x, x.__name__.strip(), x.__name__.strip().lower())
                               for x in self.app.get_models())
            self.operation_system = platform.system().lower()

        except Exception as error:
            raise error

    def get_path_app_dir(self):
        """Método para retornar o caminho aonde será criado o projeto Fastapi"""
        try:
            return Path("{}/{}".format(self.path_fastapi, self.app_name_lower))
        except Exception as error:
            Utils.show_message(f"Error in get_path_app_dir: {error}", error=True)

    def get_app_model_name(self, title_case=False):
        """ Método responsável por retornar o nome do Models das app do projeto Django"""
        try:
            if title_case is True:
                return f"{self.app_name.title()}{self.model_name}"
            return f"{self.app_name}{self.model_name}"
        except Exception as error:
            Utils.show_message(f"Error in get_app_model_name: {error}")
            return None


class Command(BaseCommand):
    help = """Manager responsável por analisar as classes de modelos do projeto Django para gerar os arquivos 
    do projeto FastAPI correspondente às apps do Django"""

    def __init__(self):
        super().__init__()
        self.path_root = os.getcwd()
        self.path_core = os.path.join(self.BASE_DIR, "core")
        self.operation_system = platform.system().lower()


        self.project = 'fastapi'
        self.fastapi_dir = os.path.join(self.BASE_DIR, '..', "fastapi")
        self.fastapi_project = "{}".format(self.project)
        self.snippet_dir = "{}/{}".format(self.path_core, "management/commands/snippets/fastapi/")

        self.current_app_model = None

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    _django_types = ["SmallAutoField", "AutoField", "BLANK_CHOICE_DASH", "BigAutoField", "BigIntegerField",
                     "BinaryField", "BooleanField", "CharField", "CommaSeparatedIntegerField", "DateField",
                     "DateTimeField", "DecimalField", "DurationField", "EmailField", "Empty", "FileField", "Field",
                     "FieldDoesNotExist", "FilePathField", "FloatField", "GenericIPAddressField", "IPAddressField",
                     "IntegerField", "FieldFile", "NOT_PROVIDED", "NullBooleanField", "ImageField",
                     "PositiveIntegerField", "PositiveSmallIntegerField", "SlugField", "SmallIntegerField", "TextField",
                     "TimeField", "URLField", "UUIDField", "ForeignKey", "OneToOneField", ]

    _schemas_types = ["int", "int", "BLANK_CHOICE_DASH", "int", "int", "str", "bool", "str", "str", "datetime.date",
                      "datetime.datetime", "float", "int", "EmailStr", "str", "str", "str", "str", "str", "float",
                      "str", "str", "int", "str", "str", "bool", "str", "int", "int", "str", "int",
                      "str", "DateTime", "str", "str", "int", "int", ]


    def add_arguments(self, parser):
        parser.add_argument("App", type=str, nargs="?")
        parser.add_argument("Model", type=str, nargs="?")
        parser.add_argument("--app", action="store_true", dest="app", help="Criar a App e seus models")
        parser.add_argument("--app_model", action="store_true", dest="app_model",
                            help="Criar a App e o Model informado")

    def _check_dir(self, path) -> bool:
        """Método responsável por verificar se o diretório já existe."""
        return Utils.check_dir(path)

    def _check_file(self, path):
        """Método responsável por verificar se o arquivo já existe no caminho informado."""
        return Utils.check_file(path)
    
    def __check_content(self, path, text_check):
        """Método responsável por verificar se o texto passado com parâmetro existe no conteúdo do arquivo."""
        return Utils.check_content(path, text_check)

    def __ignore_base_fields(self, field):
        """Método responsável por remover da análise do models os atributos herdados da classe pai Base

        Arguments:
            field {String} -- Nome do atributo

        Returns:
            bool -- True se o atributo for um dos atributos da classe pai, caso contrário False.
        """
        try:
            __ignore_fields = ["id",  "deleted", "created_on", "updated_on" ]
            return field in __ignore_fields
        except Exception as error:
            Utils.show_message(f"Error in __ignore_base_fields: {error}", error=True)

    def __get_snippet(self, path=None, file_name=None, state_manager=False):
        """Método para recuperar o valor do arquivo de snippet a ser convertido pela substituição com os valores 
        baseados em modelos do projeto Django

        Arguments:
            path {str} - Caminho do arquivo snippet a ser utilizado como padrão para gerar o arquivo resultante.
            file_name {str} - Nome do arquivo snippet a ser lido
            state_manager {bool} - Booleano para determinar se o snippet a ser lido é de algum dos pacotes
                                   de gerência de estado do projeto Fastapi (deprecated)

        Returns:
            str -- Texto base a ser utilizado para geração dos arquivos resultantes da conversão
        """

        try:
            if os.path.isfile(path):
                with open(path, encoding="utf-8") as arquivo:
                    return arquivo.read()
        except Exception as e:
            Utils.show_message(f"Error in get_snippet {e}", error=True)
            sys.exit()

    def __init_fastapi(self):
        """Método para iniciar o projeto Fastapi 
        """
        try:
            if not Utils.check_dir(self.fastapi_dir):
                Utils.show_message("Criando o projeto Fastapi.")
                __cmd_fastapi_create = "git clone https://github.com/claysllanxavier/fastapi-to-do.git {}".format(self.fastapi_dir)
                __cmd_remove_git = "cd {} && rm -rf .git".format(self.fastapi_dir)
                subprocess.call(__cmd_fastapi_create, shell=True)
                subprocess.call(__cmd_remove_git, shell=True)
                Utils.show_message("Projeto criado com sucesso.")
        except Exception as error:
            Utils.show_message(f"Error in __init_Fastapi: {error}", error=True)
    
    def __init_app(self, app_path):
        """Método para iniciar o projeto Fastapi 
        """
        try:
            if not Utils.check_dir(app_path):
                Utils.show_message("Criando diretório da app")
                os.makedirs(app_path)
                Utils.show_message("Diretório criado com sucesso")
        except Exception as error:
            Utils.show_message(f"Error in __init_Fastapi: {error}", error=True)

    def __apply_pep(self, path):
        try:
            os.system('autopep8 --in-place --aggressive --aggressive {}'.format(path))
            os.system('isort {}'.format(path))
        except Exception as error:
            Utils.show_message(f"Ocorreu o erro : {error}")
            pass

    def __manage_schema(self):
        """Método responsável por criar/configurar o arquivo de schema para a FastAPI """
        try:
            Utils.show_message("Trabalhando na configuração do Schema do model {}".format(self.model))
            
            content = self.__get_snippet(Path(
            f"{self.path_core}/management/commands/snippets/fastapi/schema.txt"))
            # Interpolando os dados
            content = content.replace("$ModelClass$", self.model)
            model = self.app_instance.get_model(self.model)
            fields = model._meta.fields
            result = ''
            for field in iter(fields):
                item = {}
                item["app"], item["model"], item["name"] = str(field).split('.')
                item["type"] = (str(
                    str(type(field)).split('.')[-1:])
                                .replace("[\"", "").replace("\'>\"]", ""))
                if item["type"] not in self._django_types:
                    print('Campo {} desconhecido'.format(field))
                    continue
                if not self.__ignore_base_fields(item['name']):
                    attribute = self._schemas_types[self._django_types.index(item['type'])]
                    field_name = item.get('name')
                    if (getattr(field, 'null', None)):
                        attribute = f"Optional[{attribute}]"
                    if (field.get_default() is not None and field.get_default() != ""):
                        attribute += f" = {field.get_default()}"
                    if (item.get("type") in ('ForeignKey', 'OneToOneField')):
                        field_name = field.get_attname_column()[1]
                    result += f"\t {field_name}: {attribute}\n"
            content = content.replace("$fields$", result)

            # Verificando se o arquivo forms.py existe
            if self._check_file(self.path_schema) is False:
                # Criando o arquivo com o conteúdo da interpolação
                with open(self.path_schema, 'w') as arquivo:
                    arquivo.write(content)
                self.__apply_pep(self.path_schema)
                return
            # Verificando se já existe configuração no forms para o
            # Models informado
            if self.__check_content(
                    self.path_schema, "class {}".format(self.model)):
                Utils.show_message("O model informado já possui schema configurado.")
                return

            with open(self.path_schema, 'a') as schema:
                schema.write("\n")
                schema.write(content)
            self.__apply_pep(self.path_schema)
        except Exception as error:
            Utils.show_message(f"Error in __manage_schema: {error}", error=True)

  

    
    def call_methods(self, options):
        """
        Método que identifica qual comando foi solicitado pelo usuário para ser executado, antes de chamar o método,
        as entradas informadas pelo usuário são validadas, evitando erros de execução do programa devido à ausência de
        parâmetros obrigatórios. 
            
        Por uma questão de padrão de projeto as possibilidades de escolha do pacote de gerência
        de estados para o projeto Fastapi foram alteradas, agora todo projeto gerado utiliza como pacote de gerência 
        de estado o pacote o Cubit/Bloc
        """
        self.__manage_schema()

    def handle(self, *args, **options):

        app = options["App"] or None
        model = options["Model"] or None

        if app is None and model is None:
            Utils.show_message(
                f"Você não informou uma APP para ser gerada.",
                error=True)
            return
        
        if app and Utils.contain_number(app):
                Utils.show_message(f"Nome da app contendo números")
                return

         # Removendo os espaços em branco
        self.app = app.strip()
        # Pegando o diretório absoluto atual do projeto.
        self.path_root = os.path.normpath(os.getcwd() + os.sep)
        # Criando o path para a APP informada.
        self.path_app = os.path.join(self.fastapi_dir, app)
        self.path_app_local = os.path.join(self.path_root, app)
        # Criando o path para a APP Core.
        self.path_core = os.path.join(self.BASE_DIR, "core")
        # Criando o path para os models baseado no App informada.
        self.path_model = os.path.join(self.path_app_local, "models.py")
        # Convertendo os nomes para caracteres minúsculo.
        # para serem usado nos locais que necessitem dos nomes
        # em minúsculo.
        self.app_lower = app.lower()

        # Criando o path para os forms baseado na App informada.
        self.path_schema= os.path.join(self.path_app, "schemas.py")
       
        # Verificando se o diretório da App informada existe
        if self._check_dir(self.fastapi_dir) is False:
            self.__init_fastapi()

        # Verifica se app esta instalada, pois precisa dela
        # para recuperar as instancias dos models
        if apps.is_installed(self.app_lower) is False:
            Utils.show_message(
                "Você deve colocar sua app no INSTALLED_APPS do settings.")
            return
        
        if self._check_dir(self.path_app) is False:
            self.__init_app(self.path_app)

        # Criando uma instancia da app
        self.app_instance = apps.get_app_config(self.app_lower)
        # Verificando se o usuário passou o nome do model
        if options['Model']:
            model = options['Model'] or None
            if Utils.contain_number(model) is False:
                # Removendo os espaços em branco
                self.model = model.strip()
                # Verificando se existe no models.py o Model informado
                if self.__check_content(
                        self.path_model,
                        'class {}'.format(self.model)) is False:
                    Utils.show_message("Model informado não encontrado.")
                    return
            try:
                # Verifica se o model está na app informada
                # Se o model for abstract ela retornará uma exceção
                # LookupError
                self.app_instance.get_model(self.model)
                Utils.show_message(
                    "Gerando arquivos para o model {}".format(self.model))
                # Convertendo os nomes para caracteres minúsculo.
                # para serem usado nos locais que necessitem dos nomes
                # em minúsculo.
                self.model_lower = model.lower()
                self.call_methods(options)
                Utils.show_message("Processo concluído.")
            except LookupError:
                Utils.show_message(
                    "Esse model é abastrato. "
                    "Não vão ser gerados os arquivos.")
        else:
            # recupera todos os models da app
            # print(self.app_instance.get_models())
            for model in self.app_instance.get_models():
                model = model.__name__
                # Removendo os espaços em branco
                self.model = model.strip()
                Utils.show_message(
                    "Gerando arquivos para o model {}".format(self.model))
                # Convertendo os nomes para caracteres minúsculo.
                # para serem usado nos locais que necessitem dos nomes
                # em minúsculo.
                self.model_lower = model.lower()
                # Chama os métodos de geração de arquivos
                self.call_methods(options)
                Utils.show_message(
                    "Processo concluído para o model {}.".format(
                        self.model))
            Utils.show_message("Processo concluído.")
            return

      