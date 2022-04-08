# external-dns-operator

> **Warning** This project is a work in progress.

ExternalDNS makes Kubernetes resources discoverable via public DNS servers. This charm makes it 
possible to deploy external-dns on any Kubernetes environment using Juju.

The upstream project is available [here](https://github.com/kubernetes-sigs/external-dns).

## Todo
- Implement relationship so that when charms relate to external-dns, they receive the k8s annotation
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

The only current supported relation is:
- hostname
  - Other charms can relate to external-dns to receive the k8s annotation that they can use to 
  apply to their service in order for it to be publicly accessible. For example, Charm X provides 
  the `nginx` hostname and external-dns would answer back with 
  `external-dns.alpha.kubernetes.io/hostname: nginx.<domain>` where `<domain>` is the domain set up
  in the charm config.

## Usage

```bash
juju deploy external-dns
juju deploy your-charm
juju relate external-dns your-charm
```
