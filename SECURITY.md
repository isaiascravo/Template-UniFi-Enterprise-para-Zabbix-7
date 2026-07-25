# Segurança

## Relato de vulnerabilidades

Não publique credenciais, API keys, cookies, tokens, IPs públicos, MACs reais ou dados de clientes em issues.

Ao relatar falhas, forneça somente amostras sanitizadas e descreva a versão do UniFi Network e do Zabbix.

## Segredos

A macro `{$UNIFI.API.KEY}` deve ser configurada como macro secreta no Zabbix. Nunca a mantenha no YAML exportado.
