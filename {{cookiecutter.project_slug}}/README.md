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
   
<br>

## Direitos Autorais

-----

Todos os direitos reservados para a Prefeitura Municipal de Palmas, Tocantins, Brasil.
Desenvolvido pela equipe de analistas da Agência de Tecnologia da Informação da Prefeitura de Palmas.
http://www.palmas.to.gov.br

Powered By

![Python](https://www.python.org/static/img/python-logo.png)
![Django](https://static.djangoproject.com/img/logo-django.42234b631760.svg)
