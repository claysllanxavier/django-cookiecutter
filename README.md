# Projeto Django CookieCutter 

## Pré requisitos

Faça o clone desse projeto para o diretório

    $ git clone https://github.com/AgtecPalmas/django_cookiecutter.git

Crie um diretório para o seu projeto

    $ mkdir "nome_do_seu_projeto"

Acesse o diretório criado na etapa anterior

    $ cd "nome_do_seu_projeto" 

Crie e habilite um ambiente python
    
    $ python -m venv venv
    $ source venv\Script\activate | windows
    $  . venv/bin/activate | linux e macOs

Instale o cookiecutter

    $ pip install cookiecutter==1.7.0

Instale o pip-tools

    $ pip install pip-tools

## Uso

Rode o cookiecutter apontando para o diretório do projeto django_cookiecutter:

    $ cookiecutter ../django_cookiecutter

Responda as perguntas sobre seu novo projeto:
> Para todas as perguntas que a opção for main basta apenas aceitar
> 
> Caso nas etapas das questões de tem o valor main for informado um valor diferente o sistema quebrará 

    project_name [Base]: Apenas clicar no enter para aceitar o valor padrão
    project_slug [base]: Apenas clicar no enter para aceitar o valor padrão
    main_app [base]: Apenas clicar no enter para aceitar o valor padrão
    client_name [Nome do Cliente]: Informe o nome da secretaria/setor que solicitou a demanda
    created_date_project: Apenas aceitar o valor informado, que é a data atual
    description [Projeto base para os novos projetos]: Escolha uma definição para seu projeto
    author_name [Informe seu nome]: Digite seu nome completo, caso contrário o autor do projeto será Agtec
    domain_name [informeseudominio.com.br]: Digite o domínio 
    email [informe@seu.email]: Digite seu e-mail institucional

Acesse o subdiretório criado pelo cookie cutter que contém o projeto Django

    $ cd nome_do_seu_projeto

Instale as dependências do projeto (lembre de estar com o virtual env ativado)

    $ pip-sync requirements.txt requirements-dev.txt

Crie as migrações do seu projeto

    $ python manage.py makemigrations

Execute a migração dos projetos

    $ python manage.py migrate

Esse projeto já traz por padrão a app de Usuario/usuario. Ao executar o comando migrate já foi adicionado no banco 
de dados as tabelas relativas a essa app, agora é necessário executar o comando abaixo para que os arquivos 
boilerplates da app/model sejam criados.

    $ python manage.py build usuario

Para criar um usuário padrão para desenvolvimento.

    $ python mock_superuser.py

Para criar dados mocados na app de usuário execute o comando abaixo

    $ python mock_data.py

Rode a aplicação Django

    $ python manage.py runserver

Com o comando acima será criado um superusuário padrão para ser utilizado no desenvolvimento.  
Dados do usuário criado:

    login: admin  
    senha: asdf@1234  
    DRF Token: 2b817ddbb5b974e5a451a8156963de586d72079e

Para rodar os testes

    pytest

### Documentação do Projeto

Para consultar a documentação do projeto basta no seu projeto com o virtual env ativo executar:

    $ mkdocs serve