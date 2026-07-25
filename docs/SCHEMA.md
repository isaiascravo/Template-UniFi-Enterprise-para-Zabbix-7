# Schema monitorado

## Página paginada

Campos obrigatórios usados pelo projeto:

- `offset`
- `limit`
- `count`
- `totalCount`
- `data[]`

## Site

- `id`
- `name`
- `internalReference`

## Dispositivo

- `id`
- `name`
- `model`
- `state`
- `macAddress`
- `ipAddress`
- `firmwareVersion`
- `firmwareUpdatable`
- `features`
- `interfaces.ports[]`
- `interfaces.radios[]`
- `uplink.deviceId` quando presente

## Porta

- `idx`
- `state`
- `connector`
- `speedMbps`
- `maxSpeedMbps`
- `poe.enabled` quando presente
- `poe.standard` quando presente
- `poe.state` quando presente
- `poe.type` quando presente

## Estatísticas

- `uptimeSec`
- `lastHeartbeatAt`
- `nextHeartbeatAt`
- `cpuUtilizationPct`
- `memoryUtilizationPct`
- `loadAverage1Min`
- `loadAverage5Min`
- `loadAverage15Min`
- `uplink.txRateBps`
- `uplink.rxRateBps`

Campos opcionais devem usar preprocessing tolerante a ausência e nunca tornar o item mestre unsupported.
