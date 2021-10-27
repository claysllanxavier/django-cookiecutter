import os
import platform
import subprocess
import sys
from pathlib import Path

from core.management.commands.utils import Utils
from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """Manager responsável por analisar as classes de modelos do projeto Django para gerar os arquivos 
    do projeto FastAPI correspondente às apps do Django"""

    def __init__(self):
        super().__init__()
        self.path_root = os.getcwd()
        self.path_core = os.path.join(self.BASE_DIR, "core")
        self.operation_system = platform.system().lower()


        self.project = 'fastapi'
        self.fastapi_dir = os.path.join(self.BASE_DIR, "fastapi")
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
                     "TimeField", "URLField", "UUIDField", "ForeignKey", "OneToOneField"]

    _schemas_types = ["int", "int", "BLANK_CHOICE_DASH", "int", "int", "str", "bool", "str", "str", "datetime.date",
                      "datetime.datetime", "float", "int", "EmailStr", "str", "str", "str", "str", "str", "float",
                      "str", "str", "int", "str", "str", "bool", "str", "int", "int", "str", "int",
                      "str", "DateTime", "str", "str", "int", "int",]
    
    _models_types = ["Integer", "Integer", "BLANK_CHOICE_DASH", "Integer", "Integer", "String", "Boolean", "String", "String", "Date",
                      "Datetime", "Float", "Integer", "String", "String", "String", "String", "String", "String", "Float",
                      "String", "String", "Integer", "String", "String", "Boolean", "String", "Integer", "Integer", "String", "Integer",
                      "String", "DateTime", "String", "String", "Integer", "Integer", ]


    def add_arguments(self, parser):
        parser.add_argument("App", type=str, nargs="?")
        parser.add_argument("Model", type=str, nargs="?")
        parser.add_argument("--app", action="store_true", dest="app", help="Criar a App e seus models")
        parser.add_argument("--app_model", action="store_true", dest="app_model",
                            help="Criar a App e o Model informado")

         # Parâmetro opcionais
        parser.add_argument(
            '--schemas',
            action='store_true',
            dest='schemas',
            help='Criar apenas os Schemas'
        )
        parser.add_argument(
            '--api',
            action='store_true',
            dest='api',
            help='Criar apenas as rotas da api'
        )
        parser.add_argument(
            '--cruds',
            action='store_true',
            dest='cruds',
            help='Criar apenas os cruds'
        )
        parser.add_argument(
            '--models',
            action='store_true',
            dest='models',
            help='Criar apenas os models'
        )

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
    
    
    def __manage_model(self):
        """Método responsável por criar/configurar o arquivo de schema para a FastAPI """
        try:
            Utils.show_message("Trabalhando na configuração do Model do model {}".format(self.model))
            
            content = self.__get_snippet(Path(
            f"{self.path_core}/management/commands/snippets/fastapi/model.txt"))
            # Interpolando os dados
            content = content.replace("$ModelClass$", self.model)
            model = self.app_instance.get_model(self.model)
            content = content.replace("$table$", model._meta.db_table)
            fields = model._meta.fields
            related_fields = model._meta.many_to_many
            result = ''
            imports = ""
            many_to_many = ""
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
                    attribute = self._models_types[self._django_types.index(item['type'])]
                    field_name = item.get('name')
                    relationship = None
                    if (field.max_length):
                        attribute += f"({field.max_length})"
                    if (item.get("type") in ('ForeignKey', 'OneToOneField')):
                        field_name = field.get_attname_column()[1]
                        __model = field.related_model._meta
                        attribute = f"ForeignKey('{__model.db_table}.id')"
                        if __model.app_label != item.get('app'):
                            imports += f"from {__model.app_label}.models import {__model.object_name}\n"
                        relationship = f"\t {item.get('name')} = relationship('{__model.object_name}')\n"
                 
                    attribute = f"{attribute}, nullable={(getattr(field, 'null', None))}"
                    if (field.has_default()):
                        attribute += f" ,default={field.get_default()}"
                    if (field.unique):
                        attribute += f" ,unique={field.unique}"
                    result += f"\t {field_name} = Column({attribute})\n"
                    if relationship is not None:
                        result += relationship
            for field in iter(related_fields):
                item = {}
                item["app"], item["model"], item["name"] = str(field).split('.')
                item["type"] = (str(
                    str(type(field)).split('.')[-1:])
                                .replace("[\"", "").replace("\'>\"]", ""))
                if (item.get("type") == "ManyToManyField"):
                        _model_name = field.model._meta.model_name
                        _related_model_name = field.related_model._meta.model_name
                        __model = field.related_model._meta
                        table = f"{item.get('app')}_{_model_name}_{field.related_model._meta.model_name}"
                        many_to_many += f"{table} = Table('{table}', Base.metadata,"
                        many_to_many += f"Column(Integer, primary_key=True, index=True),"
                        many_to_many += f"Column('{_model_name}_id', ForeignKey('{_model_name}.id')),"
                        many_to_many += f"Column('{_related_model_name}_id', ForeignKey('{_related_model_name}.id')))\n"
                        result += f"\t {item.get('name')} = relationship('{__model.object_name}', secondary={table})\n"
            content = content.replace("$columns$", result)
            content = content.replace("$imports$", imports)
            content = content.replace("$manyToMany$", many_to_many)

            # Verificando se o arquivo forms.py existe
            if self._check_file(self.path_model_fastapi) is False:
                # Criando o arquivo com o conteúdo da interpolação
                with open(self.path_model_fastapi, 'w') as arquivo:
                    arquivo.write(content)
                self.__apply_pep(self.path_model_fastapi)
                return
            # Verificando se já existe configuração no forms para o
            # Models informado
            if self.__check_content(
                    self.path_model_fastapi, "class {}".format(self.model)):
                Utils.show_message("O model informado já possui model configurado.")
                return

            with open(self.path_model_fastapi, 'a') as schema:
                schema.write("\n")
                schema.write(content)
            self.__apply_pep(self.path_model_fastapi)
        except Exception as error:
            Utils.show_message(f"Error in __manage_model: {error}", error=True)

    def __manage_cruds(self):
        """Método responsável por criar/configurar o arquivo de cruds para a FastAPI """
        try:
            Utils.show_message("Trabalhando na configuração do Crud do model {}".format(self.model))
            
            content = self.__get_snippet(Path(
            f"{self.path_core}/management/commands/snippets/fastapi/cruds.txt"))
            # Interpolando os dados
            content = content.replace("$ModelClass$", self.model)
            content = content.replace("$app$", self.app)
            content = content.replace("$model$", self.model_lower) 
            # Verificando se o arquivo forms.py existe
            if self._check_file(self.path_crud) is False:
                # Criando o arquivo com o conteúdo da interpolação
                with open(self.path_crud, 'w') as arquivo:
                    arquivo.write(content)
                self.__apply_pep(self.path_crud)
                return
            # Verificando se já existe configuração no forms para o
            # Models informado
            if self.__check_content(
                    self.path_crud, "class {}".format(self.model)):
                Utils.show_message("O model informado já possui schema configurado.")
                return

            with open(self.path_crud, 'a') as crud:
                crud.write("\n")
                crud.write(content)
            self.__apply_pep(self.path_crud)
        except Exception as error:
            Utils.show_message(f"Error in __manage_crud: {error}", error=True)
   
    def __manage_api(self):
        """Método responsável por criar/configurar o arquivo de cruds para a FastAPI """
        try:
            Utils.show_message("Trabalhando na configuração das Rotas do model {}".format(self.model))
            
            content = self.__get_snippet(Path(
            f"{self.path_core}/management/commands/snippets/fastapi/api.txt"))
            # Interpolando os dados
            content = content.replace("$ModelClass$", self.model)
            content = content.replace("$app$", self.app)
            content = content.replace("$model$", self.model_lower) 
            # Verificando se o arquivo forms.py existe
            if self._check_file(self.path_api) is False:
                # Criando o arquivo com o conteúdo da interpolação
                with open(self.path_api, 'w') as arquivo:
                    arquivo.write(content)
                self.__apply_pep(self.path_api)
                return
            # Verificando se já existe configuração no forms para o
            # Models informado
            if self.__check_content(
                    self.path_api, "class {}".format(self.model)):
                Utils.show_message("O model informado já possui schema configurado.")
                return

            if self.__check_content(self.path_api,
                                    "router = APIRouter()"):
                content = content.replace("router = APIRouter()", "")

            with open(self.path_api, 'a') as crud:
                crud.write("\n")
                crud.write(content)
            self.__apply_pep(self.path_api)
        except Exception as error:
            Utils.show_message(f"Error in __manage_crud: {error}", error=True)

  

    
    def call_methods(self, options):
        """
        Método que identifica qual comando foi solicitado pelo usuário para ser executado, antes de chamar o método,
        as entradas informadas pelo usuário são validadas, evitando erros de execução do programa devido à ausência de
        parâmetros obrigatórios. 
            
        Por uma questão de padrão de projeto as possibilidades de escolha do pacote de gerência
        de estados para o projeto Fastapi foram alteradas, agora todo projeto gerado utiliza como pacote de gerência 
        de estado o pacote o Cubit/Bloc
        """
        # Verificando se foram passados parâmetros opcionais
        if options['cruds']:
            Utils.show_message("Trabalhando apenas os cruds.")
            self.__manage_cruds()
            return
        elif options['api']:
            Utils.show_message("Trabalhando apenas a api.")
            self.__manage_api()
            return
        elif options['schemas']:
            Utils.show_message("Trabalhando apenas os schemas.")
            self.__manage_schema()
            return
        elif options['models']:
            Utils.show_message("Trabalhando apenas os models.")
            self.__manage_model()
            return
        else:
            # Chamando o método para tratar os api
            self.__manage_api()
            # Chamando o método para tratar as schemas
            self.__manage_schema()
            # Chamando o método para tratar o models
            self.__manage_model()
            # Chamando o método para tratar as cruds
            self.__manage_cruds()
            return

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
        self.path_model_fastapi = os.path.join(self.path_app, "models.py")
        self.path_crud = os.path.join(self.path_app, "cruds.py")
        self.path_api = os.path.join(self.path_app, "api.py")
       
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

      