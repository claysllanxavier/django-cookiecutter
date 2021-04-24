# Novas app do seu projeto

Após a configuração inicial do projeto quando forem criadas novas apps django no projeto, os seguintes passos devem 
ser seguidos para que os managers funcionem de forma correta.

### Observação
Não deve ser executado o comando **python manage.py build nome_da_app**, esse comando só deve ser executado dessa 
forma logo após a criação inicial do projeto, aonde temos apenas a app usuario.

### Etapas

1. Criar a nova app com o comando **python manage.py startapp nome_da_app**
1. Adicionar a app no **INSTALLED_APPS[...]* do aquivo *settings.py**
1. Criar os models com seus respectivos atributos  
    1. Adicionar no class Meta do models os campos que deseja que sejam renderizado no list_view **fields_display = 
   ['campo_um', 'campo_n']**
1. Executar os comandos **python manage.py makemigrations** e **python manage.py migrate**     
1. Executar o comando **python manage.py build nome_da_app** com as flags na ordem a seguir:
    1. **python manage.py build nome_da_app --forms** *serão geradas as forms dos models da app informada*
    1. **python manage.py build nome_da_app --views** *serão geradas as views dos models da app informada*
    1. **python manage.py build nome_da_app --urls** *serão geradas as urls dos models da app informada*
    1. ***Agora adicione no arquivos urls.py do projeto (base) o path para as urls da app***
    1. ***Acesse o arquivo urls.py da app informada e comente a linha do path da api***  
           path('api/xpto/', include('xpto.api_urls')),
    1. **python manage.py build nome_da_app --templates** *serão geradas os templates html dos models da app 
   informada*
    1. **python manage.py build nome_da_app --parserhtml** *serão realizados os parser dos templates HTML contendo os 
   atributos dos models da app informada*    
    1. **python manage.py build nome_da_app --api** *serão gerados os arquivos da APIRest dos models da app informada*
    1. ***descomente a linha da da etapa 5.e***