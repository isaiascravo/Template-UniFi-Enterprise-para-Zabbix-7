# Notas de investigação da API UniFi Network `integration/v1`

Resultado de uma validação real contra um UniFi OS Server ao vivo (build com
firmware de switch `7.4.1`, controlador com sites/dispositivos/clientes
reais). Nenhum item aqui é suposição - cada afirmação foi confirmada por uma
chamada HTTP de verdade ou por consulta à documentação oficial do Zabbix.
Nenhum dado privado (IP público, nome de site real, nome de dispositivo,
cliente ou MAC de terceiros) é reproduzido neste documento público.

## Base da API e documentação local

- A base correta da API é `https://<host>:11443/proxy/network/integration/v1`.
- `https://<host>:11443/unifi-api/network` **não é a API** - é a casca de
  uma SPA autenticada do UniFi OS (`<title>UniFi OS</title>`, carrega
  bundles `main~0/main~1/main~2` + chunks numerados). Apontar
  `{$UNIFI.API.URL}` para esse caminho faz os itens HTTP Agent receberem
  HTML em vez de JSON.
- Não existe uma especificação OpenAPI/Swagger exposta localmente:
  `GET /proxy/network/integration/v1/openapi.json`,
  `/swagger.json`, `/api-docs` e `/docs` retornam todos `404`. Os bundles JS
  da SPA (até ~2,5 MB cada) também não contêm as strings `openapi`/`swagger`.
  Os endpoints abaixo foram validados por chamada real, não por spec.

## Endpoints confirmados

| Endpoint | Status | Observações |
|---|---|---|
| `GET /sites` | 200 | `{offset,limit,count,totalCount,data[]}`; `data[]` = `{id,name,internalReference}` |
| `GET /sites/{siteId}/devices` | 200 | Mesmo envelope de paginação; `data[]` traz `id,macAddress,ipAddress,name,model,state,supported,firmwareVersion,firmwareUpdatable,features[],interfaces[]` |
| `GET /sites/{siteId}/devices/{deviceId}` | 200 | Detalhe completo; switches trazem `interfaces.ports[]` (`idx,state,connector,speedMbps,maxSpeedMbps`), APs trazem `interfaces.radios[]` (`wlanStandard,frequencyGHz,channelWidthMHz,channel`) |
| `GET /sites/{siteId}/devices/{deviceId}/statistics/latest` | 200 | `uptimeSec,lastHeartbeatAt,nextHeartbeatAt,loadAverage{1,5,15}Min,cpuUtilizationPct,memoryUtilizationPct,uplink.{txRateBps,rxRateBps}`; para APs também `interfaces.radios[].txRetriesPct` |
| `GET /sites/{siteId}/clients` | 200 | Mesmo envelope de paginação; `data[]` = `{type(WIRED/WIRELESS),id,name,connectedAt,ipAddress,macAddress,uplinkDeviceId,access.type}` |
| `GET /sites/{siteId}/devices/{deviceId}/ports` | 404 | Não existe; o estado das portas vem embutido no objeto de dispositivo acima |
| `GET /sites/{siteId}/devices/{deviceId}/radios` | 404 | Idem, embutido no objeto de dispositivo |

Erros confirmados:

- Chave inválida: `401` `{"error":{"code":401,"message":"Unauthorized"}}`
- Site/recurso inexistente: `404` `{"statusCode":404,"statusName":"NOT_FOUND","code":"api.resource-not-found",...}`

Paginação: `offset`/`limit`/`count`/`totalCount`/`data[]` - `limit=200` não
garante que a resposta traga tudo; o cliente deve avançar `offset` pelo
`count` retornado até `len(acumulado) >= totalCount`.

## O que a API confirmadamente NÃO expõe

Testado e confirmado ausente, não apenas "não implementado":

- Contadores de porta (RX/TX bytes/pacotes, erros, descartes), PoE
  (habilitado/consumo/potência), duplex, STP, e nenhuma flag indicando qual
  porta é o uplink.
- Temperatura de dispositivo.
- Potência de rádio, utilização de canal, interferência, "satisfaction"/
  experiência - só `txRetriesPct` está disponível por rádio.
- SSID, VLAN, banda, flag de convidado/VPN por cliente - o objeto de
  cliente só tem os campos listados na tabela acima.
- Qualquer campo de gateway/WAN/VPN - nenhum gateway UniFi (USG/UDM) estava
  adotado no ambiente usado para validar isto; nada foi implementado sem um
  dispositivo real para confirmar contra.

## Pegadinhas de template Zabbix descobertas nesta investigação

- O tipo de macro secreta no YAML/XML de exportação do Zabbix é
  **`SECRET_TEXT`**, não `SECRET` (confirmado na documentação oficial do
  Zabbix 7).
- Os campos de item HTTP Agent `verify_peer`/`verify_host` ("SSL verify
  peer"/"SSL verify host") são checkboxes fixos (`YES`/`NO`) e **não**
  aceitam macro de usuário - só campos documentados como aceitando "user
  macros" na documentação do Zabbix suportam isso. Um template que tenta
  `verify_peer: '{$ALGUMA.MACRO}'` não terá o comportamento dinâmico
  esperado; o correto é fixar o valor e, se for necessário alternar entre
  verificar e não verificar TLS, manter duas variantes do item/template ou
  documentar a edição manual pós-importação.
