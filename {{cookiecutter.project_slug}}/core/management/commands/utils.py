import logging
import os
import sys

from django.contrib.contenttypes.models import ContentType


class Utils(object):
    @staticmethod
    def show_message(text: str, error: bool = False):
        """ Método para mostrar uma mensagem no console do python com mensagem de erro ou não

        Arguments:
            message {str} -- String contendo a mensagem que será mostrada no console
            error {bool} -- Booleano para determinar se a mensagem é de erro ou não. Sendo mensagem de erro o processo 
                            é finalizado com o comando sys.exit()
        """
        __log = logging.getLogger('logger')
        __log.setLevel(logging.INFO)
        try:
            if error:
                print("#"*100)
                print("*"*100)
                print(f"ERRO: {text}\n\nPor favor consulte a documentação.\nBasta "
                      f"executar o comando:\nmkdoks serve -a 127.0.0.1:8080")
                print("*"*100)
                print("#"*100)
                __log.error(f"\n{'!=' * len(text)}\nERROR: {text.upper()}\n")
                sys.exit()
            else:
                print(text)
                __log.warning(text)
        except Exception as error:
            logging.error(error)

    @staticmethod
    def contain_number(text: str) -> bool:
        try:
            return any(character.isdigit() for character in text)
        except Exception as error:
            Utils.show_message(f"Error in __contain_number: {error}", error=True)
            return False

    @staticmethod
    def get_verbose_name(apps, app_name: str = None, model_name: str = None) -> str:
        try:
            if app_name is not None and model_name is not None:
                _model = ContentType.objects.get(
                    app_label=app_name.lower(), model=model_name.lower())
                return _model.model_class()._meta.verbose_name.title()
            if app_name is not None and model_name is None:
                __app_config = apps.get_app_config(app_name.lower())
                return __app_config.verbose_name.title() or app_name
        except Exception as error:
            if str(error).find("ContentType matching query does not exist") == -1:
                Utils.show_message(f"Error in Utils.get_verbose_name: {error}")
            return model_name.title() or app_name.title()

    @staticmethod
    def check_dir(path: str) -> bool:
        """Método para verificar se o diretório passado como parâmetro existe

        Arguments:
            path {str} -- Caminho do diretório

        Returns:
            bool -- True se o diretório existir e False caso contrário.
        """
        __process_result = False
        try:
            __process_result = os.path.isdir(path)
        except Exception as error:
            Utils.show_message(f"Error in Utils.check_dir: {error}", error=True)
        finally:
            return __process_result

    @staticmethod
    def check_file(path: str) -> bool:
        """Método para verificar se o arquivo existe no caminho passado como parâmetro

         Arguments:
             path {str} - Caminho do arquivo

         Returns:
             bool - True se o arquivo existir e False caso contrário
        """
        __process_result = False
        try:
            __process_result = os.path.isfile(path)
        except Exception as error:
            Utils.show_message(f"Error in Utils.check_file: {error}", error=True)
        finally:
            return __process_result

    @staticmethod
    def check_content(path: str, text: str) -> bool:
        """Método para verificar se o conteúdo do parâmetro 

         Arguments:
             path {str} - Caminho do arquivo
             text {str} - Texto para ser verificado se existe no conteúdo do arquivo passado no path

         Returns:
             bool - True se o conteúdo existir no arquivo e False caso contrário
        """
        __process_result = False
        try:
            if Utils.check_file(path):
                with open(path) as content_file:
                    content = content_file.read()
                    __process_result = text in content
        except Exception as error:
            Utils.show_message(f"Error in Utils.check_content: {error}", error=True)
        finally:
            return __process_result

    @staticmethod
    def check_file_is_locked(path: str) -> bool:
        """ Método para verificar se no arquivo passado como parâmetro existe a palavra FileLocked
            caso existe o processo de parser do arquivo não será executado

         Arguments:
             path {str} - Caminho para o arquivo a ser analizado

         Returns:
             bool - True se a palavra existir e False caso contrário
        """
        __process_result = False
        try:
            if Utils.check_file(path):
                with open(path, encoding='utf-8') as file:
                    content = file.read()
                    __process_result = "#FileLocked" in content
        except Exception as error:
            Utils.show_message(f"Error in Utils.check_file: {error}", error=True)
        finally:
            return __process_result

    @staticmethod
    def get_snippet(path: str) -> str:
        """Método para retornar o conteúdo do arquivo a ser utilizado como modelos para gerar o 
           arquivo baseado no models, gerando os arquivos de templates, views, urls, serializers, 
           forms e também os arquivos do projeto Flutter.

        Arguments:
            path {str} - Caminho para o arquivo que serve como base para criar os arquivos do projeto

        Returns:
            str -- Texto do snippet para ser parseado e depois gerar o arquivo do projeto Django/Flutter
        """
        __content = ""
        try:
            if Utils.check_file(path):
                with open(path, 'r', encoding='utf-8') as file:
                    __content = file.read()
        except Exception as error:
            Utils.show_message(f"Error in Utils.check_file: {error}", error=True)
        finally:
            return __content