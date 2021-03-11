# Projeto {{ cookiecutter.project_name }}
    {{ cookiecutter.description }}

## Cliente
> {{ cookiecutter.client_name}}

## Dados do Projeto
> **Data da Criação** : {{ cookiecutter.created_date_project }} 
<br> **Django Version** : {{ cookiecutter.django_version }}
<br> **Python Version**: {{ cookiecutter.python_version }}
<br> **PostgreSQL Version** : {{ cookiecutter.postgresql_version }}

## Analista Responsável
> {{ cookiecutter.author_name }}  
{{ cookiecutter.email }}
 

## Etapas para configuração do projeto 
### Lembre-se de ativar o virtualenv

1. Execute o comando   
   > **pip-compile requirements.in**
1. Execute o comando  
   > **pip-compile requirements-dev.in**
1. Execute o comando 
   > **pip-sync requirements.txt requirements-dev.txt**   
   > O requirements-dev.txt só deve ser utilizado em ambiente de desenvolvimento
   

## Managers

      Esse projeto conta com alguns managers customizados que facilitam o desenvolvimento do sistema. 
      Abaixo descreveremos cada um dos managers e seus respectivos comandos e funcionalidades.

### Manager build

#### Executar
> python manage.py build

      Esse manager é responsável por gerar os códigos boilerplates baseados nas classes de cada app.

      Esse manager necessita que sejam passados alguns parâmetros para sua execução.

      Parâmetros:

         1. App [Obrigatório] - Nome da app que deverá ser renderizada pelo manager. 
         2. Model [Opcional] - Nome do model que deverá ser renderizado pelo manager.
            (Caso não seja passada o sistema renderizará todos os models da App)
         3. templates [Opcional] - Caso seja passado apenas os arquivos de template HTML.
            3.1 Para que o template de listagem renderize os campos corretamente, devem ser
                setados quais atributos serão mostrados no parâmetro fields_display do class Meta do models
            3.2 Para os models que possuem campos relacionais do tipo ForeignKey e você deseje que seja criado o 
                modal com um formulário para inserção de dados você deve configurar o atributo fk_fields_modal
                também no class Meta do seu models.
            
            Exemplo:
            
            class Exemplo(Base):
                ...
                class Meta:
                    fields_display = ["atributo_um", "atributo_dois"', "atributo_n"]
                    fk_fields_modal = ["foreignkey_um", "foreignkey_dois", "foreignkey_n"]

         4. url [Opcional] - Deve ser executado para criar as urls.
         5. forms [Opcional] - Deve ser executado para criar os forms .
         6. views [Opcional] - Deve ser executado para criar as ClassBaseView`s.
         7. renderhtml [Opcional] - Deve ser executado para renderizar os formulários no templates HTML.
         8. format [Opcional] - Dever ser executado para formatar o código utilizando a PEP 8.
         9. api [Opcional] - Deve ser executado para gerar todo o código (CRUD) boilerplate da APIRest.


### Manager Flutter
      Esse manager é responsável por gerar o projeto flutter baseado nas apps/models do projeto Django.

      Esse manager deve ser utilizado para:
         1. Criar um projeto flutter.
         2. Instalar as dependências do projeto flutter.
         3. Realizar o parser dos models do projeto Django para as respectivas classes no flutter.
         4. Criar toda a estrutura de páginas navegação das ações abaixo:
            4.1 Listagem.
            4.2 Criação.
            4.3 Detalhamento.
            4.4 Edição.
            4.5 Exclusão.
         5. Criar os serviços responsáveis pela comunicação do aplicativo com a APIRest do projeto Django.
         6. Criar as classes de persistência de dados locais.
         7. Criar as classes de gerenciamento de estado da aplicação
         8. Criar os Widgets padrões a serem utilizados no aplicativo
         9. Criar as classes auxiliares de messageria, log e notificações.

      Para que ele funcione corretamente é necessário configurar a variável FLUTTER_APPS = [] no arquivo settings.py do 
      projeto com as apps do projeto Django que deverão ser mapeadas.

      Exemplo:
         FLUTTER_APPS = ['app_um', 'app_dois', 'app_n']

      Também deve ser configurada a variável API_PATH com o caminho da APIRest.

      Exemplo:
         API_PATH = "https://dominio.com.br/core/api

#### Executar
> python manage.py flutter --init-cubit

Atualizar o arquivo de dependências
> python manage.py flutter --yaml

Para gerar os arquivos flutter de uma determinada App/Model
> python manage.py flutter --model NomeDaApp nome_do_model

Para atualizar o arquivo main.dart com todas as apps do projeto
> python manage.py flutter --main


### Qualidade do Código / TDD
      Com o objetivo de manter a qualidade do código e uma certa padronização, foram instalados por padrão nesse 
      projetos algumas libs que nos auxiliarão nessa tarefa

      1. flake8 [https://gitlab.com/pycqa/flake8]
         Utilizada para verificar se os código estão em conformidade com a PEP8
         
         1.1 Para executar basta chamar no terminal flake8

      2. Pytest [https://docs.pytest.org/en/latest/]
         Para realizar testes unitários no projeto
         
         Todas as apps do projeto devem conter um subdiretório chamado tests, aonde serão implementados 
         os testes das funcionalidades do app
         
         2.1 Para executar basta abrir o arquivo de testes e mandar executar clicando na seta verde
             no canto superior direito do PyCharm

      3. ScanAPI [https://scanapi.dev/docs.html]
         Para realizar testes nos endpoints da APIRest
         
         No mesmo diretório de tests devem ser criados quantos arquivos forem necessário para testar todos
         os endpoints da referida App. O arquivo de test segue o padrão YAML, vide arquivo de exemplo scanapi_exemplo.yaml.

         3.1 Para executar basta chamar o comando no terminal

               scanapi run PATH_COMPLETO_PARA_O_ARQUIVO_DE_TESTE.yaml      
         
         Após a conclusão do teste será gerado um arquivo scanapi-report.html na raiz do projeto aonde poderá ser 
         verificado o resultado dos testes.

## Licença
[here](LICENSE)

## Direitos Autorais

-----

Todos os direitos reservados para a Prefeitura Municipal de Palmas, Tocantins, Brasil.
Desenvolvido pela equipe de analistas da Agência de Tecnologia da Informação da Prefeitura de Palmas.
http://www.palmas.to.gov.br

Powered By

![Python](https://www.python.org/static/img/python-logo.png)
![Django](https://static.djangoproject.com/img/logo-django.42234b631760.svg)
