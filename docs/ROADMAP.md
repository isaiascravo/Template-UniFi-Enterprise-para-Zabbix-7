# Roadmap

> Ver `docs/API-NOTES.md` antes de implementar qualquer item abaixo: vários
> campos listados nas fases v0.3/v0.4 (PoE, erros de porta, mudanças de
> config) não foram confirmados na API `integration/v1` até agora e podem
> não existir - valide com uma chamada real antes de assumir que o campo
> existe.

## v0.1 — Controller

- ~~API health, versão e tempo de resposta~~ - substituído: nenhum endpoint
  de health/info foi confirmado; a validação inicial ficou em `GET /sites`
  (confirmado, ver `docs/API-NOTES.md`).
- Coleta de `/sites` com item mestre + item dependente (contagem de sites).
- Macros seguras (`{$UNIFI.API.KEY}` como `Secret text`) e TLS documentado
  (verify_peer/verify_host são fixos no Zabbix, não aceitam macro).

## v0.2 — Sites e dispositivos

- LLD de sites (`GET /sites`, confirmado).
- Descoberta de dispositivos por site (`GET /sites/{siteId}/devices`, confirmado).
- Inventário de modelo, firmware, MAC, IP - confirmados. **Serial não está
  presente** nos objetos de dispositivo testados; remover essa expectativa
  ou validar em outro firmware antes de prometer o campo.
- Uplink: só existe como taxa agregada em `statistics/latest.uplink.{txRateBps,rxRateBps}`,
  não há flag indicando qual porta é a de uplink.

## v0.3 — Switching e Wi-Fi

- LLD de portas: confirmado (`interfaces.ports[]` em `GET /sites/{s}/devices/{d}`).
- **PoE e erros de porta: não confirmados** - a API testada não retornou
  esses campos; tratar como pesquisa em aberto, não como entregável certo.
- LLD de rádios 2,4/5 GHz: confirmado (`interfaces.radios[]`); 6 GHz
  depende de hardware Wi-Fi 6E/7 que não foi testado.
- Métricas agregadas de clientes: confirmado (`GET /sites/{s}/clients`,
  agregável por `type` e `uplinkDeviceId`). **SSID não está no objeto de
  cliente** - agregação por SSID não é possível com os campos atuais.

## v0.4 — Auditoria e dashboards

- Mudanças em redes, VLANs, Wi-Fi, firewall, ACL e DNS: **nenhum endpoint
  de auditoria/eventos foi testado ainda** - antes de prometer isso,
  validar se `integration/v1` expõe algo equivalente ou se exigiria a API
  privada/legada (fora do escopo "API oficial" deste projeto).
- Dashboards NOC, Wi-Fi, switching, WAN e MSP: WAN depende de um gateway
  UniFi real para validar - não testado até agora.

## v1.0

- Compatibilidade documentada.
- Testes automatizados.
- Pacote de release e guia de migração.
