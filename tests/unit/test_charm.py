# Copyright 2022 Guillaume
# See LICENSE file for licensing details.

import unittest

from ops import testing
from ops.model import ActiveStatus, BlockedStatus

from charm import ExternalDnsCharm

testing.SIMULATE_CAN_CONNECT = True


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.harness = testing.Harness(ExternalDnsCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    def test_given_no_config_when_config_changed_then_status_is_blocked(self):
        self.harness.update_config()
        self.assertEqual(self.harness.charm.unit.status, BlockedStatus("Config is not valid"))

    def test_given_provider_is_not_valid_when_config_changed_then_status_is_blocked(self):
        self.harness.update_config({"provider": "blabla", "domain": "bla.com"})
        self.assertEqual(self.harness.charm.unit.status, BlockedStatus("Config is not valid"))

    def test_given_no_domain_in_config_when_config_changed_then_status_is_blocked(self):
        self.harness.update_config({"provider": "google.com", "google-project": "blou.com"})
        self.assertEqual(self.harness.charm.unit.status, BlockedStatus("Config is not valid"))

    def test_given_provider_is_valid_but_provider_specific_config_is_not_set_when_config_changed_then_status_is_blocked(  # noqa: E501
        self,
    ):
        self.harness.update_config({"provider": "google", "domain": "bla.com"})
        self.assertEqual(self.harness.charm.unit.status, BlockedStatus("Config is not valid"))

    def test_given_valid_config_when_config_changed_then_status_is_active(self):
        self.harness.update_config(
            {"provider": "google", "google-project": "blou.com", "domain": "bla.com"}
        )
        self.assertEqual(self.harness.charm.unit.status, ActiveStatus())
