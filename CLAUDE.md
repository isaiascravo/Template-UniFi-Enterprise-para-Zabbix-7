# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A community Zabbix 7 template package for monitoring UniFi Network controllers via the
**official local API** (`integration/v1`, API-key auth — no session/cookie scraping). The
deliverable is not application code: it's Zabbix YAML templates (`templates/*.yaml`) plus the
documentation and tests that keep them honest. Repo documentation (README, docs/, commit
messages) is written in Portuguese; code, tests, and identifiers are in English.

Project status is **alpha**, validated against a live UniFi Network 10.4.57 controller and a
production Zabbix 7.0.28 instance. The core rule driving every change here: **never claim a
field, endpoint, or metric works unless it's backed by official documentation or a real,
sanitized response.** See `docs/API-NOTES.md` and `docs/VERSION_MATRIX.md`.

## Commands

```bash
# Install the only dependency needed to validate/test
python -m pip install PyYAML==6.0.2

# Run the full test suite (contract + full-template tests)
python -m unittest discover -s tests -v

# Run a single test file
python -m unittest tests.test_contracts -v
python -m unittest tests.test_full_template -v

# Run a single test case
python -m unittest tests.test_full_template.FullTemplateTests.test_no_private_ip_hardcoded_as_default -v

# Byte-compile check (what CI runs)
python -m compileall -q scripts tests

# Validate all fixture JSON parses
python -c "import json,glob; [json.loads(open(f,encoding='utf-8').read()) for f in glob.glob('tests/fixtures/*.json')]"

# Smoke-test a real controller (requires network access + a read-only API key)
python scripts/test_api.py --url https://<host>:11443/proxy/network/integration/v1 --api-key <key>
# add --insecure only to skip TLS verification against a self-signed controller
```

CI (`.github/workflows/validate.yml`) runs on push to `main`/`agent/**` and on PRs: it installs
PyYAML, compiles `scripts`/`tests`, validates fixture JSON, and runs
`python -m unittest discover -s tests -v`. There is no lint/format step — correctness here is
enforced entirely by the unittest suite in `tests/`.

## Architecture

### Two templates, two levels of maturity

- `templates/unifi_network_controller.yaml` — minimal alpha template (`/info` + `/sites` only).
  Exists to validate connectivity before importing the full template. Single Zabbix template.
- `templates/unifi_network_and_devices.yaml` — the real deliverable: **two** linked Zabbix
  templates in one export, `Template UniFi Network by Official API` (site-level) and
  `Template UniFi Device by Official API` (device-level), wired together by low-level discovery
  (LLD):

  ```
  UniFi Network template
    └─ discovery_rules: "UniFi device discovery (site)"
         └─ host_prototypes → creates one host per discovered device,
            linked to "Template UniFi Device by Official API"
              └─ discovery_rules: "UniFi port discovery" (interfaces.ports[])
              └─ discovery_rules: "UniFi radio discovery" (interfaces.radios[])
  ```

  This template was imported end-to-end into a real Zabbix 7.0.28 (3 access points + 1 switch
  auto-discovered, port/radio triggers firing on real data). Six issues only surfaced during that
  real import, not from YAML/schema validation alone — read `docs/IMPORT-NOTES.md` before hand-editing
  this file. The most consequential ones:
  - top-level (non-prototype) `triggers:`/`graphs:` live at the **root** of `zabbix_export`, not
    nested inside each `templates[i]` entry.
  - HTTP Agent TLS fields are `verify_peer`/`verify_host`, not `ssl_verify_peer`/`ssl_verify_host`.
  - secret macros use `type: SECRET_TEXT`, not `SECRET`.
  - there is no `prev()` trigger function; use `last(/host/item,#1)<>last(/host/item,#2)`.
  - a host prototype needs a static `group_links` entry (an existing group) in addition to
    `group_prototypes` (LLD-macro-based dynamic names) — `group_prototypes` alone fails import.
  - `template.update` with `macros` **replaces the whole macro list**; always re-read current
    macros via `template.get`/`selectMacros` before a partial update, and `SECRET_TEXT` macros
    never round-trip their value through `get`.

### Item pattern: raw master item + dependent items

