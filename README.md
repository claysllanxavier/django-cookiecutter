# Projeto Django CookieCutter 

## Pré requisitos

Crie um diretório para o seu projeto

    $ mkdir nome_do_seu_projeto"

Crie e habilite um ambiente python
    $ python -m venv .venv
    $ source .venv\Script\activate

Instale o cookiecutter

    $ pip install "cookiecutter>=1.7.0"

## Uso

Rode o cookiecutter apontando para o repositório do projeto base Django:

    cookiecutter ...

Responda as perguntas sobre seu novo projeto:
> Para todas as perguntas que a opção for main basta apenas aceitar

    project_name [Main]: Apenas clicar no enter para aceitar o valor padrão
    project_slug [main]: Apenas clicar no enter para aceitar o valor padrão
    main_app [main]: Apenas clicar no enter para aceitar o valor padrão
    client_name [Prefeitura de Palmas]: Informe o nome da secretaria/setor que solicitou a demanda
    created_date_project: Apenas aceitar o valor informado, que é a data atual
    description [Projeto base para os novos projetos]: Escolha uma definição para seu projeto
    author_name [Agtec]: Digite seu nome completo, caso contrário o autor do projeto será Agtec
    domain_name [example.com]: minhastarefas.na-inter.net
    email [agtec@palmas.to.gov.br]: Digite seu e-mail institucional

Instale as dependências do projeto (lembre de estar com o virtual env ativado)

    ./manage.py pip-sync requirements.txt requirements-dev.txt

Execute a migração dos projetos

    ./manage.py migrate

Remova do settings, esse valores estão definidos no arquivo .secret.yaml:

    1 - SECRET_KEY
    2 - DATABASES

Rode a aplicação Django

    ./manage.py runserver

Para criar um usuário

    ./manage.py createsuperuser

Para rodar os testes

    pytest