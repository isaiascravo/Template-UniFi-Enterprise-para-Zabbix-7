# Notas de import real — `unifi_network_and_devices.yaml`

`templates/unifi_network_and_devices.yaml` foi importado com sucesso via
API (`configuration.import`) num Zabbix 7.0.28 de produção real e validado
de ponta a ponta: descoberta automática criou hosts para os dispositivos
adotados (access points e switch), e triggers de porta/rádio dispararam
corretamente sobre condições reais (porta negociada abaixo da velocidade
máxima, rádio com retransmissão alta). Seis problemas só apareceram nesse
import real — nenhum aparecia validando o YAML apenas com um parser
genérico — e foram corrigidos diretamente no arquivo. Documentados aqui
para quem for importar isso pela primeira vez.

## 1. `triggers`/`graphs` de nível normal vão na raiz do `zabbix_export`

Triggers e graphs que não são prototypes (ou seja, não pertencem a uma
`discovery_rule`) devem ficar como listas no nível raiz de `zabbix_export`,
**não** aninhados dentro de cada `template`. Confirmado exportando um
template padrão do próprio Zabbix (`configuration.export`) e comparando a
estrutura:

```yaml
zabbix_export:
  version: '7.0'
  template_groups: [...]
  templates: [...]
  triggers: [...]   # não fica dentro de templates[i]
  graphs: [...]     # idem
```

## 2. O campo é `verify_peer`/`verify_host`, não `ssl_verify_peer`/`ssl_verify_host`

Erro do importador: `unexpected tag "ssl_verify_peer"`.

## 3. Tipo de macro secreta é `SECRET_TEXT`, não `SECRET`

Confirmado na documentação oficial do Zabbix 7: os valores válidos para o
campo `type` de uma macro são `TEXT` (padrão), `SECRET_TEXT` e `VAULT`.

## 4. Não existe função de trigger `prev()`

Para detectar mudança de valor (ex.: firmware alterado), use:

```
last(/host/item,#1)<>last(/host/item,#2)
```

em vez de `last(/host/item)<>prev(/host/item)`.

## 5. Host prototype exige `group_links` além de `group_prototypes`

`group_prototypes` (nomes dinâmicos com macros LLD, tipo
`UniFi/{#SITE_NAME}`) não bastam sozinhos — o import falha com
`"groupLinks" cannot be empty`. É preciso pelo menos um `group_links` com um
grupo **estático já existente**:

```yaml
group_links:
- group:
    name: '{$UNIFI.HOST.GROUP}'
group_prototypes:
- name: 'UniFi/{#SITE_NAME}'
- name: 'UniFi/{#SITE_NAME}/{#DEVICE_TYPE}'
```

Se o grupo referenciado não existir ainda, crie-o antes de importar
(`hostgroup.create` ou pela UI) — o import não cria automaticamente o
grupo usado em `group_links` via macro na primeira vez.

## 6. `group_links` com macro só resolve no *import* do YAML

O padrão acima (`name: '{$UNIFI.HOST.GROUP}'`) funciona no import do YAML,
que resolve a macro usando o valor padrão definido no próprio template no
momento do import. Mas a API `hostprototype.update`, usada para editar um
host prototype **já existente**, exige um `groupid` concreto — não aceita
nome de macro. Para trocar o grupo de uma instância já importada sem
reimportar do zero, descubra o `groupid` do grupo desejado e chame
`hostprototype.update` com esse ID diretamente.

## Cuidado ao editar macros de template via API

`template.update` com o parâmetro `macros` **substitui a lista inteira** —
omitir uma macro existente a apaga silenciosamente, mesmo que você só
quisesse adicionar ou mudar uma. Isso já derrubou itens HTTP Agent em
produção (a macro de timeout foi apagada sem querer, e o item ficou com o
erro `"Unsupported timeout value."` até a macro ser restaurada). Sempre
releia todas as macros atuais do template (`template.get` com
`selectMacros`) antes de enviar uma atualização parcial, e lembre que
macros do tipo `SECRET_TEXT` nunca retêm o valor real por essa consulta —
reenviar o objeto como veio da API sem preencher `value` explicitamente
falha com `"the parameter 'value' is missing"`.
