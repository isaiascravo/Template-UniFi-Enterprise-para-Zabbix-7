#!/usr/bin/env python3
"""Smoke test for the official local UniFi Network API."""

from __future__ import annotations

import argparse
import json
import ssl
import sys
import urllib.error
import urllib.request
from typing import Any


REQUIRED_PAGE_FIELDS = {"offset", "limit", "count", "totalCount", "data"}


def request_json(
    base_url: str,
    api_key: str,
    endpoint: str,
    verify_tls: bool,
    timeout: float,
) -> Any:
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    request = urllib.request.Request(
        url,
        headers={"X-API-Key": api_key, "Accept": "application/json"},
        method="GET",
    )
    context = None if verify_tls else ssl._create_unverified_context()
    with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
        content_type = response.headers.get_content_type()
        if content_type != "application/json":
            raise ValueError(f"Unexpected content type from {url}: {content_type}")
        return json.load(response)


def validate_page(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Unexpected response: JSON root is not an object")

    missing = REQUIRED_PAGE_FIELDS.difference(payload)
    if missing:
        raise ValueError(f"Unexpected response: missing fields {sorted(missing)}")

    if not isinstance(payload["data"], list):
        raise ValueError("Unexpected response: data is not an array")

    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate access to the UniFi Network integration/v1 API."
    )
    parser.add_argument(
        "--url",
        required=True,
        help="API base URL ending in /proxy/network/integration/v1",
    )
    parser.add_argument("--api-key", required=True)
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS certificate and hostname validation.",
    )
    args = parser.parse_args()

    try:
        payload = request_json(
            args.url,
            args.api_key,
            "sites?offset=0&limit=1",
            not args.insecure,
            args.timeout,
        )
        page = validate_page(payload)
        print(
            "sites: OK "
            f"(returned={page['count']}, total={page['totalCount']}, "
            f"offset={page['offset']}, limit={page['limit']})"
        )
    except urllib.error.HTTPError as exc:
        print(f"API test failed: HTTP {exc.code} {exc.reason}", file=sys.stderr)
        return 1
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        print(f"API test failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
