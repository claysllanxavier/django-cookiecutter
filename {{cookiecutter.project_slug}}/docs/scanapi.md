# ScanApi

## Sobre

App responsável por realizar os testes de integração dos endpoints da APIRest  

## Executar
```python
scanapi run app/tests/test_xpto_scanapi.yaml
```
## Relatório de cobertura dos testes
Ao executar o comando acima será gerado um arquivo **scanapi-report.html** na raiz do projeto contendo o resultado dos testes

## Arquivo de configuração padrão
```yaml
endpoints:
  - name: Servico # Nome da App/Model que está sendo testada nesse arquivo
    path: http://127.0.0.1:8000/core/api/ # Caminho Raiz da API
    requests:
      - name: Nome da Requisição # Criando o Primeiro Request
        path: usuario/usuario/ # Informando qual o caminho do endpoint, esse será concatenado com o path anterior
        method: get #Informando qual o verbo HTTP que está sendo testado
        headers: # Configurando o head da requisição
          Accept: application/json
          Contenty-Type: application/json
        tests: # Area para os testes
          - name: status_code # Nome do Teste nesse exemplo testando se o status_code é 200
            assert: ${{ response.status_code == 200 }}
          - name: count # Nome do Teste nesse exemplo testando a quantidade de itens retornados
            assert: ${{ response.json()["count"] == 40 }}
      - name: Detalhamento de um usuario # Criando um segundo request
        path: usuario/usuario/f91b3f57-8ebb-4100-b7ba-bcbea37573e4/ # Informando qual o caminho do endpoint, esse será concatenado com o path anterior
        tests: # Area para os testes
          - name: status_code # Nome do Teste
            assert: ${{ response.status_code == 200 }}
          - name: count
            assert: ${{ response.json()["cpf"] == "36150411192" }}
```

## Links
|Pip |Docs  |
--- | --- |
|[Pip](https://pypi.org/project/scanapi/)|[Doc](https://scanapi.dev/docs.html)|


