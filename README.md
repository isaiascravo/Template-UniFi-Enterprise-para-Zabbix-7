# Template UniFi Enterprise para Zabbix 7

Template comunitário para monitoramento de ambientes UniFi Network pelo Zabbix 7 usando a API oficial local e autenticação por API key.

> Status: **alpha**. A estrutura e os itens-base estão prontos; os JSONPath e protótipos avançados serão validados contra respostas sanitizadas de uma controladora UniFi Network 10.4.57.

## Objetivos

- API oficial, sem sessão, cookies ou scraping;
- coleta centralizada por HTTP Agent;
- itens dependentes para reduzir chamadas;
- descoberta de sites e dispositivos;
- evolução para switches, portas, PoE, APs, rádios, clientes e auditoria;
- compatibilidade principal com Zabbix 7.0 LTS.

## Instalação inicial

1. Importe `templates/unifi_network_controller.yaml`.
2. Crie um host para a controladora UniFi.
3. Vincule o template `UniFi Network Controller by Official API`.
4. Configure as macros:
   - `{$UNIFI.API.URL}`: exemplo `https://192.168.0.241:11443/unifi-api/network`
   - `{$UNIFI.API.KEY}`: chave criada no UniFi OS
   - `{$UNIFI.API.TLS_VERIFY}`: `1` para validar o certificado ou `0` em laboratório

## Endpoints da primeira fase

- `GET /v1/info`
- `GET /v1/sites`

## Segurança

Nunca versione API keys nem respostas que contenham dados pessoais, MACs, IPs públicos ou nomes reais de clientes. Consulte `SECURITY.md`.

## Roadmap

Consulte `docs/ROADMAP.md` e a issue #1.

## Licença

MIT.
