#!/usr/bin/env python3
# Copyright 2022 Guillaume
# See LICENSE file for licensing details.

import logging

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, BlockedStatus, MaintenanceStatus, WaitingStatus
from ops.pebble import Layer

logger = logging.getLogger(__name__)


class ExternalDnsCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self._container_name = self._service_name = "external-dns"
        self._container = self.unit.get_container(self._container_name)
        self.framework.observe(self.on.config_changed, self._on_pebble_ready)
        self.framework.observe(self.on.external_dns_pebble_ready, self._on_pebble_ready)

    def _on_pebble_ready(self, event):
        if self._config_is_valid:
            self.unit.status = ActiveStatus()
        else:
            self.unit.status = BlockedStatus("Config is not valid")
            event.defer()
            return
        self._configure_pebble(event)
        self.unit.status = ActiveStatus()

    @property
    def _config_is_valid(self):
        if not self._provider:
            return False

        if not self._domain:
            return False

        if self._provider == "google":
            if self._google_project:
                return True
            else:
                return False

    def _configure_pebble(self, event):
        if self._container.can_connect():
            plan = self._container.get_plan()
            layer = self._pebble_layer
            if plan.services != layer.services:
                self.unit.status = MaintenanceStatus(
                    f"Configuring pebble layer for {self._service_name}..."
                )
                self._container.add_layer(self._container_name, layer, combine=True)
                self._container.restart(self._service_name)
                logger.info(f"Restarted container {self._service_name}")
                self.unit.status = ActiveStatus()
        else:
            self.unit.status = WaitingStatus("Waiting for container to be ready...")
            event.defer()

    @property
    def _pebble_layer(self) -> Layer:
        """Returns pebble layer for the charm."""

        base_command = [
            "--source=service",
            "--source=ingress",
            f"--domain-filter={self._domain}",
            f"--provider={self._provider}",
            "--policy=upsert-only",
            "--registry=txt",
            "--txt-owner-id=my-identifier",
        ]
        provider_specific_args = self._get_provider_specific_args(self._provider)
        exec_command = base_command + provider_specific_args

        return Layer(
            {
                "summary": f"{self._service_name} pebble layer",
                "services": {
                    self._service_name: {
                        "override": "replace",
                        "startup": "enabled",
                        "command": exec_command,
                    }
                },
            }
        )

    def _get_provider_specific_args(self, provider: str):
        if provider == "google":
            return ["--google-zone-visibility=private", f"--google-project={self._google_project}"]

    @property
    def _provider(self) -> str:
        return self.model.config.get("provider", None)

    @property
    def _google_project(self) -> str:
        return self.model.config.get("google-project", None)

    @property
    def _domain(self) -> str:
        return self.model.config.get("domain", None)


if __name__ == "__main__":
    main(ExternalDnsCharm)
