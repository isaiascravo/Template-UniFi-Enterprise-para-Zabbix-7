from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "templates" / "unifi_network_and_devices.yaml"

PRIVATE_IP_RE = re.compile(
    r"\b(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
    r"172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|"
    r"192\.168\.\d{1,3}\.\d{1,3})\b"
)


class FullTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = TEMPLATE_PATH.read_text(encoding="utf-8")
        cls.document = yaml.safe_load(cls.text)
        cls.templates = {t["template"]: t for t in cls.document["zabbix_export"]["templates"]}

    def test_both_templates_present(self) -> None:
        self.assertIn("Template UniFi Network by Official API", self.templates)
        self.assertIn("Template UniFi Device by Official API", self.templates)

    def test_triggers_and_graphs_are_at_export_root_not_inside_templates(self) -> None:
        export = self.document["zabbix_export"]
        self.assertIn("triggers", export)
        self.assertIn("graphs", export)
        for template in export["templates"]:
            self.assertNotIn("triggers", template)
            self.assertNotIn("graphs", template)

    def test_device_discovery_host_prototype_has_group_links(self) -> None:
        network = self.templates["Template UniFi Network by Official API"]
        discovery = next(
            d for d in network["discovery_rules"] if d["host_prototypes"]
        )
        prototype = discovery["host_prototypes"][0]
        self.assertTrue(prototype["group_links"], "host prototype needs a static group_links entry")
        self.assertEqual(prototype["group_links"][0]["group"]["name"], "{$UNIFI.HOST.GROUP}")

    def test_host_group_macro_is_parametrized_not_hardcoded(self) -> None:
        network = self.templates["Template UniFi Network by Official API"]
        macros = {m["macro"]: m.get("value") for m in network["macros"]}
        self.assertIn("{$UNIFI.HOST.GROUP}", macros)
        # must default to something generic, never to a specific deployer's own group/company name
        self.assertEqual(macros["{$UNIFI.HOST.GROUP}"], "UniFi")

    def test_no_hardcoded_client_or_company_names(self) -> None:
        # this template must stay importable as-is by any Zabbix operator
        for needle in ("Inarmeg", "inarmeg"):
            self.assertNotIn(needle, self.text)

    def test_no_private_ip_hardcoded_as_default(self) -> None:
        self.assertIsNone(PRIVATE_IP_RE.search(self.text), "found a private IPv4 literal in the template")

    def test_no_real_secret_is_versioned(self) -> None:
        self.assertIn("{$UNIFI.API.KEY}", self.text)
        self.assertNotIn("X-API-Key: ", self.text)

    def test_secret_macros_are_type_secret_text(self) -> None:
        for template in self.templates.values():
            for macro in template["macros"]:
                if macro["macro"] == "{$UNIFI.API.KEY}":
                    self.assertEqual(macro.get("type"), "SECRET_TEXT")

    def test_trigger_expressions_do_not_use_nonexistent_prev_function(self) -> None:
        for trigger in self.document["zabbix_export"]["triggers"]:
            self.assertNotIn("prev(", trigger["expression"])

    def test_all_uuids_are_unique_across_the_file(self) -> None:
        uuids = re.findall(r"uuid: ([0-9a-f]{32})", self.text)
        self.assertEqual(len(uuids), len(set(uuids)))

    def test_http_agent_items_use_correct_verify_field_names(self) -> None:
        self.assertNotIn("ssl_verify_peer", self.text)
        self.assertNotIn("ssl_verify_host", self.text)

    def test_port_and_radio_discovery_rules_exist(self) -> None:
        device = self.templates["Template UniFi Device by Official API"]
        names = {d["name"] for d in device["discovery_rules"]}
        self.assertIn("UniFi port discovery", names)
        self.assertIn("UniFi radio discovery", names)


if __name__ == "__main__":
    unittest.main()
