# Changelog

## [Unreleased]

### Fixed

- Corrigida a base da API no template e no README: `{$UNIFI.API.URL}` de
  exemplo apontava para `/unifi-api/network` (página de documentação HTML,
  não a API) em vez de `/proxy/network/integration/v1`.
- Removidos os endpoints `/v1/info` e `/v1/sites` (prefixo `/v1` inexistente
  e um endpoint `info` nunca confirmado); substituídos pelo endpoint real e
  validado `GET /sites`.
- Corrigidos os campos `verify_peer`/`verify_host` do item HTTP Agent, que
  usavam a macro `{$UNIFI.API.TLS_VERIFY}` - esses campos são checkboxes
  fixos no Zabbix e não aceitam macro de usuário (confirmado na
  documentação oficial). Removida a macro `{$UNIFI.API.TLS_VERIFY}`, que
  não tinha efeito real; os itens agora fixam `verify_peer`/`verify_host`
  como `NO`, documentado no próprio YAML.
- Consolidada a licença do projeto em MIT (a branch `main` ainda tinha
  Apache-2.0 do template inicial do GitHub).

### Added

- `docs/API-NOTES.md`: achados de uma validação real contra um UniFi OS
  Server ao vivo - endpoints confirmados/ausentes, formato de paginação e
  erro, e duas pegadinhas de schema do Zabbix (`SECRET_TEXT` vs `SECRET`
  para macro secreta; `verify_peer`/`verify_host` não aceitam macro).
- Item dependente `unifi.api.sites.count`, demonstrando o padrão de "uma
  chamada por payload, métricas derivadas via item dependente" que o
  README já prometia mas o template ainda não exemplificava.

### Changed

- `docs/ROADMAP.md` anotado com o que já está confirmado versus o que
  ainda é suposição (PoE, erros de porta, endpoints de auditoria, WAN).

## Anterior

- Estrutura inicial do projeto.
- Template alfa para UniFi Network Controller via API oficial.
- Documentação de instalação, segurança e roadmap.
