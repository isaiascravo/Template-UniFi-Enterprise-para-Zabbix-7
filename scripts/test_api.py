#!/usr/bin/env python3
"""Smoke test for the UniFi Network official local API."""

from __future__ import annotations

import argparse
import json
import ssl
import sys
import urllib.error
import urllib.request


def request_json(base_url: str, api_key: str, endpoint: str, verify_tls: bool) -> object:
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    request = urllib.request.Request(
        url,
        headers={"X-API-Key": api_key, "Accept": "application/json"},
        method="GET",
    )
    context = None if verify_tls else ssl._create_unverified_context()
    with urllib.request.urlopen(request, timeout=15, context=context) as response:
        return json.load(response)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--api-key", required=True)
    parser.add_argument("--insecure", action="store_true")
    args = parser.parse_args()

    try:
        for endpoint in ("v1/info", "v1/sites"):
            payload = request_json(args.url, args.api_key, endpoint, not args.insecure)
            print(f"{endpoint}: OK ({type(payload).__name__})")
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        print(f"API test failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
