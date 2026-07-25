# Changelog

## [Unreleased]

### Added (import real validado)

- `templates/unifi_network_and_devices.yaml`: dois templates com
  descoberta de site → dispositivos → portas de switch → rádios de AP,
  itens dependentes, value maps e triggers de porta/rádio. Importado via
  API e validado de ponta a ponta num Zabbix 7.0.28 de produção real (3
  access points e 1 switch descobertos automaticamente; triggers de porta
  abaixo da velocidade máxima e de retransmissão de rádio dispararam sobre
  dados reais).
- Macro `{$UNIFI.HOST.GROUP}` (padrão `UniFi`): grupo estático em que cada
  host descoberto entra, parametrizável para reusar um grupo já existente
  em vez de criar um novo (essencial num Zabbix multi-tenant/MSP).
- `docs/IMPORT-NOTES.md`: seis problemas reais encontrados só ao importar
  de verdade (posição de `triggers`/`graphs` no schema, nome correto de
  `verify_peer`/`verify_host`, `SECRET_TEXT` vs `SECRET`, ausência da
  função `prev()`, exigência de `group_links` em host prototypes, e o
  cuidado com `template.update` substituindo a lista inteira de macros).
- `docs/ROADMAP.md`: v0.3 marcada como entregue e v0.4 como parcialmente
  entregue (faltando PoE e LAG) nesse novo template.

### Added (this update)

- `GET /info` de volta ao template (`unifi.api.info.raw` + item dependente
  `unifi.api.info.application_version`). Um commit anterior o removeu por
  julgá-lo não confirmado; na verdade é um endpoint real e documentado -
  confirmado ao vivo contra o ambiente de referência, que retornou
  `{"applicationVersion": "10.4.57"}`, batendo com a versão citada em
  `docs/VERSION_MATRIX.md`.
- `docs/API-NOTES.md`: seção listando a superfície de API adicional
  confirmada existir na spec oficial `network/v10.4.57` (firewall, DNS,
  VPN, hotspot, RADIUS, DPI, MC-LAG/stacking) mas ainda não implementada;
  `wans`, `switching/lags` e `networks` testados ao vivo (200, vazios ou
  com dados reais conforme o recurso).
- `docs/ROADMAP.md`: nova fase v0.7 para essa superfície estendida.

### Fixed

- Corrigida a base da API para `/proxy/network/integration/v1`.
- Removidos endpoints inexistentes e corrigido o smoke test para `GET /sites`.
- Corrigido o tipo de macro secreta para `SECRET_TEXT`.
- Removida a expectativa de controlar `verify_peer`/`verify_host` por macro.
- Timeout alterado para intervalo Zabbix explícito (`10s`).
- Documentação de PoE corrigida: estado/capacidade por porta são documentados, mas watts, tensão, corrente e orçamento não foram encontrados.
- Documentação de OpenAPI corrigida: não exposta nos caminhos locais testados, porém disponível no Developer Portal oficial.
- Licença consolidada em MIT.

### Added

- `docs/API-NOTES.md` com endpoints e limitações validados.
- `docs/OPENAPI.md` com política de uso dos contratos oficiais.
- `docs/SCHEMA.md` com os campos monitorados.
- `docs/VERSION_MATRIX.md` com matriz inicial de compatibilidade.
- Fixtures sanitizadas para sites e switch com PoE opcional.
- Testes automatizados de contrato, fixture e template.
- GitHub Actions para compilação Python, validação JSON e testes.
- Item dependente `unifi.api.sites.count`.

### Changed

- Roadmap reorganizado para desenvolvimento orientado a schema, fixtures e testes.

## Anterior

- Estrutura inicial do projeto.
- Template alfa para UniFi Network Controller via API oficial.
- Documentação de instalação, segurança e roadmap.
