# Changelog

## [Unreleased]

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
