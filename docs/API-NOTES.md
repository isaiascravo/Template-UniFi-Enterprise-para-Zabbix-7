# Notas de investigação da API UniFi Network `integration/v1`

Resultado de validação contra uma controladora UniFi Network 10.4.57 e comparação com a documentação oficial versionada. As conclusões devem ser lidas dentro desse escopo: campos podem variar entre versões e modelos.

## Base da API e documentação

- Base local validada: `https://<host>:11443/proxy/network/integration/v1`.
- `/unifi-api/network` é a interface autenticada de documentação e pode retornar HTML.
- Não foi encontrada uma especificação OpenAPI servida diretamente pela controladora nos caminhos locais testados.
- A Ubiquiti publica OpenAPI, coleção Postman e exemplos no Developer Portal oficial, separados por versão do UniFi Network.

## Endpoints confirmados no ambiente 10.4.57

| Endpoint | Status | Observações |
|---|---:|---|
| `GET /sites` | 200 | `{offset,limit,count,totalCount,data[]}` |
| `GET /sites/{siteId}/devices` | 200 | Inventário resumido de dispositivos |
| `GET /sites/{siteId}/devices/{deviceId}` | 200 | Portas e rádios embutidos em `interfaces` |
| `GET /sites/{siteId}/devices/{deviceId}/statistics/latest` | 200 | Uptime, heartbeat, CPU, memória, carga e taxas de uplink |
| `GET /sites/{siteId}/clients` | 200 | Clientes cabeados, wireless e tipos de acesso disponíveis |
| `GET /sites/{siteId}/devices/{deviceId}/ports` | 404 | Portas vêm no detalhe do dispositivo |
| `GET /sites/{siteId}/devices/{deviceId}/radios` | 404 | Rádios vêm no detalhe do dispositivo |

Erros observados:

- chave inválida: `401`;
- recurso inexistente: `404`.

## Paginação

O envelope usa `offset`, `limit`, `count`, `totalCount` e `data[]`. Para descoberta completa, avance `offset` pelo `count` retornado até cobrir `totalCount`. Um `limit` alto não deve ser tratado como garantia de página única.

## PoE

A documentação oficial versionada descreve `interfaces.ports[].poe` com campos de estado/capacidade, incluindo:

- `enabled`;
- `standard`;
- `state`;
- `type`.

Esses campos podem ser opcionais e não aparecer em modelos ou portas sem suporte PoE. No schema analisado não foram encontrados:

- consumo instantâneo em watts;
- tensão ou corrente;
- orçamento total/disponível do switch;
- energia acumulada.

Portanto, o projeto pode descobrir e monitorar estado/capacidade PoE, mas não deve prometer telemetria elétrica sem confirmação adicional.

## Outros recursos documentados relevantes

- relação de topologia por `uplink.deviceId`;
- taxas agregadas em `statistics/latest.uplink`;
- estados detalhados de dispositivo, além de apenas online/offline;
- grupos LAG em recursos de switching nas versões que os documentam;
- ação de porta `POWER_CYCLE`, que deve ficar fora do template somente leitura e usar credencial de escrita separada.

## Limitações observadas

No ambiente e schemas analisados não foram confirmados contadores RX/TX por porta, erros, descartes, duplex, STP, potência de rádio, interferência, utilização de canal ou orçamento PoE. Gateway/WAN/VPN exige validação com hardware correspondente.

## Zabbix

- Macro secreta exportada como `SECRET_TEXT`.
- `verify_peer` e `verify_host` são valores fixos `YES`/`NO`; não aceitam macro de usuário.
- O timeout deve usar um intervalo Zabbix explícito, por exemplo `10s`.
