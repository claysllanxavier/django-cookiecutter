# Pytest

## Sobre

Framework para realizar testes unitários compreendendo testes de:  

1 - models.py  
2 - forms.py  
3 - views.py
  
Na raiz do projeto existe o arquivo ```pytest.ini``` contendo a configuração necessário para que o framework identifique os testes no projeto Django.  

Para ser consderado válido um commit nos projeto a cobertura de testes deve ser igual ou maior que 90%

## Executar
```python
pytest
```

## Relatório de cobertura dos testes

    ----------- coverage: platform win32, python 3.8.6-final-0 -----------
    Name                                             Stmts   Miss  Cover
    --------------------------------------------------------------------
    __init__.py                                          0      0   100%
    usuario\__init__.py                                  1      0   100%
    usuario\admin.py                                     1      0   100%
    usuario\apps.py                                      4      0   100%
    usuario\models.py                                   43     14    67%
    usuario\tests\__init__.py                            0      0   100%
    usuario\tests\tests.py                              13      0   100%
    --------------------------------------------------------------------
    TOTAL                                               80     14    82%

    FAIL Required test coverage of 90% not reached. Total coverage: 82.50%

## Arquivo de configuração
A linha ```addopts = --cov --cov-fail-under=90``` especifica o percentual mínimo de cobertura aceito para que o projeto passe no processo de CI
```toml
[pytest]
DJANGO_SETTINGS_MODULE = base.settings
python_files = tests.py test_*.py *_tests.py
addopts = --cov --cov-fail-under=90
```

## Links
|Pip |Docs  |
--- | --- |
|[Pip](https://pypi.org/project/pytest/)|[Doc](https://docs.pytest.org/en/latest/)|