Every metric group follows the same shape: one HTTP Agent item does the actual GET request and
stores the raw JSON (e.g. `unifi.api.sites.raw`), and one or more `DEPENDENT` items extract
individual fields from it via JSONPath preprocessing (e.g. `unifi.api.sites.count` ←
`$.totalCount`). This minimizes API calls — discovery and every derived metric reuse the same
raw response instead of re-polling. When adding a new metric, extend an existing raw item with a
new dependent item rather than adding a new HTTP request unless the data isn't already fetched.

Pagination envelope (`offset`, `limit`, `count`, `totalCount`, `data[]`) is required on every
list endpoint; `docs/SCHEMA.md` lists exactly which fields per resource are actually consumed by
the template. Optional fields (e.g. `poe.*`, only present on PoE-capable ports) must use
preprocessing that tolerates absence and never mark the master item unsupported.

### Required host macros

`{$UNIFI.API.URL}`, `{$UNIFI.API.KEY}` (must be `SECRET_TEXT`), `{$UNIFI.API.TIMEOUT}` (explicit
Zabbix interval like `10s`, not a raw number), and for the full template `{$UNIFI.SITE.ID}`,
`{$UNIFI.SITE.NAME}`, and `{$UNIFI.HOST.GROUP}` (the static group discovered hosts link into —
defaults to `UniFi`, must stay generic/reusable, never a specific deployer's own group name).

### Documentation layout (`docs/`)

- `API-NOTES.md` — endpoint-by-endpoint validation status against the live 10.4.57 reference
  controller, plus a list of documented-but-not-yet-implemented API surface (firewall, DNS, VPN,
  hotspot, RADIUS, DPI, MC-LAG, etc.) kept as verifiable roadmap material, not promises.
  Write-type actions (e.g. port `POWER_CYCLE`) are explicitly excluded from this read-only template.
- `SCHEMA.md` — the exact subset of API response fields the template actually consumes.
- `VERSION_MATRIX.md` — which UniFi Network versions are validated vs. researched-only.
- `IMPORT-NOTES.md` — real Zabbix-import failure modes and their fixes (see above).
- `ROADMAP.md` — versioned plan (v0.1 done through v1.0); every new metric entry must record which
  documentation version was checked and, where possible, ship with a sanitized fixture + test.
- `OPENAPI.md` — the controller does not serve `openapi.json` locally; official specs come from
  Ubiquiti's Developer Portal (versioned) and must never be auto-fetched at template runtime —
  only reviewed and vendored deliberately.

### Tests (`tests/`)

`test_contracts.py` and `test_full_template.py` are plain `unittest` cases that parse the YAML
templates with `yaml.safe_load` and assert on structure — no live API calls, no Zabbix instance
required. Categories of assertions worth knowing before adding a template feature:
- **schema/shape**: dependent items reference the right master item and JSONPath, UUIDs are
  unique, triggers/graphs sit at the correct nesting level.
- **hygiene/leak prevention**: no real secret (`X-API-Key: `) ever appears literally in a
  template, no hardcoded private IPv4 literal, no hardcoded client/company name — this template
  must stay importable as-is by any operator.
- **fixtures** (`tests/fixtures/*.json`): sanitized, realistic API responses (e.g.
  `device-detail-switch.json` models a port with PoE and one without) used to assert the schema
  assumptions the template's JSONPath preprocessing relies on.

When adding a new endpoint or field: add a sanitized fixture, a contract test asserting the
template consumes it correctly, and a `docs/SCHEMA.md`/`docs/API-NOTES.md` entry citing the
documentation version — mirroring the existing pattern is more important than the specific test
content.

## Security / sanitization rules (enforced by tests, not just convention)

- Never commit a real API key, cookie, token, public IP, real MAC address, or customer-identifying
  name — anywhere (templates, fixtures, docs, commit messages). `SECURITY.md` and
  `test_no_real_secret_is_versioned*`, `test_no_private_ip_hardcoded_as_default`,
  `test_no_hardcoded_client_or_company_names` enforce this for the templates.
  `{$UNIFI.API.KEY}` must always appear as the macro placeholder, never a literal value.
- Don't promise telemetry that isn't in the official schema (e.g. PoE watts/voltage/current/budget
  are explicitly *not* implemented — only enable/standard/state/type are documented and consumed).
