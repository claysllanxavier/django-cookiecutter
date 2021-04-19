# Projeto Django CookieCutter 

## Pré requisitos

Crie um diretório para o seu projeto

    $ mkdir nome_do_seu_projeto"

Crie e habilite um ambiente python
    
    $ python -m venv .venv
    $ source .venv\Script\activate

Instale o cookiecutter

    $ pip install "cookiecutter>=1.7.0"

Instale o pip-tools

    $ pip install pip-tools

## Uso

Rode o cookiecutter apontando para o repositório do projeto base Django:

    cookiecutter ...

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

Instale as dependências do projeto (lembre de estar com o virtual env ativado)

    pip-sync requirements.txt requirements-dev.txt

Crie as migrações do seu projeto

    ./manage.py makemigrations

Execute a migração dos projetos

    ./manage.py migrate

Rode a aplicação Django

    ./manage.py runserver

Para criar um usuário

    ./manage.py createsuperuser

Para rodar os testes

    pytest