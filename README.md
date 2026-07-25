# Template UniFi Enterprise para Zabbix 7

Template comunitário para monitoramento de ambientes UniFi Network pelo Zabbix 7 usando a API oficial local (`integration/v1`) e autenticação por API key.

> Status: **alpha**. Os endpoints e campos abaixo foram validados com chamadas reais contra um UniFi OS Server ao vivo (ver `docs/API-NOTES.md`) - nada aqui é suposição. A cobertura de itens/LLD ainda é mínima; ver `docs/ROADMAP.md`.

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
4. Configure as macros no host (não no template, para não versionar a chave):
   - `{$UNIFI.API.URL}`: base da API, exemplo `https://192.168.0.241:11443/proxy/network/integration/v1`
     (**não** aponte para `/unifi-api/network` - esse caminho é a página de
     documentação autenticada, uma SPA que devolve HTML, não a API)
   - `{$UNIFI.API.KEY}`: chave de leitura criada no UniFi OS (o macro já é do tipo `Secret text`)
   - `{$UNIFI.API.TIMEOUT}`: timeout em segundos (padrão `10`)

## Endpoints validados

Validados com chamadas reais (não apenas lidos de uma especificação - ver `docs/API-NOTES.md` para o porquê):

- `GET /sites`
- `GET /sites/{siteId}/devices`
- `GET /sites/{siteId}/devices/{deviceId}`
- `GET /sites/{siteId}/devices/{deviceId}/statistics/latest`
- `GET /sites/{siteId}/clients`

Apenas `/sites` está implementado no template nesta fase (`unifi.api.sites.raw` +
`unifi.api.sites.count` como item dependente, demonstrando o padrão de
"uma chamada por payload"); os demais entram nas próximas fases do roadmap.

## Segurança

Nunca versione API keys nem respostas que contenham dados pessoais, MACs, IPs públicos ou nomes reais de clientes. Consulte `SECURITY.md`.

## Roadmap

Consulte `docs/ROADMAP.md` e a issue #1.

## Limitações conhecidas da API

Ver `docs/API-NOTES.md` para a lista completa. Resumo: não há especificação
OpenAPI/Swagger local exposta pelo UniFi OS Server testado; a API não expõe
contadores de porta, PoE, duplex, STP, potência/interferência de rádio, ou
atributos de SSID/VLAN/banda por cliente. Gateway/WAN/VPN não foram
validados por falta de um dispositivo desse tipo no ambiente de teste.

## Licença

MIT.
