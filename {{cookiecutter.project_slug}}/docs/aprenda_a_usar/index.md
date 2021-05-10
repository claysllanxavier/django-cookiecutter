# Projeto Django 

Esse projeto foi criado utilizando o Django Cookiecutter que gera um projeto Django com as configurações padrões de 
um projeto Django, com Django Rest Framework e com managers que auxiliarão no desenvolvimento do seu projeto. 

> Lembre-se de sempre consultar a documentação quando surgir alguma dúvida.

Abaixo temos as etapas a serem executadas quando o projeto for criado.

### Ativar o virtualenv

    $ source venv\Script\activate | windows
    $  . venv/bin/activate | linux e macOs

### Comandos a serem executados após a criação do projeto

1. Gerar a secret_key do projeto Django
   > import secrets  
   > print(secrets.token_urlsafe())   
   > **Caso necessário é possível informar a quantidade caracteres na chamada do** ***secrets.token_urlsafe(n)*** 
1. Acessar o subdiretório do projeto que foi criado após o comando *cookiecutter ..\django-cookiecutter* 
1. Instale as dependências  
    ```pip-sync requirements.txt requirements-dev.txt``` 
1. Execute o comando de criação das migrações  
    ```python manage.py makemigrations```
1. Execute o comando de aplicação das migrações    
    ```python manage.py migrate```
1. Crie os códigos boilerplates da app usuario  
    ```python manage.py build usuario```   
1. Crie o super user padrão do projeto  
    ```python mock_superuser.py```
1. Crie usuários de exemplo da app usuário  
    ```python mock_data.py```

-----

Esse projeto já traz por padrão a app de Usuario/usuario. Ao executar o comando migrate já foi adicionado no banco 
de dados as tabelas relativas a essa app, agora é necessário executar o comando abaixo para que os arquivos 
boilerplates da app/model sejam criados.

Com o comando de criação do superusuário temos um usuário do tipo super user com os dados abaixo.  

    login: admin  
    senha: asdf@1234  
    DRF Token: 2b817ddbb5b974e5a451a8156963de586d72079e