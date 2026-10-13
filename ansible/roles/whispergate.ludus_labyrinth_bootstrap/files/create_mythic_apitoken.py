#!/usr/bin/env python3
"""Create a Mythic operator API token via GraphQL login (Mythic 3.x style)."""
from __future__ import annotations

import json
import os
import ssl
import sys
import urllib.error
import urllib.request


def post_json(url: str, payload: dict, headers: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    graphql_url = os.environ.get("MYTHIC_GRAPHQL_URL", "https://127.0.0.1:7443/graphql")
    username = os.environ["MYTHIC_ADMIN_USER"]
    password = os.environ["MYTHIC_ADMIN_PASSWORD"]
    token_name = os.environ.get("MYTHIC_TOKEN_NAME", "labyrinth-bootstrap")

    login_query = """
    mutation Login($username: String!, $password: String!) {
      login(username: $username, password: $password) {
        status
        error
        access_token
        refresh_token
      }
    }
    """
    login_body = post_json(
        graphql_url,
        {
            "query": login_query,
            "variables": {"username": username, "password": password},
        },
    )
    login = (login_body.get("data") or {}).get("login") or {}
    if login.get("status") != "success" or not login.get("access_token"):
        print(json.dumps({"error": "login failed", "body": login_body}), file=sys.stderr)
        return 1
    access = login["access_token"]

    create_query = """
    mutation CreateToken($name: String!) {
      createAPIToken(name: $name) {
        status
        error
        token_value
      }
    }
    """
    create_body = post_json(
        graphql_url,
        {"query": create_query, "variables": {"name": token_name}},
        headers={"Authorization": f"Bearer {access}"},
    )
    token_block = (create_body.get("data") or {}).get("createAPIToken") or {}
    token_value = token_block.get("token_value")
    if token_block.get("status") == "success" and token_value:
        print(token_value)
        return 0

    # Mythic 3.x fallback: apitoken header from login access_token
    if access:
        print(access)
        return 0

    print(json.dumps({"error": "token creation failed", "body": create_body}), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
