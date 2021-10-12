# Python Decouple

## Sobre

Lib para aplicar dentre outras funcionalidades a separação de dados sensíveis da aplicação do arquivo settings e colocar em variáveis de ambiente

## Arquivo .env
No ambiente de desenvolvimento deve-se utilizar esse arquivo para conter as configurações do projeto. Como exemplo 
temos a configuração da variáveis SECRET_KEY e do DATABASE.

### Gerando uma nova chave SECRET_KEY para o projeto gerado

```python
from django.core.management import utils
print(utils.get_random_secret_key())
```

### O arquivo .env deve ser adicionado no arquivo .gitignore para evitar de ser enviado ao servidor de versionamento  

  
```
DEBUG=True
# O campo SECRET_KEY deve receber o valor gerado pelo comando do django utils.get_random_secret_key() 
SECRET_KEY=
ALLOWED_HOSTS=.localhost,
# O campo API_PATH deve receber o caminho da APIRest
API_PATH=
# O campo SENTRY_DNS deve receber o valor do DNS do Sentry para capturar os erros 
SENTRY_DNS=
# O campo DB_NAME deve receber o nome do banco de dados PostgreSQL
DB_NAME=
# O campo DB_USER deve receber o nome do usuário para autenticar no servidor PostgreSQL
DB_USER=
# O campo DB_PASSWORD deve receber a senha de acesso do usuário para autenticar no servidor PostgreSQL
DB_PASSWORD=
# O campos DB_HOST deve receber o IP do servidor PostgreSQL
DB_HOST=
```

## Links
|Pip |Docs  |
--- | --- |
|[Pip](https://pypi.org/project/python-decouple/)|[Doc](https://github.com/henriquebastos/python-decouple)|
