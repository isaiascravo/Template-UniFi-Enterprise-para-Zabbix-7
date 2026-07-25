# Roadmap

> Toda métrica nova deve indicar a versão da documentação consultada e, quando possível, possuir fixture sanitizada e teste automatizado.

## v0.1 — Controller

- Coleta de `/info` e `/sites`, cada um com item mestre e item dependente.
- Macro `{$UNIFI.API.KEY}` como `Secret text`.
- Timeout explícito e TLS documentado.
- Smoke test da API local.

## v0.2 — Contratos e testes

- Matriz de compatibilidade por versão.
- Notas de OpenAPI/Postman oficial.
- Fixtures sanitizadas de sites, dispositivos, clientes e estatísticas.
- Testes de schema e JSONPath.
- GitHub Actions para YAML, JSON e testes Python.

## v0.3 — Sites e dispositivos

- LLD de sites.
- Descoberta de dispositivos por site.
- Inventário de modelo, firmware, MAC, IP, estado e recursos.
- Value maps para estados detalhados.
- Topologia por `uplink.deviceId` quando disponível.

## v0.4 — Switching e Wi-Fi

- LLD de portas em `interfaces.ports[]`.
- PoE: habilitação, padrão, estado e tipo quando `interfaces.ports[].poe` estiver presente.
- Não prometer watts, tensão, corrente ou orçamento PoE sem campo documentado/validado.
- LLD de rádios em `interfaces.radios[]`.
- Métricas disponíveis em `statistics/latest`, incluindo `txRetriesPct` quando presente.
- Descoberta de LAG nas versões que expõem esse recurso.

## v0.5 — Clientes e dashboards

- Agregação de clientes wired, wireless e tipos de acesso documentados.
- Dashboard NOC, switching, Wi-Fi e MSP.
- Supressão de sintomas: não gerar cascata de alertas de portas/rádios quando o dispositivo pai estiver indisponível.

## v0.6 — Ações opcionais

- Módulo separado para `POWER_CYCLE` de porta.
- Credencial de escrita separada da chave somente leitura.
- Nenhuma ação destrutiva ou de remediação automática no template principal.

## v0.7 — Superfície estendida (pesquisa)

A spec oficial `network/v10.4.57` documenta bastante além do que este
projeto usa hoje; nada nesta lista foi testado (exceto `wans`,
`switching/lags` e `networks`, confirmados vazios/funcionais no ambiente de
referência - ver `docs/API-NOTES.md`). Cada item exige validação com
resposta real antes de virar item/trigger:

- Firewall e ACLs (`firewall/policies`, `firewall/zones`, `acl-rules`).
- DNS (`dns/policies`).
- VPN (`vpn/servers`, `vpn/site-to-site-tunnels`).
- Hotspot (`hotspot/vouchers`) e RADIUS (`radius/profiles`).
- SSIDs (`wifi/broadcasts`).
- DPI (`dpi/applications`, `dpi/categories`).
- MC-LAG e stacking de switches (`switching/mc-lag-domains`, `switching/switch-stacks`).
- Dispositivos pendentes de adoção e tags (`pending-devices`, `device-tags`).

## v1.0

- Compatibilidade documentada.
- Testes automatizados.
- Pacote de release e guia de migração.
