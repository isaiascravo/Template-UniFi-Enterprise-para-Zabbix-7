# Changelog

## [Unreleased]

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
