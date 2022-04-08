# external-dns-operator

> **Warning** This project is a work in progress.

ExternalDNS makes Kubernetes resources discoverable via public DNS servers. This charm makes it 
possible to deploy external-dns on any Kubernetes environment using Juju.

## Todo
- Implement relationship so that when charms relate to external-dns, they receive the domain name
- Implement library so that when charms relate to external-dns, the logic to create an annotation
to their service is abstracted to the charm developer.

## Configs

### Mandatory
For this charm to function correctly, some configuration parameters need to be set:
- Domain: The domain name to be registered in you cloud DNS
- Provider: The DNS provider. Currently, only "google" is provided.

### Optional
Depending on the provider, some extra configuration parameters will have to be set.

#### Google
When using the "google" provider, the following parameters must be set:
- google-project

## Relations

Charm X provides the domain name (ex. `nginx`) and external-dns provides the annotation to write 
to their service (ex. `external-dns.alpha.kubernetes.io/hostname: nginx.external-dns-test.gcp.zalan.do`)

## Usage

```bash
juju deploy external-dns
juju deploy your-charm
juju relate external-dns your-charm
```
