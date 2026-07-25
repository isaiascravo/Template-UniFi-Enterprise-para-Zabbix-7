# Template UniFi Enterprise para Zabbix 7

Template comunitário para monitoramento de ambientes UniFi Network pelo Zabbix 7 usando a API oficial local (`integration/v1`) e autenticação por API key.

> Status: **alpha**. A cobertura atual foi validada contra uma controladora UniFi Network 10.4.57 e comparada com a documentação oficial versionada. Campos podem variar entre versões; consulte `docs/API-NOTES.md` e `docs/VERSION_MATRIX.md`.

## Objetivos

- API oficial, sem sessão, cookies ou scraping;
- coleta centralizada por HTTP Agent;
- itens dependentes para reduzir chamadas;
- descoberta de sites, dispositivos, portas e rádios;
- monitoramento do estado/capacidade PoE documentado por porta;
- evolução para clientes, topologia, LAG, dashboards e auditoria quando suportada;
- compatibilidade principal com Zabbix 7.0 LTS.

## Instalação inicial

1. Importe `templates/unifi_network_controller.yaml`.
2. Crie um host para a controladora UniFi.
3. Vincule o template `UniFi Network Controller by Official API`.
4. Configure as macros no host:
   - `{$UNIFI.API.URL}`: exemplo `https://192.168.0.241:11443/proxy/network/integration/v1`;
   - `{$UNIFI.API.KEY}`: chave de leitura criada no UniFi OS;
   - `{$UNIFI.API.TIMEOUT}`: intervalo Zabbix de timeout, padrão `10s`.

Não use `/unifi-api/network` como base: esse caminho é a interface de documentação autenticada e pode retornar HTML.

## Endpoints validados

- `GET /info` - confirmado ao vivo, retorna `{"applicationVersion": "10.4.57"}`
- `GET /sites`
- `GET /sites/{siteId}/devices`
- `GET /sites/{siteId}/devices/{deviceId}`
- `GET /sites/{siteId}/devices/{deviceId}/statistics/latest`
- `GET /sites/{siteId}/clients`

`/info` e `/sites` estão implementados no template nesta fase (cada um com
item mestre + item dependente). Os demais entram conforme o roadmap e os
testes por fixture.

## PoE

O schema oficial documenta `interfaces.ports[].poe` com informações como habilitação, padrão, estado e tipo. Não foram encontrados no schema analisado consumo instantâneo em watts, tensão, corrente ou orçamento PoE do switch. Esses campos não serão prometidos sem evidência oficial ou resposta real sanitizada.

## OpenAPI e Postman

Não foi encontrada uma especificação OpenAPI servida diretamente pela controladora nos caminhos locais testados. A Ubiquiti, porém, disponibiliza especificação OpenAPI e coleção Postman no Developer Portal oficial, versionadas por versão do UniFi Network.

## Segurança

Nunca versione API keys nem respostas que contenham dados pessoais, MACs, IPs públicos ou nomes reais de clientes. Consulte `SECURITY.md`.

## Roadmap

Consulte `docs/ROADMAP.md` e a issue #1.

## Licença

MIT.
