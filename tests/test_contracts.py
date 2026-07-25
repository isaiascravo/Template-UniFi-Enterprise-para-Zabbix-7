from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


class ContractTests(unittest.TestCase):
    def test_sites_fixture_has_paginated_envelope(self) -> None:
        payload = json.loads((FIXTURES / "sites.json").read_text(encoding="utf-8"))
        self.assertTrue({"offset", "limit", "count", "totalCount", "data"} <= payload.keys())
        self.assertIsInstance(payload["data"], list)
        self.assertEqual(payload["count"], len(payload["data"]))

    def test_switch_fixture_models_optional_poe(self) -> None:
        device = json.loads(
            (FIXTURES / "device-detail-switch.json").read_text(encoding="utf-8")
        )
        ports = device["interfaces"]["ports"]
        self.assertIn("poe", ports[0])
        self.assertNotIn("poe", ports[1])
        self.assertEqual(
            {"enabled", "standard", "state", "type"},
            set(ports[0]["poe"]),
        )

    def test_zabbix_template_yaml_and_site_count_jsonpath(self) -> None:
        template_path = ROOT / "templates" / "unifi_network_controller.yaml"
        document = yaml.safe_load(template_path.read_text(encoding="utf-8"))
        template = document["zabbix_export"]["templates"][0]
        items = {item["key"]: item for item in template["items"]}
        self.assertIn("unifi.api.sites.raw", items)
        dependent = items["unifi.api.sites.count"]
        self.assertEqual("DEPENDENT", dependent["type"])
        self.assertEqual("$.totalCount", dependent["preprocessing"][0]["parameters"][0])

    def test_zabbix_template_has_info_item_and_dependent(self) -> None:
        template_path = ROOT / "templates" / "unifi_network_controller.yaml"
        document = yaml.safe_load(template_path.read_text(encoding="utf-8"))
        template = document["zabbix_export"]["templates"][0]
        items = {item["key"]: item for item in template["items"]}
        self.assertIn("unifi.api.info.raw", items)
        self.assertTrue(items["unifi.api.info.raw"]["url"].endswith("/info"))
        dependent = items["unifi.api.info.application_version"]
        self.assertEqual("DEPENDENT", dependent["type"])
        self.assertEqual("unifi.api.info.raw", dependent["master_item"]["key"])
        self.assertEqual("$.applicationVersion", dependent["preprocessing"][0]["parameters"][0])

    def test_template_uuids_are_unique(self) -> None:
        template_path = ROOT / "templates" / "unifi_network_controller.yaml"
        document = yaml.safe_load(template_path.read_text(encoding="utf-8"))
        template = document["zabbix_export"]["templates"][0]
        uuids = [item["uuid"] for item in template["items"]]
        self.assertEqual(len(uuids), len(set(uuids)))

    def test_no_real_secret_is_versioned_in_template(self) -> None:
        text = (ROOT / "templates" / "unifi_network_controller.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("{$UNIFI.API.KEY}", text)
        self.assertNotIn("X-API-Key: ", text)


if __name__ == "__main__":
    unittest.main()
