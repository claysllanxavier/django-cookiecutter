"""Esse manager é responsável por gerar os arquivos padrões de um projeto Django (templates, urls, views, forms)
baseado nas informações contidas na classe da App do projeto Django.
"""

import fileinput
import os
from pathlib import Path

from bs4 import BeautifulSoup
from core.management.commands.utils import Utils
from django.apps import apps
from django.core.management.base import BaseCommand
from django.urls import resolve, reverse


class Command(BaseCommand):
    help = "Manager responsável por gerar os arquivos padrões de um projeto Django."

    BASE_DIR = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    def __init__(self):
        super().__init__()
        self.path_root = os.getcwd()
        self.path_core = os.path.join(self.BASE_DIR, "core")
        self._snippet_index_view = self.__get_snippet(
            Path(f"{self.path_core}/management/commands/snippets/django/index_view.txt"))
        self._snippet_crud_view = self.__get_snippet(
            Path(f"{self.path_core}/management/commands/snippets/django/crud_views.txt"))
        self._snippet_crud_urls = self.__get_snippet(
            Path(f"{self.path_core}/management/commands/snippets/django/crud_urls.txt"))
        self._snippet_index_template = self.__get_snippet(
            Path(f"{self.path_core}/management/commands/snippets/django/indextemplate.txt"))
        self._snippet_detail_template = self.__get_snippet(
            Path(f"{self.path_core}/management/commands/snippets/django/detailtemplate.txt"))
        self._snippet_list_template = self.__get_snippet(Path(
            f"{self.path_core}/management/commands/snippets/django/listtemplate.txt"))
        self._snippet_update_template = self.__get_snippet(Path(
            f"{self.path_core}/management/commands/snippets/django/updatetemplate.txt"))
        self._snippet_crud_modal_template = self.__get_snippet(
            Path(f"{self.path_core}/management/commands/snippets/django/crud_form_modal.txt"))
        self._snippet_url = self.__get_snippet(
            Path(f"{self.path_core}/management/commands/snippets/django/url.txt"))
        self._snippet_urls_imports = self.__get_snippet(
            Path(f"{self.path_core}/management/commands/snippets/django/url_imports.txt"))
        self._snippet_modal_foreign_key = self.__get_snippet(
            Path(f"{self.path_core}/management/commands/snippets/django/modal_form.txt"))
        self._snippet_api_router = self.__get_snippet(
            Path(f"{self.path_core}/management/commands/snippets/django/api_router.txt"))
        self._snippet_api_routers = self.__get_snippet(
            Path(f"{self.path_core}/management/commands/snippets/django/api_router_urls.txt"))
        self._snippet_api_view = self.__get_snippet(
            Path(f"{self.path_core}/management/commands/snippets/django/api_view.txt"))
        self._snippet_api_urls = self.__get_snippet(
            Path(f"{self.path_core}/management/commands/snippets/django/api_urls.txt"))
        self._snippet_serializer = self.__get_snippet(Path(
            f"{self.path_core}/management/commands/snippets/django/serializer.txt"))
        self._snippet_serializer_url = self.__get_snippet(
            Path(f"{self.path_core}/management/commands/snippets/django/serializer_urls.txt"))
        self._snippet_form = self.__get_snippet(
            Path(f"{self.path_core}/management/commands/snippets/django/form.txt"))
        self._snippet_form_url = self.__get_snippet(
            Path(f"{self.path_core}/management/commands/snippets/django/form_urls.txt"))
        self._snippet_create_template = self.__get_snippet(
            Path(f"{self.path_core}/management/commands/snippets/django/createtemplate.txt"))
        self._snippet_delete_template = self.__get_snippet(Path(
            f"{self.path_core}/management/commands/snippets/django/deletetemplate.txt"))

    def add_arguments(self, parser):
        parser.add_argument('App', type=str)
        parser.add_argument('Model', type=str, nargs='?')
        parser.add_argument('--templates', action='store_true', dest='templates', help='Criar apenas os Templates')
        parser.add_argument('--api', action='store_true', dest='api', help='Criar apenas a API')
        parser.add_argument('--urls', action='store_true', dest='url', help='Criar apenas as Urls')
        parser.add_argument('--forms', action='store_true', dest='forms', help='Criar apenas o Form')
        parser.add_argument('--views', action='store_true', dest='views', help='Criar apenas as Views (CRUD)')
        parser.add_argument('--parserhtml', action='store_true', dest='renderhtml',
                            help='Renderizar os fields do models para HTML')
        parser.add_argument('--format', action='store_true', dest='format', help='Aplicar PEP8 nos arquivos')

    def __get_verbose_name(self, app_name=None, model_name=None):
        """Método responsável por recuperar o verbose_name do model da App Django."""
        return Utils.get_verbose_name(apps, app_name=app_name, model_name=model_name)

    def __check_dir(self, path) -> bool:
        """Método responsável por verificar se o diretório já existe."""
        return Utils.check_dir(path)

    def __check_file(self, path):
        """Método responsável por verificar se o arquivo já existe no caminho informado."""
        return Utils.check_file(path)

    def __check_content(self, path, text_check):
        """Método responsável por verificar se o texto passado com parâmetro existe no conteúdo do arquivo."""
        return Utils.check_content(path, text_check)

    def __check_file_is_locked(self, path):
        """Método responsável por verificar se o arquivo está travado para renderização/conversão"""
        return Utils.check_file_is_locked(path)

    def __get_snippet(self, path):
        """Método para recuperar o conteúdo do arquivo de modelo para ser utilizado na geração dos demais arquivos."""
        return Utils.get_snippet(path)

    def __get_model(self):
        """Método responsável para recuperar a instância da class da App"""
        try:
            return apps.get_model(self.app, self.model)
        except Exception as error:
            Utils.show_message(f"Error in __get_model : {error}", error=True)
            return None

    def __apply_pep(self):
        try:
            __items_apply_pep8 = [self.path_urls, self.path_form, self.path_views, self.path_serializer,
                                  self.path_api_urls, self.path_api_views]
            for element in __items_apply_pep8:
                os.system('autopep8 --in-place --aggressive --aggressive {}'.format(element))
                os.system('isort {}'.format(element))
        except Exception as error:
            Utils.show_message(f"Ocorreu o erro : {error}")
            pass

    def __manage_index_template(self):
        """Método responsável por gerar o template index.html da app"""
        try:
            Utils.show_message("Trabalhando na configuração do template inicial da APP")
            path = Path(f"{self.path_template_dir}/index.html")
            if self.__check_file_is_locked(path):
                return
            content = self._snippet_index_template
            _title = self.__get_verbose_name(app_name=self.app.lower()) or self.app.lower()
            content = content.replace("$titlepage$", _title)
            content = content.replace("$title$", _title)
            content = content.replace("$app_name$", self.app_lower)
            with open(path, 'w', encoding='utf-8') as template:
                template.write(content)
        except Exception as error:
            Utils.show_message(f"Error in __manage_index_template: {error}", error=True)

    def __manage_detail_template(self):
        """Método responsável por gerar o template detail.html da app"""
        try:
            Utils.show_message("Trabalhando na configuração do template de Detalhamento.")
            path = Path(
                f"{self.path_template_dir}/{self.model_lower}_detail.html")
            if self.__check_file_is_locked(path):
                return
            content = self._snippet_detail_template
            _title = self.__get_verbose_name(app_name=self.app.lower()) or self.app.lower()
            content = content.replace("$title$", _title)
            content = content.replace("$model_name$", self.model_lower)
            content = content.replace("$url_back$", '{}:{}-list'.format(self.app_lower, self.model_lower))
            content = content.replace("$app_name$", self.app_lower)
            with open(path, 'w', encoding='utf-8') as template:
                template.write(content)
        except Exception as error:
            Utils.show_message(f"Error in __manage_detail_template : {error}")

    def __manage_list_template(self):
        """Método responsável por gerar o template list.html da app"""
        try:
            Utils.show_message("Trabalhando na configuração do template de Listagem.")
            path = Path(f"{self.path_template_dir}/{self.model_lower}_list.html")
            if self.__check_file_is_locked(path):
                return
            content = self._snippet_list_template
            _title = self.__get_verbose_name(app_name=self.app.lower(), model_name=self.model_lower) or self.app.lower()
            content = content.replace("$title$", _title)
            content = content.replace("$label_count_item$", self.model)
            content = content.replace("$model_name$", self.model_lower)
            content = content.replace("$app_name$", self.app_lower)
            with open(path, 'w', encoding='utf-8') as template:
                template.write(content)

        except Exception as error:
            Utils.show_message(f"Error in __manage_list_template : {error}")

    def __manage_update_template(self):
        """Método responsável por gerar o template update.html da app"""
        try:
            Utils.show_message("Trabalhando na configuração do template de Atualização.")
            path = Path(f"{self.path_template_dir}/{self.model_lower}_update.html")
            if self.__check_file_is_locked(path):
                return
            content = self._snippet_update_template
            _title = self.__get_verbose_name(app_name=self.app.lower(), model_name=self.model_lower) or self.app.lower()
            content = content.replace("$title$", _title)
            content = content.replace("$app_name$", self.app_lower)
            content = content.replace("$model_name$", self.model_lower)

            with open(path, 'w', encoding='utf-8') as template:
                template.write(content)

        except Exception as error:
            Utils.show_message(f"Error in __manage_update_template: {error}")

    def __manage_create_template(self):
        """Método responsável por gerar o template create.html da app"""
        try:
            Utils.show_message("Trabalhando na configuração do template de Criação.")
            path = Path(f"{self.path_template_dir}/{self.model_lower}_create.html")
            if self.__check_file_is_locked(path):
                return
            content = self._snippet_create_template
            _title = self.__get_verbose_name(app_name=self.app.lower(), model_name=self.model_lower) or self.app.lower()
            content = content.replace("$title$", _title)
            content = content.replace("$app_name$", self.app_lower)
            with open(path, 'w', encoding='utf-8') as template:
                template.write(content)

        except Exception as error:
            Utils.show_message(f"Error in __manage_create_template : {error}")

    def __manage_delete_template(self):
        """Método responsável por gerar o template delete.html da app"""
        try:
            Utils.show_message("Trabalhando na configuração do template de Exclusão.")
            path = Path(f"{self.path_template_dir}/{self.model_lower}_delete.html")
            if self.__check_file_is_locked(path):
                return
            content = self._snippet_delete_template
            _title = self.__get_verbose_name(app_name=self.app.lower(), model_name=self.model_lower) or self.app.lower()
            content = content.replace("$app_name$", self.app_lower)
            content = content.replace("$model_name$", self.model_lower)
            content = content.replace("$title$", _title)
            with open(path, 'w', encoding='utf-8') as template:
                template.write(content)

        except Exception as error:
            Utils.show_message(f"Error in __manage_delete_template : {error}")

    def __manage_templates(self):
        """Método principal para chamar os demais métodos de geração dos templates da App/Model"""
        try:
            if self.__check_dir(self.path_template_dir) is False:
                Utils.show_message("Criando o diretório dos Templates")
                os.makedirs(self.path_template_dir)
            self.__manage_index_template()
            self.__manage_detail_template()
            self.__manage_list_template()
            self.__manage_create_template()
            self.__manage_delete_template()
            self.__manage_update_template()
        except Exception as error:
            Utils.show_message(f"Error in __manage_templates : {error}", error=True)

    def __manage_api_url(self):
        """Método responsável por criar/configurar o arquivo de urls para a APIRest (DRF) """
        try:
            Utils.show_message("Trabalhando na configuração das Urls API do model {}".format(self.model))
            content = self._snippet_api_router
            content = content.replace("$app_name$", self.app_lower)
            content = content.replace("$model_name$", self.model_lower)
            content = content.replace("$ModelName$", self.model)

            if self.__check_file(self.path_api_urls) is False:
                api_url_file = open(self.path_api_urls, 'w', encoding='utf-8')
                api_url_file.write(content)
                return
            content_file = open(self.path_api_urls, 'r', encoding='utf-8')

            if content_file.read().find(f"{self.model}ViewAPI") != -1:
                return

            # Variável que conterá o código sem o urlpatterns
            content_without_router = ""

            # Abrindo o arquivo para ler o conteúdo
            with open(self.path_api_urls, 'r', encoding='utf-8') as read_api_urls_content:
                content_without_router = read_api_urls_content.read()

            # removendo o conteúdo router = router.urls
            content_without_router = content_without_router.replace("urlpatterns = router.urls", "")
            content_without_router = content_without_router.strip()

            # Abrindo o arquivo para gravar o novo valor
            with open(self.path_api_urls, 'w', encoding='utf-8') as update_content_file:
                update_content_file.write(content_without_router)

            with open(self.path_api_urls, 'a', encoding='utf-8') as api_url_file:
                content = content.replace("router = routers.DefaultRouter()", "")
                content = content.replace("from django.urls import include, path", "")
                content = content.replace("from rest_framework import routers", "")
                api_url_file.write(content)

        except Exception as error:
            print("Error ", error)
            Utils.show_message(f"Ocorreu o erro : {error} no __manage_api_url")

    def __manage_api_view(self):
        """Método responsável por criar/configurar o arquivo de views para a APIRest (DRF) """
        try:
            Utils.show_message("Trabalhando na configuração das Views da API do model {} ".format(self.model))
            content = self._snippet_api_view
            content_urls = self._snippet_api_urls
            content = content.replace("$ModelName$", self.model)
            content_urls = content_urls.replace("$ModelName$", self.model)
            if self.__check_file(self.path_api_views) is False:
                with open(self.path_api_views, 'w', encoding='utf-8') as api_views_file:
                    api_views_file.write(content_urls + content)
                return

            if self.__check_content(self.path_api_views, " {}ViewAPI".format(self.model)):
                Utils.show_message("O model informado já possui views da API configurado.")
                return

            # Verificando se o from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
            # Já existe no arquivo
            if self.__check_content(self.path_api_views, "from rest_framework.viewsets import ModelViewSet"):
                content = content.replace("from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet", "")
                content = content.strip()

            # Verificando se o from drf_jsonmask.views import OptimizedQuerySetMixin
            # Já existe no arquivo
            if self.__check_content(self.path_api_views, "from drf_jsonmask.views import OptimizedQuerySetMixin"):
                content = content.replace("from drf_jsonmask.views import OptimizedQuerySetMixin", "")
                content = content.strip()

            # Verificando se o from rest_framework import filters
            # Já existe no arquivo
            if self.__check_content(self.path_api_views, "from rest_framework import filters"):
                content = content.replace("from rest_framework import filters, status", "")
                content = content.strip()

            # Verificando se o from rest_framework.permissions import IsAuthenticated
            # Já existe no arquivo
            if self.__check_content(self.path_api_views, "from rest_framework.permissions import IsAuthenticated"):
                content = content.replace("from rest_framework.permissions import IsAuthenticated", "")
                content = content.strip()

            # Verificando se o from rest_framework.decorators import permission_classes
            # Já existe no arquivo
            if self.__check_content(self.path_api_views, "from rest_framework.decorators import permission_classes"):
                content = content.replace("from rest_framework.decorators import permission_classes", "")
                content = content.strip()

            if self.__check_content(self.path_api_views, self.model) is False:
                content_models = content_urls.split("\n")[5]
                api_views_file = open(self.path_api_views, "r", encoding='utf-8')
                data = []
                for line in api_views_file:
                    if line.startswith('from .models import'):
                        line = line.replace("\n", "") + f", {self.model} \n"
                    data.append(line)
                api_views_file.close()

                api_views_file = open(self.path_api_views, "w", encoding='utf-8')
                api_views_file.writelines(data)
                api_views_file.close()
            else:
                content_urls = content_urls.rsplit("\n", 1)[0]

            if self.__check_content(self.path_api_views, "from rest_framework.viewsets import ModelViewSet"):
                content_urls = content_urls.split("\n")[4]
                api_views_file = open(self.path_api_views, "r", encoding='utf-8')
                data = []
                for line in api_views_file:
                    if line.startswith('from .serializers import'):
                        line = line.replace("\n", ", ") + content_urls.replace("from .serializers import", "") + "\n"
                    data.append(line)
                api_views_file.close()

                api_views_file = open(self.path_api_views, "w", encoding='utf-8')
                api_views_file.writelines(data)
                api_views_file.close()
            else:
                with open(self.path_api_views, 'a', encoding='utf-8') as views:
                    views.write("\n")
                    views.write(content_urls)

            with open(self.path_api_views, 'a', encoding='utf-8') as api_views:
                api_views.write("\n")
                api_views.write(content)
        except Exception as error:
            Utils.show_message(f"Error in __manage_api_view: {error}", error=True)

    def __manage_serializer(self):
        """Método responsável por criar/configurar o arquivo de serializer para a APIRest (DRF) """
        try:
            Utils.show_message("Trabalhando na configuração do Serializer do model {}".format(self.model))
            content = self._snippet_serializer
            content_urls = self._snippet_serializer_url
            content = content.replace("$ModelName$", self.model)
            content = content.replace("$ModelClass$", self.model)
            content_urls = content_urls.replace("$ModelName$", self.model)
            if self.__check_file(self.path_serializer) is False:
                with open(self.path_serializer, 'w', encoding='utf-8') as arquivo:
                    arquivo.write(content_urls + '\n\n' + content)
                return

            if self.__check_file_is_locked(self.path_serializer) is True:
                return

            if self.__check_content(self.path_serializer, "class {}Serializer".format(self.model)):
                Utils.show_message("O model informado já possui serializer configurado.")
                return

            # Verificando se o from drf_jsonmask.serializers import FieldsListSerializerMixin
            # já existe no arquivo para não importar novamente
            if self.__check_content(self.path_serializer,
                                    "from drf_jsonmask.serializers import FieldsListSerializerMixin"):
                content = content.replace("from drf_jsonmask.serializers import FieldsListSerializerMixin", "")

            if self.__check_content(self.path_serializer, "from rest_framework.serializers import ModelSerializer"):
                content_urls = content_urls.split("\n")[1]
                serializer_file = open(self.path_serializer, "r")
                data = []
                for line in serializer_file:
                    if line.startswith('from .models import'):
                        models = line.split('import')[-1].rstrip()
                        import_model = ', ' + content_urls.split()[-1]
                        models += import_model
                        line = 'from .models import{}\n'.format(models)
                    data.append(line)
                serializer_file.close()

                serializer_file = open(self.path_serializer, "w", encoding='utf-8')
                serializer_file.writelines(data)
                serializer_file.close()
            else:
                with open(self.path_serializer, 'a', encoding='utf-8') as views:
                    views.write(content_urls)
            with open(self.path_serializer, 'a', encoding='utf-8') as urls:
                urls.write("\n")
                urls.write(content)
        except Exception as error:
            Utils.show_message(f"Error in __manage_serializer : {error}")

    def __manage_form(self):
        """Método responsável por criar/configurar o arquivo forms.py"""
        try:
            Utils.show_message("Trabalhando na configuração do Form do model {}".format(self.model))
            content = self._snippet_form
            content_urls = self._snippet_form_url
            content = content.replace("$ModelClass$", self.model)
            content_urls = content_urls.replace("$ModelClass$", self.model)

            if self.__check_file(self.path_form) is False:
                with open(self.path_form, 'w', encoding='utf-8') as arquivo:
                    arquivo.write(content_urls + '\n' + content)
                return

            if self.__check_file_is_locked(self.path_form) is True:
                return

            if self.__check_content(self.path_form, "class {}Form".format(self.model)):
                Utils.show_message("O model informado já possui form configurado.")
                return

            if self.__check_content(self.path_form, "from core.forms import BaseForm"):
                content_urls = content_urls.split("\n")[1]
                arquivo = open(self.path_form, "r", encoding='utf-8')
                data = []
                for line in arquivo:
                    if line.startswith('from .models import'):
                        models = line.split('import')[-1].rstrip()
                        import_model = ', ' + content_urls.split()[-1]
                        models += import_model
                        line = 'from .models import{}\n'.format(models)
                    data.append(line)
                arquivo.close()

                arquivo = open(self.path_form, "w", encoding='utf-8')
                arquivo.writelines(data)
                arquivo.close()
            else:
                with open(self.path_form, 'a', encoding='utf-8') as views:
                    views.write(content_urls)
            with open(self.path_form, 'a', encoding='utf-8') as form:
                form.write("\n")
                form.write(content)
        except Exception as error:
            Utils.show_message(f"Error in __manage_form : {error}")

    def __manage_views(self):
        """Método responsável por criar/configurar o views.py"""
        try:
            __snippet_index_template = self._snippet_index_view
            Utils.show_message("Trabalhando na configuração das Views do model {}".format(self.model))
            content = self._snippet_crud_view
            content_urls = self._snippet_crud_urls
            content = content.replace("$ModelClass$", self.model)
            content = content.replace("$app_name$", self.app_lower)
            content = content.replace("$model_name$", self.model_lower)
            content_urls = content_urls.replace("$ModelClass$", self.model)
            _import_forms_modal = ""
            _model = self.__get_model()
            try:
                if hasattr(_model._meta, 'fk_fields_modal') is True:
                    _forms = ""
                    for fk_name in _model._meta.fk_fields_modal:
                        _field = _model._meta.get_field(fk_name)
                        _field_name = str(_field.related_model).split("'")[1]
                        _field_split = _field_name.split(".")
                        _app_field = _field_split[0]
                        _model_field = _field_split[2]
                        if _app_field != self.app_lower:
                            _import_forms_modal += "\nfrom {}.forms import {}Form".format(
                                _app_field, _model_field)
                        _forms += "{s}context['form_{l}'] = {u}Form\n".format(
                            l=_model_field.lower(), u=_model_field, s=" " * 8)
                    modal_update = self._snippet_crud_modal_template
                    modal_update = modal_update.replace(
                        '$ModelClass$', "{}UpdateView".format(self.model))
                    modal_update = modal_update.replace(
                        '$FormsModal$', _forms.strip())
                    content = content.replace(
                        '$FormsModalUpdate$', modal_update)

                    modal_create = self._snippet_crud_modal_template
                    modal_create = modal_create.replace(
                        '$ModelClass$', "{}CreateView".format(self.model))
                    modal_create = modal_create.replace(
                        '$FormsModal$', _forms.strip())
                    content = content.replace(
                        '$FormsModalCreate$', modal_create)
                else:
                    content = content.replace('$FormsModalCreate$', "")
                    content = content.replace('$FormsModalUpdate$', "")
            except Exception as error:
                Utils.show_message(f"Error in __manage_views: {error}")

            try:
                if hasattr(_model._meta, 'fields_display') is True:
                    content = content.replace(
                        '$ListFields$', 'list_display = {}'.format(
                            _model._meta.fields_display))
                else:
                    content = content.replace('$ListFields$', "")
            except Exception as error:
                Utils.show_message(f"Error in __manage_views {error}")

            if self.__check_content(self.path_views, "{}IndexTemplateView".format(self.app.title())) is False:
                __snippet_index_template = __snippet_index_template.replace(
                    "$AppClass$", self.app.title())
                __snippet_index_template = __snippet_index_template.replace(
                    "$app_name$", self.app_lower)
                content = __snippet_index_template + content

            if self.__check_file(self.path_views) is False:
                with open(self.path_views, 'w', encoding='utf-8') as arquivo:
                    arquivo.write(content_urls + '\n' + content)
                return

            if self.__check_content(self.path_views, "class {}ListView".format(self.model)):
                Utils.show_message("O model informado já possui as views configuradas.")
                return

            if self.__check_content(self.path_views, "from core.views"):
                content_models = content_urls.split("\n")[1]
                content_forms = content_urls.split("\n")[2]
                arquivo = open(self.path_views, "r", encoding='utf-8')
                data = []
                for line in arquivo:
                    if line.startswith('from .models import'):
                        models = line.split('import')[-1].rstrip()
                        import_model = ', ' + content_models.split()[-1]
                        models += import_model
                        line = 'from .models import{}\n'.format(models)
                    elif line.startswith('from .forms import'):
                        forms = line.split('import')[-1].rstrip()
                        import_form = ', ' + content_forms.split()[-1]
                        forms += import_form
                        line = 'from .forms import{}\n'.format(forms)
                    data.append(line)
                data.append(_import_forms_modal)
                arquivo.close()

                arquivo = open(self.path_views, "w", encoding='utf-8')
                arquivo.writelines(data)
                arquivo.close()
            else:
                with open(self.path_views, 'a', encoding='utf-8') as views:
                    views.write(content_urls)

            with open(self.path_views, 'a', encoding='utf-8') as views:
                views.write(_import_forms_modal)
                views.write("\n")
                views.write(content)

        except Exception as error:
            Utils.show_message(f"Error in __manage_views : {error}")

    def __manage_urls_api_app(self):
        """Método para adicionar o path da app ao arquivo urls_api.py"""
        try:
            content_exist = False
            new_data = ""
            content_include = "    path('$app_name$/api/v1/', include('$app_name$.api_urls')),".replace("$app_name$", self.app_lower)
            with open(Path(f"{self.BASE_DIR}/base/urls_api.py"), 'r', encoding='utf-8') as urlsapi:
                new_data = urlsapi.read()
                if self.app_lower in new_data:
                    return 
                new_data = new_data.replace("]", f"{content_include}\n]")
            if content_exist is True:
                return 
            with open(Path(f"{self.BASE_DIR}/base/urls_api.py"), 'w', encoding='utf-8') as urlsapi:
                urlsapi.write(new_data)
        except Exception as error:
            print(f"Erro ao executar o __manage_urls_api_app de Build: {error}")

    def __manage_url(self):
        """Método para criar/configurar o arquivo urls.py do model"""
        try:
            Utils.show_message("Trabalhando na configuração das Urls do model {}".format(self.model))
            content = self._snippet_url
            content_urls = self._snippet_urls_imports
            content = content.replace("$app_name$", self.app_lower)
            content = content.replace("$app_title$", self.app_lower.title())
            content = content.replace("$model_name$", self.model_lower)
            content = content.replace("$ModelClass$", self.model)
            content_urls = content_urls.replace("$ModelClass$", self.model)

            if self.__check_file_is_locked(self.path_urls) is True:
                return

            if self.__check_content(self.path_urls, " {}ListView".format(self.model)):
                Utils.show_message("O model informado já possui urls configuradas.")
                return

            # Verificando se já existe o caminho path('api/$app_name$/', include('$app_name$.api_urls')),
            # no arquivo para não importar novamente
            content_include = "path('api/$app_name$/', include('$app_name$.api_urls')),"
            content_include = content_include.replace("$app_name$", self.app_lower)
            if self.__check_content(self.path_urls, content_include):
                content = content.replace(content_include, "").strip()

            if self.__check_content(self.path_urls, "{}IndexTemplateView".format(self.app.title())):
                content_urls = content_urls.replace(", $AppIndexTemplate$", "")
            else:
                content_urls = content_urls.replace("$AppIndexTemplate$",
                                                    "{}IndexTemplateView".format(self.app.title()))
            if self.__check_file(self.path_urls) is False:
                with open(self.path_urls, 'w', encoding='utf-8') as url_file:
                    url_file.write(content_urls + '\n' + content)
                return

            if self.__check_content(self.path_urls, "from .views import"):
                content_urls = content_urls.split("\n")[1]
                url_file = open(self.path_urls, "r", encoding='utf-8')
                data = []
                for line in url_file:
                    if line.startswith('from .views import'):
                        models = line.split('import')[-1].rstrip()
                        import_model = '{}, '.format(content_urls.split('import')[-1].rstrip())
                        models += import_model
                        line = 'from .views import{}\n'.format(models)
                    data.append(line)
                url_file.close()

                url_file = open(self.path_urls, "w", encoding='utf-8')
                url_file.writelines(data)
                url_file.close()
            else:
                with open(self.path_urls, 'a', encoding='utf-8') as views:
                    views.write(content_urls)

            if self.__check_content(self.path_urls, "urlpatterns = ["):
                content = content.replace(
                    "urlpatterns = [", "urlpatterns += [")
                content = content.replace("path('api/{}/', include(router.urls)),\n    ".format(
                    self.app_lower), '')
                _url_index_page = "path('{}/', {}IndexTemplateView.as_view(), name='{}-index'),\n    ".format(
                    self.app_lower, self.app.title(), self.app_lower)
                content = content.replace(_url_index_page, "")

            if self.__check_content(self.path_urls, "app_name = \'{}\'".format(self.app)):
                content = content.replace(
                    "app_name = \'{}\'".format(self.app), "")

            if self.__check_file_is_locked(self.path_urls) is True:
                return

            with open(self.path_urls, 'a', encoding='utf-8') as urls:
                urls.write(content)

        except Exception as error:
            Utils.show_message(f"Error in __manage_url : {error}")

    def __render_modal_foreign_key(self, model, app, model_lower, field_name) -> str:
        """Método responsável por criar o código que gerencia os dados de um campo Fk utilizando um modal do
        Bootstrap """
        try:
            content = self._snippet_modal_foreign_key
            content = content.replace("$ModelName$", model)
            content = content.replace("$app_name$", app)
            content = content.replace("$model_name$", model_lower)
            content = content.replace("$field_name$", field_name)
            return content
        except Exception as error:
            Utils.show_message(f"Ocorreu o erro : {error}")

    def __render_input(self, field) -> str:
        """Método responsável por renderizar os elementos de formulários para os templates HTML"""
        try:
            types = ['AutoField', 'BLANK_CHOICE_DASH', 'BigAutoField', 'BigIntegerField', 'BinaryField', 'BooleanField',
                     'CharField', 'CommaSeparatedIntegerField', 'DateField', 'DateTimeField', 'DecimalField',
                     'DurationField', 'EmailField', 'Empty', 'FileField', 'Field', 'FieldDoesNotExist', 'FilePathField',
                     'FloatField', 'GenericIPAddressField', 'IPAddressField', 'IntegerField', 'FieldFile',
                     'NOT_PROVIDED', 'NullBooleanField', 'ImageField', 'PositiveIntegerField',
                     'PositiveSmallIntegerField', 'SlugField', 'SmallIntegerField', 'TextField', 'TimeField',
                     'URLField', 'UUIDField', 'ForeignKey', 'OneToOneField', 'ManyToManyField', 'OptimizedImageField']
            _model = self.__get_model()
            iten = {}
            iten["app"], iten["model"], iten["name"] = str(field).split('.')
            iten["tipo"] = (str(
                str(type(field)).split('.')[-1:])
                            .replace("[\"", "").replace("\'>\"]", ""))
            if iten["tipo"] in types:
                if iten["tipo"] == 'BooleanField':
                    tag_result = "<div class='form-check col-md-6'>"
                else:
                    tag_result = "<div class='form-group col-md-6'>"
                required = 'required'
                if ((getattr(field, 'blank', None) is True) or
                        (getattr(field, 'null', None) is True)):
                    required = ''
                readonly = getattr(field, 'readonly', '')
                label = "{{{{ form.{}.label_tag }}}}".format(iten['name'])
                help_text = getattr(field, 'help_text', '')
                if iten.get("tipo") in ('ForeignKey', 'OneToOneField'):
                    tag_result += label
                    _foreign_key_field = "\n{{{{ form.{} }}}}".format(
                        iten['name'])
                    if hasattr(_model._meta, 'fk_fields_modal') is True:
                        if iten["name"] in _model._meta.fk_fields_modal:
                            _foreign_key_field = '\n<div class="input-group">'
                            _foreign_key_field += "{{{{ form.{} }}}}\n".format(
                                iten['name'])
                            _foreign_key_field += "{{% if form.{0}.field.queryset.model|{1} %}}".format(
                                iten['name'], "has_add_permission:request"
                            )
                            _foreign_key_field += '<button type="button" class="btn btn-outline-secondary"'
                            _foreign_key_field += ' data-toggle="modal" data-target='
                            _foreign_key_field += '"#form{}Modal">+</button>{{% endif %}}'.format(
                                field.related_model._meta.object_name)
                            _foreign_key_field += '</div>'
                            self.html_modals += self.__render_modal_foreign_key(
                                field.related_model._meta.object_name, iten['app'],
                                field.related_model._meta.model_name, iten['name'])
                    tag_result += _foreign_key_field

                elif iten["tipo"] == 'BooleanField':
                    tag_result += "{{{{ form.{} }}}}\n{}".format(iten['name'], label)
                elif iten["tipo"] == 'ManyToManyField':
                    tag_result += "{}\n{{{{ form.{} }}}}".format(label, iten['name'])
                else:
                    tag_result += "{}\n{{{{ form.{} }}}}".format(label, iten['name'])
                if readonly != '':
                    tag_result = tag_result.replace(
                        "class='", "class='form-control-plaintext ")
                if required != '':
                    tag_result += '\n<div class="invalid-feedback">Campo Requerido.</div>'
                if help_text != '':
                    tag_result += "\n<small class='form-text text-muted'>{{{{ form.{0}.help_text }}}}</small>\n".format(
                        iten['name'])
                tag_result += "{{% if form.{0}.errors  %}}{{{{ form.{0}.errors  }}}}{{% endif %}}".format(
                    iten['name'])
                tag_result += "</div>"
                return tag_result
            else:
                print('Campo {} desconhecido'.format(field))

        except Exception as error:
            Utils.show_message(f"Error in __render_input : {error}")

    def __manage_render_html(self):
        """Método para renderizar o código HTML a ser inserido nos arquivos de template do models."""
        try:
            model = self.__get_model()
            if model is None:
                Utils.show_message("Favor declarar a app no settings.", error=True)
            self.__manage_templates()
            html_tag = ""
            self.html_modals = ""
            __fields = model._meta.fields + model._meta.many_to_many
            for field in iter(__fields):
                if str(field).split('.')[2] not in ('updated_on', 'created_on', 'deleted', 'enabled', 'id'):
                    html_tag += self.__render_input(field)
            if html_tag != '':
                for temp in ['create', 'update']:
                    list_update_create = Path(
                        f"{self.path_template_dir}/{self.model_lower}_{temp}.html")
                    if self.__check_file_is_locked(list_update_create) is True:
                        continue
                    with fileinput.FileInput(list_update_create, inplace=True) as arquivo:
                        for line in arquivo:
                            print(line.replace(
                                "<!--REPLACE_PARSER_HTML-->",
                                BeautifulSoup(html_tag, 'html5lib').prettify().replace(
                                    "<html>", "").replace(
                                    "<head>", "").replace(
                                    "</head>", "").replace(
                                    "<body>", "").replace(
                                    "</body>", "").replace(
                                    "</html>", "").strip()).replace(
                                "$url_back$", '{}:{}-list'.format(
                                    self.app_lower, self.model_lower
                                )), end='')

                    with fileinput.FileInput(list_update_create, inplace=True) as arquivo:
                        for line in arquivo:
                            print(line.replace(
                                "<!--REPLACE_MODAL_HTML-->",
                                self.html_modals).replace(
                                "$url_back$", '{}:{}-list'.format(
                                    self.app_lower, self.model_lower
                                )), end='')
                try:
                    list_view = '{}:{}-list'.format(self.app_lower,
                                                    self.model_lower)
                    fields_display = resolve(
                        reverse(list_view)).func.view_class.list_display
                    thead = ''
                    tline = ''
                    for item in fields_display:
                        app_field = next(
                            (item_field for item_field in model._meta.fields if item == item_field.name), None)
                        if app_field is not None:
                            field_name = app_field.verbose_name.title() if app_field.verbose_name else "Não Definido."
                            thead += f"<th>{field_name}</th>\n"
                            tline += '<td>{{{{ item.{} }}}}</td>\n'.format(item.replace('__', '.'))
                    list_template = Path(
                        f"{self.path_template_dir}/{self.model_lower}_list.html")
                    list_template_content = self.__get_snippet(list_template)
                    list_template_content = list_template_content.replace("<!--REPLACE_THEAD-->", thead)
                    list_template_content = list_template_content.replace("<!--REPLACE_TLINE-->", tline)
                    with open(list_template, 'w', encoding='utf-8') as list_file:
                        list_file.write(list_template_content)

                except Exception as error:
                    Utils.show_message(f"Error in __manage_render_html ao realizar o parser do template : {error}")
        except Exception as error:
            Utils.show_message(f"Error in __manage_render_html : {error}")

    def __verified_options_flag_is_false(self, options):
        __flags = ['templates', 'api', 'url', 'forms', 'views', 'renderhtml']
        result = False
        try:
            for flag in __flags:
                if options[flag] is True:
                    result = True
        finally:
            return result

    def call_methods(self, options):
        if options['templates']:
            Utils.show_message("Trabalhando apenas os templates.")
            self.__manage_templates()
            self.__apply_pep()
            return
        elif options['api']:
            self.__manage_serializer()
            self.__manage_api_view()
            self.__manage_api_url()
            self.__manage_urls_api_app()
            self.__apply_pep()
            return
        elif options['url']:
            Utils.show_message("Trabalhando apenas as urls.")
            self.__manage_url()
            self.__apply_pep()
            return
        elif options['forms']:
            Utils.show_message("Trabalhando apenas os forms.")
            self.__manage_form()
            self.__apply_pep()
            return
        elif options['views']:
            Utils.show_message("Trabalhando apenas as views.")
            self.__manage_views()
            self.__apply_pep()
            return
        elif options['renderhtml']:
            self.__manage_render_html()
            return
        elif options['format']:
            self.__apply_pep()
            return
        else:
            self.__manage_form()
            self.__manage_views()
            self.__manage_serializer()
            self.__manage_url()
            self.__manage_api_view()
            self.__manage_api_url()
            self.__manage_templates()
            self.__manage_render_html()
            self.__apply_pep()

    def handle(self, *args, **options):
        app = options['App'] or None
        if Utils.contain_number(app) is False:
            if app != "usuario" and self.__verified_options_flag_is_false(options) is False:
                Utils.show_message("Apenas a app usuario aceita o comando build sem as flags", error=True)
                return
            Utils.show_message("Gerando os arquivos da app")
            self.app = app.strip()
            self.path_root = os.getcwd()
            self.path_app = Path(f"{self.path_root}/{app}")
            self.path_core = Path(f"{self.BASE_DIR}/core")
            self.path_model = Path(f"{self.path_app}/models.py")
            self.path_form = Path(f"{self.path_app}/forms.py")
            self.path_views = Path(f"{self.path_app}/views.py")
            self.path_api_views = Path(f"{self.path_app}/api_views.py")
            self.path_urls = Path(f"{self.path_app}/urls.py")
            self.path_api_urls = Path(f"{self.path_app}/api_urls.py")
            self.path_serializer = Path(f"{self.path_app}/serializers.py")
            self.path_template_dir = Path(
                f"{self.path_app}/templates/{self.app}")
            self.path_app = Path(f"{self.path_root}/{app}")
            self.app_lower = app.lower()
            if self.__check_dir(self.path_app) is False:
                Utils.show_message("Diretório não encontrado.")
                return
            if apps.is_installed(self.app_lower) is False:
                Utils.show_message("Você deve colocar sua app no INSTALLED_APPS do settings.")
                return
            self.app_instance = apps.get_app_config(self.app_lower)
            if options['Model']:
                model = options['Model'] or None
                if Utils.contain_number(model) is False:
                    self.model = model.strip()
                    if self.__check_content(self.path_model, 'class {}'.format(self.model)) is False:
                        Utils.show_message("Model informado não encontrado.")
                        return
                try:
                    self.app_instance.get_model(self.model)
                    Utils.show_message("Gerando arquivos para o model {}".format(self.model))
                    self.model_lower = model.lower()
                    self.call_methods(options)
                except LookupError as error:
                    Utils.show_message(f"Error in handler : {error}")
            else:
                for model in self.app_instance.get_models():
                    Utils.show_message(f"Gerando os arquivos para a app {self.app} e model {model.__name__.strip()}")
                    model = model.__name__
                    self.model = model.strip()
                    self.model_lower = model.lower()
                    self.call_methods(options)
                Utils.show_message("Processo concluído.")
                return