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
SECRET_KEY=NYPmGeU11uQ96YQtX9UjOZ_EuAGsuJltGJt5XBrXt0HQhgShCP7KIWlLFgxtZDhl0z4
DEBUG=True
ALLOWED_HOSTS=.localhost,
API_PATH=http://localhost:8080/api/
SENTRY_DNS=q0y#b#k6@23f=g8ts-x^j55mqcskn3@-_ct&z4(8zp32-z77oq
DB_NAME=nome_do_banco_de_dados
DB_USER=usuario_do_banco_de_dados
DB_PASSWORD=senha_do_banco_de_dados
DB_HOST=endereco_do_servidor_do_banco_de_dados
```

## Links
|Pip |Docs  |
--- | --- |
|[Pip](https://pypi.org/project/python-decouple/)|[Doc](https://github.com/henriquebastos/python-decouple)|
