# Dynaconf

## Sobre

Lib para aplicar dentre outras funcionalidades a separação de dados sensíveis da aplicação do arquivo settings e colocar em variáveis de ambiente

## Settings

```python
# Importando a lib logo no começo do arquivo settings.py
import dynaconf
... 

# Adicionando na última linha do arquivo settings.py a configuração do dynaconf
# Após a declaração dessa linha não pode haver nenhum outro código
settings = dynaconf.DjangoDynaconf(__name__) 
```

## Arquivo .secrets.yaml
No ambiente de desenvolvimento deve-se utilizar esse arquivo para conter as configurações do projeto. Como exemplo 
temos a configuração da variáveis SECRET_KEY e do DATABASE
```python
default:
  SECRET_KEY: 'o#z)k&$3pdfhe+7)+*ge+9_1gsf_^(^dztn4&8&u#8p_8p20oa'
  DATABASES:
    default:
      ENGINE: "django.db.backends.sqlite3"
      NAME: "db.sqlite3"
```
Nesse arquivo podem ser criadas outras variáveis como por exemplo chaves de serviços de terceiros. No caso de ser criado alguma chave que não seja padrão do Django antes de utilizar é necessário fazer o import.

### Exemplo
```python
default:
  SECRET_KEY: 'o#z)k&$3pdfhe+7)+*ge+9_1gsf_^(^dztn4&8&u#8p_8p20oa'
  DATABASES:
    default:
      ENGINE: "django.db.backends.sqlite3"
      NAME: "db.sqlite3"
  MINHA_CHAVE: Xpto
```

Para utilizar a MINHA_CHAVE
```python
from django.conf import settings
minha_chave = settings.MINHA_CHAVE
```


## Links
|Pip |Docs  |
--- | --- |
|[Pip](https://pypi.org/project/dynaconf/)|[Doc](https://www.dynaconf.com/)|
