# OpenAPI e coleção Postman

A controladora testada não expôs `openapi.json` nos caminhos locais tentados. Isso não significa que a especificação oficial inexista.

A Ubiquiti disponibiliza no Developer Portal:

- documentação versionada do UniFi Network;
- especificação OpenAPI;
- coleção Postman;
- exemplos em diferentes linguagens.

## Política do projeto

1. Registrar a versão da documentação usada.
2. Não copiar API keys ou respostas privadas para o repositório.
3. Manter fixtures sanitizadas derivadas do schema e de respostas reais.
4. Comparar versões antes de adicionar campos opcionais.
5. Abrir issue quando um campo desaparecer ou mudar de tipo.

O projeto não deve baixar automaticamente contratos externos durante a execução do template. Contratos usados em CI devem ser revisados e versionados de forma controlada.
