# Network ports

| Port | Protocol | Between | Needed for |
|---|---|---|---|
| 8765 | TCP | Reader ↔ controller | Reader connectivity |
| 8766 | TCP | Reader ↔ controller | Reader connectivity |
| 51926 | TCP | HomeKit client ↔ controller | HomeKit pairing |
| 5353 | UDP, multicast to `224.0.0.251` | HomeKit client ↔ controller | HomeKit pairing (discovery only) |

## Reader connectivity: 8765, 8766

These two are the only ports a reader (ESP8266 or ESP32) needs to reach the
controller. Point `BACKEND_HOST` in the firmware's `include/secrets.h` at the
controller's address; both ports must be reachable from the reader's network.

- **8765/TCP** — the WebSocket transport (`ws://BACKEND_HOST:8765/readers`).
  Carries PN532 commands, discovery/target events, button events and access
  results. Required at all times; without it the reader cannot function.
- **8766/TCP** — plain HTTP. Serves `/firmware/latest`, which the reader
  checks at boot, every six hours, and whenever the controller requests an
  immediate check (see [Controller-managed firmware updates](../README.md#controller-managed-firmware-updates)
  in the README). Also serves `/health` (no auth) and the admin endpoints
  `/api/readers`, `/api/firmware`, `/api/firmware/rollout` (bearer token).

Neither port is needed by a phone, only by readers and whoever administers
the controller over the admin API.

## HomeKit pairing: 51926, 5353/UDP

These are only needed for an iPhone/Apple Watch to register a Wallet
credential in the Home app. They are irrelevant to normal reader operation —
a reader with no phone ever paired still authenticates RFID and already
registered Home Key credentials fine over 8765/8766 alone.

- **51926/TCP** — the HomeKit accessory itself (HAP protocol). The Home app
  connects here once it has found the accessory.
- **5353/UDP, multicast** — mDNS/Bonjour, used by the Home app to *discover*
  the accessory before it can connect to 51926. This is multicast on the
  local subnet, not a normal routed connection: it will not cross most
  routed firewalls or VLAN boundaries without an mDNS reflector, even if
  51926/TCP itself is reachable. This is also why HomeKit pairing does not
  work from a controller running in Docker on macOS/Windows — see
  ["Running the controller in Docker"](../README.md#running-the-controller-in-docker)
  in the README.

## Exposure

Per [`SECURITY.md`](../SECURITY.md): none of these ports should ever be
reachable from the public Internet. 8765/8766 should be reachable only from
the reader/admin network; 51926/5353 only from the LAN segment your HomeKit
clients are on. Use firewall rules or VLAN policy to enforce this rather than
relying on the controller's own access control.
